from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['POST'])
def incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        account = Account.objects.get(app_secret_token=token)
    except Account.DoesNotExist:
        return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    if request.method == 'GET' and not isinstance(data, dict):
        return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
    destinations = account.destinations.all()
    for destination in destinations:
        headers = destination.headers
        url = destination.url
        method = destination.http_method.lower()

        if method == 'get':
            response = requests.get(url, headers=headers, params=data)
        elif method == 'post':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'put':
            response = requests.put(url, headers=headers, json=data)
        
        # Log or handle response if necessary

    return Response({"message": "Data processed"}, status=status.HTTP_200_OK)
