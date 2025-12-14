import logging

import stripe
from stripe.checkout import Session

from payments.exceptions import InvalidBookingStatusError
from reservations.models import Reservation, ReservationStatus

logger = logging.getLogger(__name__)

def create_checkout(reservation: Reservation) -> Session:
    if reservation.status != ReservationStatus.PENDING:
        raise InvalidBookingStatusError(
            f"Cannot checkout reservation {reservation.id}: Status is {reservation.status}"
        )

    unit_amount: int = int(round(float(reservation.full_price) * 100))

    try:
        session: Session = stripe.checkout.Session.create(
            success_url=(
                f"cinemax://payment-return"
                f"?status=success"
                f"&session_id={{CHECKOUT_SESSION_ID}}"
                f"&reservation_id={reservation.id}"
            ),
            cancel_url=(
                f"cinemax://payment-return"
                f"?status=cancel"
                f"&reservation_id={reservation.id}"
            ),
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
