from app.routes_demo import list_demo_users


def test_list_demo_users_returns_presets() -> None:
    users = list_demo_users()
    assert len(users) >= 2
    assert all(user.id and user.label for user in users)
