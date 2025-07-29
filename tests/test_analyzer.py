# tests/test_analyzer.py
from advanced_password_tool.core.analyzer import analyze_password

def test_entropy_simple():
    res = analyze_password("abc123")
    assert res["length"] == 6
    assert res["shannon_entropy"] > 0

def test_zxcvbn_score_if_available():
    res = analyze_password("correcthorsebatterystaple")
    if "zxcvbn_score" in res:
        assert 0 <= res["zxcvbn_score"] <= 4

def test_breach_flagging():
    res = analyze_password("password", check_breach=True)
    assert isinstance(res.get("pwned_count"), (int,))
