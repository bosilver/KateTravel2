from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'KateTravel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^booking/$', 'booking.views.activity_booking_page'),
    url(r'^get/activities/$', 'booking.views.get_activities'),
    url(r'^get/timetable/$', 'booking.views.get_time_table'),
    url(r'^get/activity/$', 'booking.views.get_activity'),
    url(r'^post/booking/$', 'booking.views.receive_booking')
)
