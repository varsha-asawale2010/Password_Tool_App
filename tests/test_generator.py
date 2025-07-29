# tests/test_generator.py

from advanced_password_tool.core.generator import generate_strong_password, DEFAULT_LENGTH, MIN_LENGTH

def test_default_generate():
    out = generate_strong_password()
    assert len(out["password"]) == DEFAULT_LENGTH
    assert out["entropy_bits"] > 0

def test_custom_requirements():
    out = generate_strong_password(length=12, min_digits=2, min_symbols=2)
    pwd = out["password"]
    digits = sum(c.isdigit() for c in pwd)
    syms = sum(c in string.punctuation for c in pwd)
    assert digits >= 2
    assert syms >= 2

def test_too_short():
    import pytest
    with pytest.raises(ValueError):
        generate_strong_password(length=4)
