from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('<int:id>/remove/', views.remove, name='cart.remove'), # FIXME: this is not used
    path('orders/', views.orders, name='cart.orders'),
    path('checkout/', views.checkout, name='cart.checkout'),
]