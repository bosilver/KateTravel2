from django.contrib import admin
from booking.models import Activity, Company, Location, TimeTable
# Register your models here.

admin.site.register(Location)
admin.site.register(Company)
admin.site.register(Activity)
admin.site.register(TimeTable)
