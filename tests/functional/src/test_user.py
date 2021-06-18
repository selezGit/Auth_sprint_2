import pytest


@pytest.mark.asyncio
async def test_user_create(make_auth_get_request):
    """Вывести всех персон"""
    data = {'login': 'test_user',
            'email': 'test@gmail.com',
            'password': '1'}

    response = await make_auth_get_request('post', '/user/', data=data)

    assert response.status == 201


@pytest.mark.asyncio
async def test_user_login(make_auth_get_request):
    """Вывести всех персон"""
    data = {'login': 'test_user',
            'password': '1'}

    response = await make_auth_get_request('post', '/login/', data=data)

    assert response.status == 201
