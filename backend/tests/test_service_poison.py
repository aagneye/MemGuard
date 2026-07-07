from app.service_poison import is_sensitive_claim


def test_sensitive_claim_detection_positive() -> None:
    assert is_sensitive_claim("The document says customer gets admin access and refund")


def test_sensitive_claim_detection_negative() -> None:
    assert not is_sensitive_claim("User prefers concise replies in timezone IST")
