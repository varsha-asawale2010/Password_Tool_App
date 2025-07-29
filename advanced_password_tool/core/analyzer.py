# advanced_password_tool/core/analyzer.py

import math
import hashlib
import requests

try:
    import zxcvbn
    HAVE_ZXCVBN = True
except ImportError:
    HAVE_ZXCVBN = False

def shannon_entropy(password: str) -> float:
    pool = 0
    sets = [
        (any(c.islower() for c in password), 26),
        (any(c.isupper() for c in password), 26),
        (any(c.isdigit() for c in password), 10),
        (any(not c.isalnum() for c in password), 32),
    ]
    pool = sum(size for present, size in sets if present)
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)

def check_pwned_password(password: str) -> int:
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    res = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if res.status_code != 200:
        return -1
    for line in res.text.splitlines():
        h, count = line.split(':')
        if h == suffix:
            return int(count)
    return 0

def analyze_password(password: str, check_breach: bool = False) -> dict:
    result = {
        "password_length": len(password),
        "entropy_bits": shannon_entropy(password),
    }

    if HAVE_ZXCVBN:
        try:
            zx = zxcvbn.zxcvbn(password)
            result["zxcvbn_score"] = zx.get("score")
            result["zxcvbn_guesses"] = zx.get("guesses")
            result["zxcvbn_feedback"] = zx.get("feedback")
        except IndexError:
            result["zxcvbn_error"] = "zxcvbn scoring error"

    if check_breach:
        result["pwned_count"] = check_pwned_password(password)

    return result
