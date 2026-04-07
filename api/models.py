from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=30, default="Senegal")
    region = models.CharField(max_length=30, default="Dakar")  # or state
    city = models.CharField(max_length=30)
    suburb = models.CharField(max_length=60, null=True, blank=True)  # commune
    location_name = models.CharField(max_length=100, default="Dakar, Senegal")
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    generated_code = models.CharField(max_length=30, default="SN-DAK", unique=True)
    users = models.ManyToManyField(User, related_name="user_adresses", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.generated_code

    def get_address_users(self):
        return User.objects.filter(user_adresses__id__exact=self.id)

    class Meta:
        ordering = ["created_at"]


class Audio(models.Model):
    uri = models.CharField(max_length=200)
    recording_date = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="user_audios", blank=True)
    address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.uri

    class Meta:
        ordering = ["recording_date"]
