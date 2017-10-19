
from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.MapView.as_view(), name="map"),
    url(r'^events/$', views.EventsView.as_view(), name="events"),
    url(r'^profile/$', views.ProfileView.as_view(), name="profile")
]
