from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
path('', views.index, name="ShopHome"),
path('', lambda request: redirect('shop/')),
path('shop/', include('shop.urls')),
path('about/', views.about, name="AboutUs"),
path('contact/', views.contact_view, name="contact Us"),
path('tracker/', views.tracker, name="trackerForm"),
path('search/', views.search, name="Search"),
path('products/<int:my_id>', views.productview, name="Productview"),
path('cheekout/', views.cheekout, name="cheekout"),
path('handlerequest/', views.handlerequest, name="handlerequest")

]
