from rest_framework.response import Response
from rest_framework import status


def exception_handling(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Response({
                'data': {},
                'message': e.__str__(),
                'status': False
            }, status = status.HTTP_400_BAD_REQUEST)
    return wrapper
