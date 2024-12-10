from django.contrib import admin
from booking.models import *

# Register your models here.
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Schedule)
admin.site.register(Seat)
admin.site.register(booking_history)

