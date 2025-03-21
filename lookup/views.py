import json
from django.core.cache import cache
from django.http import JsonResponse
from .utils import get_cache, set_cache
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
        min_price = request.data.get('min')
        max_price = request.data.get('max')
        product = request.data.get('product')
        if not product:
            return Response({'message' : 'Make sure to pass a product!'})
        if min_price and max_price and min_price > max_price:
            return Response({'message' : 'Please input a valid price range.'})
        cached = None
        cached = get_cache(product, min_price, max_price)
        message = {'message' : 'Successfully fetched products!'} 
        if not cached:
            manager = get_searcher(product = product)
            products = manager.start_searching(product_input = product, min_value = min_price,
                                            max_value = max_price)   
            set_cache(product, min_price, max_price, products = products) 
            return JsonResponse({**message, **products})
        else:
            return JsonResponse({**message, **cached})
