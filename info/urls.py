from django.conf.urls import url
from . import views

app_name = 'info'

urlpatterns = [
    url(r'^$', views.archieve, name='info'),

]