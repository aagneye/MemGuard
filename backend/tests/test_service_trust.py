from app.service_trust import score_trust


def test_user_stated_is_high_trust() -> None:
    trust, ttl = score_trust("user_stated", confidence=1.0)
    assert trust == "high"
    assert ttl == 180


def test_confidence_can_downgrade_trust() -> None:
    trust, ttl = score_trust("tool_inferred", confidence=0.4)
    assert trust == "low"
    assert ttl == 60
