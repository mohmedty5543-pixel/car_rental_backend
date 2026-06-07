from rest_framework.exceptions import APIException
from rest_framework import status

class DomainError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Domain rule violation.'
    default_code = 'domain_error'

class OverlapError(DomainError):
    default_detail = 'Vehicle is not available for the requested period.'
    default_code = 'overlap'

class InvalidTransition(DomainError):
    default_detail = 'Invalid state transition.'
    default_code = 'invalid_transition'
