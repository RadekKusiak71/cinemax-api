from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidBookingStatusError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The booking status is invalid for this operation."
    default_code = "invalid_booking_status"