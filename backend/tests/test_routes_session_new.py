from app.routes_session_new import new_session
from app.schemas import NewSessionRequest


def test_new_session_returns_unique_session_id() -> None:
    first = new_session(NewSessionRequest(user_id="demo_alice"))
    second = new_session(NewSessionRequest(user_id="demo_alice"))
    assert first.session_id != second.session_id
    assert first.session_id.startswith("s_")
