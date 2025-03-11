from . import views
from django.urls import path

app_name = 'product_lookups'
urlpatterns = [
    path('search/', views.InitiateLookup.as_view(), name = 'search-product')
]