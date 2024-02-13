from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'position']
    list_filter = ['position']

admin.site.register(Profile, ProfileAdmin)