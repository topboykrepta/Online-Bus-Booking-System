from django import forms
from .models import Trip, Booking


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'origin', 'destination', 'depart_time', 'seats', 'price']
        widgets = {
            'depart_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # price and luggage_fee are computed server-side; user provides route and passenger info
        fields = ['route', 'name', 'phone', 'id_number', 'has_luggage', 'luggage_weight']
        widgets = {
            'luggage_weight': forms.NumberInput(attrs={'step': '0.1', 'min': '0'}),
            'route': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Number'}),
            'has_luggage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned = super().clean()
        # Set price based on selected route
        route = cleaned.get('route')
        if route:
            price_val = Booking.ROUTE_PRICES.get(route)
            if price_val is not None:
                # reflect on instance so view can save
                self.instance.price = price_val
        
        # Get luggage settings
        has_luggage = cleaned.get('has_luggage')
        weight = cleaned.get('luggage_weight')
        
        try:
            from django.conf import settings
            free_kg = getattr(settings, 'LUGGAGE_FREE_KG', 7)
            per_kg = getattr(settings, 'LUGGAGE_FEE_PER_KG', 100)
        except Exception:
            free_kg = 7
            per_kg = 100

        # Validate luggage weight
        if has_luggage:
            if not weight:
                self.add_error('luggage_weight', 'Enter luggage weight')
            else:
                # Calculate luggage fee for weight over free allowance
                luggage_fee = 0
                if float(weight) > free_kg:
                    extra = float(weight) - float(free_kg)
                    luggage_fee = round(extra * float(per_kg), 2)
                self.instance.luggage_fee = luggage_fee
        else:
            # No luggage selected
            cleaned['luggage_weight'] = None
            self.instance.luggage_fee = 0
        
        return cleaned

