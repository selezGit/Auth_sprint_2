import pytest


@pytest.mark.asyncio
async def test_user_create(make_auth_get_request):
    data = {'login': 'test_user',
            'email': 'test@gmail.com',
            'password': '1'}

    response = await make_auth_get_request('post', '/user/', data=data)

    assert response.status == 201




@pytest.mark.asyncio
async def test_user_history(make_auth_get_request):

    response = await make_auth_get_request(type='get', method='/user/history', authorization=True)

    assert response.status == 200


@pytest.mark.asyncio
async def test_user_me(make_auth_get_request):

    response = await make_auth_get_request(type='get', method='/user/me', authorization=True)
    assert response.status == 200


@pytest.mark.asyncio
async def test_user_change_email(make_auth_get_request):

    data = {'email': 'test@gmail.com'}
    response = await make_auth_get_request(type='patch', method='/user/change-email', data=data, authorization=True)

    assert response.status == 200


@pytest.mark.asyncio
async def test_user_change_password(make_auth_get_request):

    data = {'old_password': '1',
            'new_password': '1'}
    response = await make_auth_get_request(type='patch', method='/user/change-password', data=data, authorization=True)

    assert response.status == 200
    assert response.body['status'] == 'Success'

@pytest.mark.asyncio
async def test_user_delete(make_auth_get_request):

    response = await make_auth_get_request(type='delete', method='/user/', authorization=True)

    assert response.status == 200
    assert response.body['message'] == 'user successfully deleted'
