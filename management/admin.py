from django.contrib import admin

from management.models import Parking, ParkingSpace, Reservation, Ticket
# Register your models here.

admin.site.register(Parking)
admin.site.register(ParkingSpace)
admin.site.register(Ticket)
admin.site.register(Reservation)