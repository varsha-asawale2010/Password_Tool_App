# advanced_password_tool/utils/json_serialization.py
from decimal import Decimal

def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        if obj == obj.to_integral_value():
            return int(obj)
        return float(obj)
    raise TypeError(f"Type {type(obj).__name__} not serializable")
