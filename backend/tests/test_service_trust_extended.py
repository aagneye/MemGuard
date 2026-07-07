"""Extended tests for trust scoring — confidence downgrade and TTL values."""
import pytest

from app.service_trust import score_trust


class TestScoreTrust:
    def test_user_stated_high_confidence_is_high(self):
        tier, ttl = score_trust("user_stated", 1.0)
        assert tier == "high"
        assert ttl == 180

    def test_tool_inferred_is_medium(self):
        tier, ttl = score_trust("tool_inferred", 1.0)
        assert tier == "medium"
        assert ttl == 60

    def test_document_extracted_is_low(self):
        tier, ttl = score_trust("document_extracted", 1.0)
        assert tier == "low"
        assert ttl == 14

    def test_low_confidence_high_trust_downgrades_to_medium(self):
        tier, _ = score_trust("user_stated", 0.3)
        assert tier == "medium"

    def test_low_confidence_medium_trust_downgrades_to_low(self):
        tier, _ = score_trust("tool_inferred", 0.3)
        assert tier == "low"

    def test_document_extracted_low_confidence_stays_low(self):
        tier, _ = score_trust("document_extracted", 0.1)
        assert tier == "low"

    def test_borderline_confidence_exactly_half(self):
        tier, _ = score_trust("user_stated", 0.5)
        assert tier == "high"
