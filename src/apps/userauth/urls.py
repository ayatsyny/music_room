from django.conf.urls import url
from apps.userauth.views import ListCourse

app_name = 'userauth'

urlpatterns = [
    url(r'^$', ListCourse.as_view(), name='course_list'),
]
