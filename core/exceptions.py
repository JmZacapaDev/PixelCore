from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        # For validation errors, DRF often returns a dictionary of fields.
        # We can flatten this or keep it as is, depending on desired format.
        # For now, let's just add the status code.
        response.data['status_code'] = response.status_code
    else:
        # Handle unexpected exceptions (e.g., 500 errors)
        # This is a generic fallback for unhandled exceptions
        if not isinstance(exc, Exception): # Ensure it's an actual exception
            return None # Let Django handle it if it's not an exception instance

        # Log the exception for debugging purposes
        import logging
        logger = logging.getLogger(__name__)
        logger.exception("An unhandled exception occurred: %s", exc)

        response = Response(
            {'detail': 'An unexpected error occurred.', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
