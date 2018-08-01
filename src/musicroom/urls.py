from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from .views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/courses/', include('apps.userauth.urls', namespace='courses')),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^social-auth/', include('social_django.urls', namespace='social_auth')),
    url(r'^$', home, name='home'),
]
