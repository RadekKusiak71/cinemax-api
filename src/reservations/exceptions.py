from rest_framework.exceptions import APIException


class InvalidReservationStatusException(APIException):
    status_code = 400
    default_detail = "The reservation status is invalid for this operation."
    default_code = "invalid_reservation_status"

class ExistingPendingReservationException(APIException):
    status_code = 400
    default_detail = "A pending reservation already exists for this user and showing."
    default_code = "existing_pending_reservation"

class MaxSeatsPerReservationExceededException(APIException):
    status_code = 400
    default_detail = "The maximum number of seats per reservation has been exceeded."
    default_code = "max_seats_per_reservation_exceeded"

class SeatDoesNotExistException(APIException):
    status_code = 404
    default_detail = "One or more of the selected seats do not exist for this showing."
    default_code = "seat_does_not_exist"

class SeatsAlreadyBookedException(APIException):
    status_code = 400
    default_detail = "One or more of the selected seats are already booked."
    default_code = "seats_already_booked"