from django.conf.urls import url, include
from rest_framework import routers
from backend import event_holiday_APICall
from backend import views as calendar_views
from amenities import views as amenity_views
from parallel_coord_plot import views as parallel_views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'testCreateTable/$', event_holiday_APICall.createHolidayEventTable),
    url(r'testloadholiday/(?P<city>\w+)/$', event_holiday_APICall.loadHolidays),
    url(r'testloadevent/(?P<city>\w+)/$', event_holiday_APICall.loadEvents),
    url(r'testholidayevent/(?P<city>\w+)/(?P<date>\d+)/$', event_holiday_APICall.HolidayEvent),
    # url(r'', views.Home),
    url(r'summaries/daily/(?P<city>\w+)/$', calendar_views.CalendarSummary),
    url(r'review/comments/(?P<city>\w+)/$', calendar_views.CityReviews),
    url(r'amenities/$', amenity_views.AmenityData),
    url(r'up/$', calendar_views.Uptime),
    url(r'parallelcoord/$', parallel_views.ParallelCoordData),
]
