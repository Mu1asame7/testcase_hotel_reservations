async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2021-06-01",
            "date_to": "2021-06-02",
        }
    )
    # print(f"{response.json()=})

    assert response.status_code == 200