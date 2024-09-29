from django.contrib import admin
from .models import Profile, ValidEntry

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'brother_letters')

@admin.register(ValidEntry)
class ValidEntryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'brother_letters')
    search_fields = ('first_name', 'last_name', 'phone_number', 'brother_letters')
