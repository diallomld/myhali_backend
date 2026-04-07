from django.contrib import admin
from .models import *

# Register your models here.
# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'created_at')
#     list_filter = ('id', 'first_name', 'last_name', 'created_at')
#     list_editable = ('first_name', 'last_name')
#     search_fields = ('first_name', 'last_name')
#     list_per_page = 10


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'region', 'city',
                    'generated_code', 'created_at')
    list_filter = ('id', 'country', 'region', 'city')
    search_fields = ('country', 'region', 'city', 'generated_code')
    list_per_page = 10


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'uri', 'recording_date')
    search_fields = ('id', 'uri')
    list_per_page = 10
