from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.TripListView.as_view(), name='list'),
    path('trip/add/', views.TripCreateView.as_view(), name='add'),
    path('trip/<int:pk>/', views.TripDetailView.as_view(), name='detail'),
    path('trip/<int:pk>/edit/', views.TripUpdateView.as_view(), name='edit'),
    path('trip/<int:pk>/delete/', views.TripDeleteView.as_view(), name='delete'),
    path('booking/add/', views.BookingCreateView.as_view(), name='booking_add'),
    path('booking/<int:pk>/payment/', views.payment_view, name='payment'),
    path('booking/<int:pk>/success/', views.payment_success, name='payment_success'),
]
