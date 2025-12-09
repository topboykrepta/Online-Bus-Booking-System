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
    # Trip is optional for direct route-based bookings from the landing page
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    id_number = models.CharField(max_length=100)
    has_luggage = models.BooleanField(default=False)
    luggage_weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Route choices and price stored on booking for later reference
    ROUTES = [
        ('NAI_MOM', 'Nairobi – Mombasa'),
        ('NAI_KIS', 'Nairobi – Kisumu'),
        ('NAI_MAL', 'Nairobi – Malindi'),
        ('MOM_NAI', 'Mombasa – Nairobi'),
        ('KIS_NAI', 'Kisumu – Nairobi'),
        ('MAL_NAI', 'Malindi – Nairobi'),
    ]

    ROUTE_PRICES = {
        'NAI_MOM': 2500,
        'NAI_KIS': 2000,
        'NAI_MAL': 2500,
        'MOM_NAI': 2500,
        'KIS_NAI': 2000,
        'MAL_NAI': 2500,
    }

    route = models.CharField(max_length=20, choices=ROUTES, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    luggage_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        trip_str = str(self.trip) if self.trip else self.route or 'No trip'
        return f"Booking #{self.pk} — {self.name} for {trip_str}"
