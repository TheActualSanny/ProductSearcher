import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .ecommerce_apis.search_initiator import get_searcher

class InitiateLookup(APIView):
    '''
        This endpoint will initiate the actual lookup methods
        to return the product data.
    '''
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message' : 'Welcome, please pass a product that you wish to search for.'})

    def post(self, request):
        product = request.data.get('product')
        if not product:
            return Response({'message' : 'Make sure to pass a product!'})
        manager = get_searcher()
        products = manager.start_searching(product_input = product)

        return JsonResponse({'message' : 'Successfully fetched products!', **products})

