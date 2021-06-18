import pytest


@pytest.mark.asyncio
async def test_user(make_auth_get_request):
    """Вывести всех персон"""
    data = {'login': 'test_user',
            'email': 'test@gmail.com',
            'password': '1'}

    response = await make_auth_get_request('/user/', data=data)

    assert response.status == 201