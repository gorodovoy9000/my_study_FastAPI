from datetime import date, timedelta
from fastapi.openapi.models import Example


# booking date examples
start_date_examples = {
    "today": Example(summary="Today", value=date.today()),
    "tomorrow": Example(summary="Tomorrow", value=date.today() + timedelta(days=1)),
}
end_date_examples = {
    "tomorrow": Example(summary="Tomorrow", value=date.today() + timedelta(days=1)),
    "next_5_days": Example(summary="Next 5 days", value=date.today() + timedelta(days=5)),
    "next_7_days": Example(summary="Next 7 days", value=date.today() + timedelta(days=7)),
    "next_10_days": Example(summary="Next 10 days", value=date.today() + timedelta(days=10)),
}
