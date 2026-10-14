import json
import re
from datetime import datetime
from urllib.request import Request, urlopen

ORDERS_URL = "https://test.ooobs.ru/api/orders"


def normalize_phone(value):
    digits = re.sub(r"\D", "", str(value or ""))
    if len(digits) == 10 and digits.startswith("9"):
        digits = "7" + digits
    elif len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    if len(digits) != 11 or not digits.startswith("7"):
        return None
    return "+" + digits


def _amount(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("-inf")


def _created(value):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return datetime.min


def transform(orders):
    selected = {}
    invalid = 0
    duplicates = 0
    for order in orders:
        phone = normalize_phone(order.get("phone"))
        if phone is None:
            invalid += 1
            continue
        item = {"name": order.get("name", ""), "phone": phone,
                "email": order.get("email", ""), "amount": order.get("amount", 0)}
        previous = selected.get(phone)
        if previous is not None:
            duplicates += 1
            old_order = previous["_order"]
            if (_amount(order.get("amount")) > _amount(old_order.get("amount")) or
                    (_amount(order.get("amount")) == _amount(old_order.get("amount")) and
                     _created(order.get("created_at")) > _created(old_order.get("created_at")))):
                selected[phone] = {"item": item, "_order": order}
        else:
            selected[phone] = {"item": item, "_order": order}
    return {"clients": [entry["item"] for entry in selected.values()],
            "stats": {"received": len(orders), "unique": len(selected),
                      "duplicates_merged": duplicates, "invalid_dropped": invalid}}


def fetch_result():
    request = Request(ORDERS_URL, headers={"Accept": "application/json"})
    with urlopen(request, timeout=30) as response:
        return transform(json.load(response))
