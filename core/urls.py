from django.conf.urls import url, include

from . import views

app_name = 'core'
urlpatterns = [
    url('^$', views.login),
    url(r'^map/$', views.MapView.as_view(), name="map"),
    url(r'^events/$', views.EventsView.as_view(), name="events"),
    url(r'^events/(?P<event_id>[0-9]+)/join$', views.EventJoinView.as_view(), name="event_join"),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventView.as_view(), name="event"),
    url(r'^profile/$', views.ProfileView.as_view(), name="profile"),
    # url(r'^', include('django.contrib.auth.urls', namespace='auth')),
    # url(r'^', include('social_django.urls', namespace='social'))
]
