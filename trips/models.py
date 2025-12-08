from django.db import models


class Trip(models.Model):
    title = models.CharField(max_length=200)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    depart_time = models.DateTimeField()
    seats = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.title} — {self.origin} → {self.destination}"


class Booking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    id_number = models.CharField(max_length=100)
    has_luggage = models.BooleanField(default=False)
    luggage_weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    paid = models.BooleanField(default=False)
    mpesa_checkout_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.pk} — {self.name} for {self.trip}"
