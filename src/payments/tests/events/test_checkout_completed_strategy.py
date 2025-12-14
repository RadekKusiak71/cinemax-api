import pytest

from payments.events import CheckoutCompletedStrategy
from payments.exceptions import InvalidBookingStatusError
from reservations.factories import ReservationFactory
from reservations.models import ReservationStatus

pytestmark = pytest.mark.django_db


def test_handle_success_confirms_booking(reservation_factory: ReservationFactory):
    reservation = reservation_factory(status=ReservationStatus.PENDING)

    strategy = CheckoutCompletedStrategy()
    event = {
        'id': 'evt_123',
        'data': {
            'object': {
                'id': 'cs_test_123',
                'metadata': {'reservation_id': str(reservation.id)}
            }
        }
    }

    strategy.handle(event)

    reservation.refresh_from_db()
    assert reservation.status == ReservationStatus.CONFIRMED


def test_handle_ignores_already_confirmed_booking(reservation_factory, caplog):
    reservation = reservation_factory(status=ReservationStatus.CONFIRMED)
    strategy = CheckoutCompletedStrategy()
    event = {
        'data': {'object': {'metadata': {'reservation_id': str(reservation.id)}}}
    }

    with pytest.raises(InvalidBookingStatusError):
        strategy.handle(event)

    reservation.refresh_from_db()
    assert reservation.status == ReservationStatus.CONFIRMED