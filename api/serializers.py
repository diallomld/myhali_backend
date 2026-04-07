from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
        }

        def create(self, validated_data):
            user = User.objects.create_user(
                validated_data["username"],
                password=make_password(validated_data["password"]),
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
            )
            return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AudioSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True, required=False)
    users_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, many=True, required=False
    )
    country = serializers.CharField(source="address.country")
    region = serializers.CharField(source="address.region")
    city = serializers.CharField(source="address.city")
    suburb = serializers.CharField(source="address.suburb")
    location_name = serializers.CharField(source="address.location_name")
    latitude = serializers.CharField(source="address.latitude")
    longitude = serializers.CharField(source="address.longitude")
    generated_code = serializers.CharField(source="address.generated_code")

    class Meta:
        model = Audio
        fields = (
            "pk",
            "uri",
            "duration",
            "country",
            "region",
            "city",
            "suburb",
            "location_name",
            "latitude",
            "longitude",
            "generated_code",
            "users",
            "users_id",
        )

    def create(self, validated_data):
        addr = validated_data.get("address", "")
        uri = validated_data.get("uri", "")
        duration = validated_data.get("duration", "")

        country = addr["country"]
        region = addr["region"]
        city = addr["city"]
        suburb = addr["suburb"]
        location_name = addr["location_name"]
        latitude = addr["latitude"]
        longitude = addr["longitude"]
        generated_code = addr["generated_code"]

        if validated_data.get("users_id", ""):
            users = validated_data.pop("users_id")
            address = Address.objects.create(
                country=country,
                region=region,
                city=city,
                suburb=suburb,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
                generated_code=generated_code,
            )
            for user in users:
                address.users.add(user)
            audio = Audio.objects.create(uri=uri, duration=duration, address=address)
            for user in users:
                audio.users.add(user)
        else:
            address = Address.objects.create(
                country=country,
                region=region,
                city=city,
                suburb=suburb,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
                generated_code=generated_code,
            )
            audio = Audio.objects.create(uri=uri, duration=duration, address=address)

        return audio


class AddressSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True, required=False)
    users_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, many=True, required=False
    )

    class Meta:
        model = Address
        fields = (
            "pk",
            "country",
            "region",
            "city",
            "suburb",
            "location_name",
            "latitude",
            "longitude",
            "generated_code",
            "users",
            "users_id",
        )

    def create(self, validated_data):
        if validated_data.get("users_id"):
            users = validated_data.pop("users_id")
            address = Address.objects.create(**validated_data)
            for user in users:
                address.users.add(user)
        else:
            address = Address.objects.create(**validated_data)
        return address
