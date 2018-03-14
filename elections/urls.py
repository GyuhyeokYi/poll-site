from django.conf.urls import url
from . import views


urlpatterns = [    
    url(r'^$', views.index, name='home'),
   	url(r'^areas/(?P<area>[가-힣]+)/$', views.areas),
   	url(r'^areas/(?P<area>[가-힣]+)/results$', views.results, name='results'),
   	url(r'^polls/(?P<poll_id>\d+)/$', views.polls, name='polls'),
   	url(r'^candidates/(?P<name>.+)/$', views.candidates, name='candidates'),
]
