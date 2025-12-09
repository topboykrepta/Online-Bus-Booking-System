from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('booking/add/', views.BookingCreateView.as_view(), name='booking_add'),
    path('success/<int:booking_id>/', views.home_success_view, name='home_success'),
]


