import logging
from urllib.parse import urlencode

import stripe
from django.conf import settings
from payments.exceptions import InvalidBookingStatusError
from reservations.models import Reservation, ReservationStatus
from stripe.checkout import Session

logger = logging.getLogger(__name__)

def create_checkout(reservation: Reservation) -> Session:
    if reservation.status != ReservationStatus.PENDING:
        raise InvalidBookingStatusError(
            f"Cannot checkout reservation {reservation.id}: Status is {reservation.status}"
        )

    unit_amount: int = int(round(float(reservation.full_price) * 100))

    success_base = settings.STRIPE_SUCCESS_URL_BASE
    cancel_base = settings.STRIPE_CANCEL_URL_BASE

    success_qs = urlencode(
        {
            "status": "success",
            "session_id": "{CHECKOUT_SESSION_ID}",
            "reservation_id": reservation.id,
        },
        safe="{}",
    )
    
    cancel_qs = urlencode(
        {
            "status": "cancel",
            "reservation_id": reservation.id,
        }
    )

    try:
        session: Session = stripe.checkout.Session.create(
            success_url=f"{success_base}?{success_qs}",
            cancel_url=f"{cancel_base}?{cancel_qs}",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": f"Reservation #{reservation.id}",
                            "description": (
                                f"{reservation.showing.variant.movie.title} at "
                                f"{reservation.showing.start_time.isoformat()}"
                            ),
                        },
                        "unit_amount": unit_amount,
                    },
                    "quantity": 1,
                }
            ],
            metadata={"reservation_id": str(reservation.id)},
        )
    except stripe.error.StripeError as e:
        logger.exception(
            "Stripe error while creating checkout session for reservation %s: %s",
            reservation.id,
            e,
        )
        raise

    return session