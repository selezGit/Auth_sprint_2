import pytest


@pytest.mark.asyncio
async def test_genre_all_valid_data(prepare_es_genre, make_get_request):
    response = await make_get_request('/genre/', {'page': 1, 'size': 20})

    assert response.status == 200
    assert len(response.body) >= 1


@pytest.mark.parametrize('test_input,expected,error',
                         [({'method': '/genre', 'params': {'page': 0}}, 422,
                          'too small page validator, status must be 422'),
                          ({'method': '/genre', 'params': {'size': 2001}}, 422,
                           'too large size validator, status must be 422'),
                          ({'method': '/genre', 'params': {'size': 0}}, 422,
                           'too small size validator, status must be 422'),
                          ({'method': '/genre/1-not-valid-uuid'}, 422,
                           'not valid genre_id status must be 422'),
                          ({'method': '/genre/6aea47a2-7db0-4bf6-a05a-31ea35eb3cde'}, 404,
                           'not found genre, status must be 404')
                          ])
@pytest.mark.asyncio
async def test_genre_all_not_valid_params(prepare_es_genre, make_get_request, test_input, expected, error):
    response = await make_get_request(**test_input)
    
    assert response.status == expected, error


@pytest.mark.asyncio
async def test_genre_detail_valid_data(prepare_es_genre, make_get_request):
    response = await make_get_request('/genre/e91db2b1-d967-4785-bec9-1eade1d56243')

    assert response.status == 200
    assert response.body == prepare_es_genre[0]
