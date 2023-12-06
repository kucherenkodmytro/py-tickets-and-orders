from django.db import transaction
from django.db.models.query import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    order = Order.objects.create(
        user=User.objects.get(username=username)
    )
    if date is not None:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        row = ticket_data["row"]
        seat = ticket_data["seat"]
        movie_session_id = ticket_data["movie_session"]

        Ticket.objects.create(
            order=order,
            row=row,
            seat=seat,
            movie_session_id=movie_session_id
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset