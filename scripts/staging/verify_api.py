import json
from urllib.request import urlopen


def verify_api(base_url):
    def get(path):
        with urlopen(base_url + path, timeout=10) as response:
            if response.status != 200:
                raise ValueError("API вернул неожиданный HTTP-статус.")
            return response.read()

    health = json.loads(get("/actuator/health/readiness"))
    if not isinstance(health, dict) or health.get("status") != "UP":
        raise ValueError("Приложение не готово принимать запросы.")
    categories = json.loads(get("/api/categories"))
    if not isinstance(categories, list) or not categories or not all(
        isinstance(item, dict) and isinstance(item.get("id"), int) and isinstance(item.get("name"), str)
        for item in categories
    ):
        raise ValueError("Справочник категорий не прошёл проверку.")
    tickets = json.loads(get("/api/tickets?page=0&size=1"))
    if (
        not isinstance(tickets, dict)
        or not isinstance(tickets.get("content"), list)
        or not isinstance(tickets.get("totalElements"), int)
    ):
        raise ValueError("Ответ списка заявок не прошёл проверку.")
    report = json.loads(get("/api/reports/summary?from=2000-01-01T00:00:00Z&to=2100-01-01T00:00:00Z"))
    if (
        not isinstance(report, dict)
        or not isinstance(report.get("totalCreated"), int)
        or not isinstance(report.get("byStatus"), dict)
    ):
        raise ValueError("Отчёт не прошёл проверку.")
    contract = get("/openapi.yaml").decode("utf-8")
    if "/api/tickets" not in contract or "/api/reports/summary" not in contract:
        raise ValueError("Контракт OpenAPI недоступен.")
    return {"readiness": "UP", "categories": len(categories), "tickets": tickets["totalElements"],
            "reportTotalCreated": report["totalCreated"], "openApi": "passed"}
