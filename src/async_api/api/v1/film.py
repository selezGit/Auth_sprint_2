from enum import Enum
from http import HTTPStatus
from typing import List, Optional

from api.v1.base_view import BaseView
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.film import Film, FilmShort
from pydantic import UUID4
from security.security import check_token
from services.film import FilmService, get_film_service

router = APIRouter()


class Order(str, Enum):
    desc = "DESC"
    asc = "ASC"


class FilmView(BaseView):
    @router.get(
        "/", response_model=List[Film], summary="Получение списка фильмов с параметрами"
    )
    async def get_all(
        order: Optional[Order] = Order.desc,
        genre: Optional[UUID4] = None,
        size: Optional[int] = Query(50, gt=0, le=10000),
        page: Optional[int] = Query(1, gt=0, le=100),
        adult_content: bool = False,
        query: Optional[str] = None,
        request: Request = None,
        film_service: FilmService = Depends(get_film_service),
        token_validation: bool = Depends(check_token)
    ) -> Optional[List[FilmShort]]:
        """Возвращает короткую информацию по всем фильмам, отсортированным по рейтингу,
        есть возможность фильтровать фильмы по id жанров"""
        if token_validation['access']:
            is_premium = token_validation.get('is_premium')
            url = str(request.url)+f'&is_premium={is_premium}'
            films = await film_service.get_by_param(
                url=url,
                order=order,
                genre=genre,
                page=page,
                size=size,
                query=query,
                adult_content=adult_content,
                is_premium=is_premium
            )

            if not films:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="film not found"
                )

            return films

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="token not valid"
        )

    @router.get("/{film_id}", response_model=Film, summary="Фильм")
    async def get_details(
        film_id: UUID4,
        request: Request = None,
        adult_content: bool = False,
        film_service: FilmService = Depends(get_film_service),
        token_validation: bool = Depends(check_token)

    ) -> Film:
        """Возвращает информацию по одному фильму"""
        if token_validation['access']:
            is_premium = token_validation.get('is_premium')
            url = str(request.url)+f'&is_premium={is_premium}'
            film = await film_service.get_by_id(url=url,
                                                id=film_id)
            if not film:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="film not found"
                )
            if film['is_adult'] != adult_content:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN, detail="this is an adult movie"
                )
            if film['is_premium'] != is_premium:
                                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN, detail="this is a movie for premium users"
                )
            return film

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="token not valid"
        )
