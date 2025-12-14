from rest_framework.views import exception_handler
import sys
import traceback

def custom_exception_handler(exc, context):
    """
    Safe global exception handler compatible with Python 3.11 frozen exceptions.
    """
    # Call default handler first
    response = exception_handler(exc, context)

    # If DRF handled it, return as-is
    if response is not None:
        return response

    # Otherwise, build a safe manual response
    exc_type, _, tb = sys.exc_info()
    safe_data = {
        "error": str(exc),
        "exception_type": exc_type.__name__ if exc_type else None,
        "detail": "Unhandled server error. See logs for traceback."
    }

    # Print traceback for debugging (won’t crash)
    print("\n❌ Unhandled exception caught globally:")
    traceback.print_exc()

    del tb
    from rest_framework.response import Response
    from rest_framework import status

    return Response(safe_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
