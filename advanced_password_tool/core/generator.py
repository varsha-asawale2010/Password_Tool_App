# advanced_password_tool/core/generator.py

import secrets
import string
import math

from .analyzer import shannon_entropy  # optional, for feedback

DEFAULT_LENGTH = 16
MIN_LENGTH = 8

def calculate_password_entropy(length: int, pool_size: int) -> float:
    """
    Calculate entropy bits: log2(pool_size^length) = length * log2(pool_size)
    """
    return length * math.log2(pool_size)

def generate_strong_password(length: int = DEFAULT_LENGTH,
                             include_lowercase: bool = True,
                             include_uppercase: bool = True,
                             include_digits: bool = True,
                             include_symbols: bool = True,
                             min_lowercase: int = 1,
                             min_uppercase: int = 1,
                             min_digits: int = 1,
                             min_symbols: int = 1) -> dict:
    """
    Generate a strong password satisfying minimum counts for each class.
    Returns: {"password": str, "entropy_bits": float}
    """

    if length < MIN_LENGTH:
        raise ValueError(f"Password length must be >= {MIN_LENGTH}")

    pools = []
    if include_lowercase:
        pools.append((string.ascii_lowercase, min_lowercase))
    if include_uppercase:
        pools.append((string.ascii_uppercase, min_uppercase))
    if include_digits:
        pools.append((string.digits, min_digits))
    if include_symbols:
        pools.append((string.punctuation, min_symbols))

    password_chars = []

    # Enforce minimums first
    for chars, minimum in pools:
        for _ in range(minimum):
            password_chars.append(secrets.choice(chars))

    # Fill the remaining length from full allowed pool
    full_pool = ''.join(chars for chars, _ in pools)
    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(secrets.choice(full_pool))

    # Shuffle to avoid predictable ordering
    secrets.SystemRandom().shuffle(password_chars)
    password = ''.join(password_chars)

    # Compute entropy estimation
    pool_size = len(set(full_pool))
    entropy_bits = calculate_password_entropy(length, pool_size)

    # Optionally or additionally:
    # zshannon = shannon_entropy(password)

    return {"password": password, "entropy_bits": entropy_bits}
