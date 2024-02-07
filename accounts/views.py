from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class IndexView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
