import pytest


@pytest.mark.asyncio
async def test_get_all_films(prepare_es_film, make_get_request, get_all_data_elastic):
    """Вывести все фильмы"""

    # получаем все фильмы из elasticsearch
    all_films = await get_all_data_elastic('movies')

    response = await make_get_request('/film', {'size': 10000, 'page': 1})

    assert response.status == 200

    assert len(response.body) == len(all_films) - 7


@pytest.mark.asyncio
async def test_search_detailed(prepare_es_film, make_get_request):
    """Поиск конкретного фильма"""

    # Выполнение запроса
    response = await make_get_request('/film', {'query': 'abracadabra'})
    # Проверка результата
    assert response.status == 200

    assert len(response.body) == 1

    assert response.body == prepare_es_film


@pytest.mark.asyncio
async def test_get_by_id(prepare_es_film, make_get_request):
    """Тест проверяет работу получения по id в эндпоинте film"""

    response = await make_get_request('/film/3a5f9a83-4b74-48be-a44e-a6c8beee9460')

    # Проверка результата
    assert response.status == 200

    assert response.body == prepare_es_film[0]


@pytest.mark.parametrize('test_input,expected,error',
                         [({'method': '/film'}, 200,
                          'empty parametr validator, status must be 200'),
                          ({'method': '/film/wrong-uuid'}, 422,
                           'wrong uuid validator, status must be 422'),
                             ({'method': '/film', 'params': {'genre': 'wrong-uuid'}}, 422,
                              'wrong genre uuid validator, status must be 422'),
                             ({'method': '/film', 'params': {'page': 101}}, 422,
                              'too large page validator, status must be 422'),
                             ({'method': '/film', 'params': {'page': 0}}, 422,
                              'too small page validator, status must be 422'),
                             ({'method': '/film', 'params': {'size': 10001}}, 422,
                              'too large size validator, status must be 422'),
                             ({'method': '/film', 'params': {'size': 0}}, 422,
                              'too small size validator, status must be 422'),
                             ({'method': '/film', 'params': {'query': 'MovieNonExists'}}, 404,
                              'search non-existent movie validator, status must be 404')])
@pytest.mark.asyncio
async def test_validator(make_get_request, test_input, expected, error):
    """Тест корректной валидации форм"""

    response = await make_get_request(**test_input)
    assert response.status == expected, error


@pytest.mark.asyncio
async def test_speed(make_get_request):
    """Тест на разгоняемый кэш"""

    # этот запрос сделан без удаления кэша
    response = await make_get_request('/film', {'page': 1, 'size': 10000}, False)
    assert response.status == 200, 'get all movies without delete cache validator, status must be 200'

    # в этом запросе мы получаем результат кэша от первого запроса
    # и сравниваем затраченное время
    response2 = await make_get_request('/film', {'page': 1, 'size': 10000})
    assert response.status == 200, 'get all movies without delete cache validator, status must be 200'

    assert response.resp_speed > response2.resp_speed
