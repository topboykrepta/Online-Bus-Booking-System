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
        fields = ['trip', 'name', 'phone', 'id_number', 'has_luggage', 'luggage_weight']
        widgets = {
            'luggage_weight': forms.NumberInput(attrs={'step': '0.1'}),
        }

    def clean(self):
        cleaned = super().clean()
        has_luggage = cleaned.get('has_luggage')
        weight = cleaned.get('luggage_weight')
        if has_luggage and not weight:
            self.add_error('luggage_weight', 'Enter luggage weight')
        if not has_luggage:
            cleaned['luggage_weight'] = None
        return cleaned
from django import forms
from .models import Trip


class TripForm(forms.ModelForm):
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
            fields = ['trip', 'name', 'phone', 'id_number', 'has_luggage', 'luggage_weight']
            widgets = {
                'luggage_weight': forms.NumberInput(attrs={'step': '0.1'}),
            }

        def clean(self):
            cleaned = super().clean()
            has_luggage = cleaned.get('has_luggage')
            weight = cleaned.get('luggage_weight')
            if has_luggage and not weight:
                self.add_error('luggage_weight', 'Enter luggage weight')
            if not has_luggage:
                cleaned['luggage_weight'] = None
            return cleaned
