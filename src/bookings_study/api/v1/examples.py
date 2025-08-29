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

# bookings example
booking_examples = {
    "book_on_1_day": Example(summary="Book On 1 Day", value={
        "room_id": 1,
        "date_from": date.today(),
        "date_to": date.today() + timedelta(days=1),
    }),
    "book_on_5_days": Example(summary="Book On 5 Days", value={
        "room_id": 1,
        "date_from": date.today(),
        "date_to": date.today() + timedelta(days=5),
    }),
    "book_on_7_days": Example(summary="Book On 7 Days", value={
        "room_id": 1,
        "date_from": date.today(),
        "date_to": date.today() + timedelta(days=7),
    }),
}

# hotels examples
hotels_examples = {
    "red_star": Example(summary="Red Star", value={"title": "red_star", "location": "Moscow"}),
    "golden": Example(summary="Golden", value={"title": "golden", "location": "Dubai"})
}

# rooms examples
rooms_examples = {
    "standard1": Example(summary="Standard 1", value={
        "hotel_id": 1,
        "title": "standard1",
        "description": "Standard for 1 lone wolf",
        "price": 4000,
        "quantity": 8,
        "facilities_ids": [1],
    }),
    "standard2": Example(summary="Standard 2", value={
        "hotel_id": 1,
        "title": "standard2",
        "description": "Standard for 2 people",
        "price": 4500,
        "quantity": 8,
        "facilities_ids": [1],
    }),
    "lux": Example(summary="Luxury", value={
        "hotel_id": 1,
        "title": "luxury",
        "description": "Luxury number",
        "price": 6500,
        "quantity": 4,
        "facilities_ids": [1],
    })
}

# facilities examples
facilities_examples = {
    "wi-fi": Example(summary="Wi-Fi", value={"title": "wi-fi"}),
    "tv": Example(summary="TV", value={"title": "tv"}),
    "minibar": Example(summary="Minibar", value={"title": "minibar"}),
}
