from django.contrib import admin
from .models import User, Course, Review

admin.site.register(User, admin.ModelAdmin)
admin.site.register(Course)
admin.site.register(Review)
