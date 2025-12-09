from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import BookingForm
from .models import Booking


def home_view(request):
    """Render the landing page."""
    return render(request, 'home.html')


class BookingCreateView(generic.CreateView):
    """Create a booking with route selection, passenger details, and luggage info."""
    model = Booking
    form_class = BookingForm
    template_name = 'trips/booking_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # expose route prices and luggage settings to the template for live calculation
        ctx['route_prices'] = Booking.ROUTE_PRICES
        ctx['luggage_free_kg'] = getattr(settings, 'LUGGAGE_FREE_KG', 7)
        ctx['luggage_fee_per_kg'] = getattr(settings, 'LUGGAGE_FEE_PER_KG', 100)
        return ctx

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill route from GET parameter if provided
        route = self.request.GET.get('route')
        if route:
            initial['route'] = route
        return initial

    def get_success_url(self):
        """Redirect to success page with booking id after successful save."""
        return reverse_lazy('trips:home_success', kwargs={'booking_id': self.object.pk})

    def form_valid(self, form):
        """Ensure computed fields (price, luggage_fee) are set on the instance before saving."""
        instance = form.instance
        # set price from chosen route if not already set
        if not getattr(instance, 'price', None):
            route = form.cleaned_data.get('route')
            if route:
                instance.price = Booking.ROUTE_PRICES.get(route, 0)
        # ensure luggage_fee exists
        if not hasattr(instance, 'luggage_fee') or instance.luggage_fee is None:
            weight = form.cleaned_data.get('luggage_weight')
            free_kg = getattr(settings, 'LUGGAGE_FREE_KG', 7)
            per_kg = getattr(settings, 'LUGGAGE_FEE_PER_KG', 100)
            if weight and weight > free_kg:
                instance.luggage_fee = round((float(weight) - float(free_kg)) * float(per_kg), 2)
            else:
                instance.luggage_fee = 0
        # Call parent form_valid to save the instance
        return super().form_valid(form)


def home_success_view(request, booking_id):
    """Render home page with success notification."""
    context = {'booking_id': booking_id, 'success': True}
    return render(request, 'home.html', context)
