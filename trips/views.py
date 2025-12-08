from django.urls import reverse_lazy
from django.views import generic
from .models import Trip
from .forms import TripForm

from django.shortcuts import redirect, render, get_object_or_404
from .forms import BookingForm
from .models import Booking
from .mpesa import MpesaService


class TripListView(generic.ListView):
    model = Trip
    template_name = 'trips/list.html'
    context_object_name = 'trips'


class TripDetailView(generic.DetailView):
    model = Trip
    template_name = 'trips/detail.html'


class TripCreateView(generic.CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'trips/form.html'
    success_url = reverse_lazy('trips:list')


class TripUpdateView(generic.UpdateView):
    model = Trip
    form_class = TripForm
    template_name = 'trips/form.html'
    success_url = reverse_lazy('trips:list')


class TripDeleteView(generic.DeleteView):
    model = Trip
    template_name = 'trips/confirm_delete.html'
    success_url = reverse_lazy('trips:list')


class BookingCreateView(generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'trips/booking_form.html'

    def get_initial(self):
        initial = super().get_initial()
        trip_pk = self.request.GET.get('trip')
        if trip_pk:
            try:
                initial['trip'] = Trip.objects.get(pk=trip_pk)
            except Trip.DoesNotExist:
                pass
        return initial

    def get_success_url(self):
        return reverse_lazy('trips:payment', kwargs={'pk': self.object.pk})


def payment_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    mpesa = MpesaService()
    context = {'booking': booking, 'mpesa_configured': mpesa.is_configured()}
    if request.method == 'POST':
        # Initiate STK Push (simulated if not configured)
        amount = booking.trip.price
        phone = booking.phone
        account_ref = f'BOOKING-{booking.pk}'
        res = mpesa.stk_push(phone, float(amount), account_ref, f'Payment for booking {booking.pk}')
        # store checkout id if present
        booking.mpesa_checkout_id = res.get('checkout_id')
        booking.save()
        # If simulated, immediately mark as paid for convenience
        if res.get('status') in ('simulated', 'initiated') and not mpesa.is_configured():
            booking.paid = True
            booking.save()
            return redirect('trips:payment_success', pk=booking.pk)
        context['response'] = res
    return render(request, 'trips/payment.html', context)


def payment_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # In real flow, payment confirmation would come from MPESA callback/webhook
    booking.paid = True
    booking.save()
    return render(request, 'trips/payment_success.html', {'booking': booking})
from django.urls import reverse_lazy
from django.views import generic
from .models import Trip
from .forms import TripForm

from django.shortcuts import redirect, render, get_object_or_404
from .forms import BookingForm
from .models import Booking
from .mpesa import MpesaService


class TripListView(generic.ListView):
    model = Trip
    template_name = 'trips/list.html'
    context_object_name = 'trips'


class TripDetailView(generic.DetailView):
    model = Trip
    template_name = 'trips/detail.html'


class TripCreateView(generic.CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'trips/form.html'
    success_url = reverse_lazy('trips:list')


class TripUpdateView(generic.UpdateView):
    model = Trip
    form_class = TripForm
    template_name = 'trips/form.html'
    success_url = reverse_lazy('trips:list')


class TripDeleteView(generic.DeleteView):
    model = Trip
    template_name = 'trips/confirm_delete.html'
    success_url = reverse_lazy('trips:list')


class BookingCreateView(generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'trips/booking_form.html'

    def get_initial(self):
        initial = super().get_initial()
        trip_pk = self.request.GET.get('trip')
        if trip_pk:
            try:
                initial['trip'] = Trip.objects.get(pk=trip_pk)
            except Trip.DoesNotExist:
                pass
        return initial

    def get_success_url(self):
        return reverse_lazy('trips:payment', kwargs={'pk': self.object.pk})


def payment_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    mpesa = MpesaService()
    context = {'booking': booking, 'mpesa_configured': mpesa.is_configured()}
    if request.method == 'POST':
        # Initiate STK Push (simulated if not configured)
        amount = booking.trip.price
        phone = booking.phone
        account_ref = f'BOOKING-{booking.pk}'
        res = mpesa.stk_push(phone, float(amount), account_ref, f'Payment for booking {booking.pk}')
        # store checkout id if present
        booking.mpesa_checkout_id = res.get('checkout_id')
        booking.save()
        # If simulated, immediately mark as paid for convenience
        if res.get('status') in ('simulated', 'initiated') and not mpesa.is_configured():
            booking.paid = True
            booking.save()
            return redirect('trips:payment_success', pk=booking.pk)
        context['response'] = res
    return render(request, 'trips/payment.html', context)


def payment_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # In real flow, payment confirmation would come from MPESA callback/webhook
    booking.paid = True
    booking.save()
    return render(request, 'trips/payment_success.html', {'booking': booking})
