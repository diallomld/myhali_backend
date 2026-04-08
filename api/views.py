from rest_framework import generics
from rest_framework.decorators import api_view
import numpy as np
import requests
from operator import itemgetter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from api.serializers import *
from api.letters import *

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Register API
@method_decorator(csrf_exempt, name='dispatch')
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        true_password = make_password(data.pop("password"))
        data["password"] = true_password
        data["username"] = request.data.get("username", "")
        data["first_name"] = request.data.get("first_name", "")
        data["last_name"] = request.data.get("last_name", "")
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            }
        )


@api_view(["GET"])
def isLocation_coded(request):
    """Check if the location is coded or not and return the code if True.

    Parameter:
    location (str): A specific location or position.

    Returns:
    Response: a bool variable whether the location is already in our database or not.
    """
    try:
        location = request.GET.get("location")
        user_id = request.GET.get("userId", "")

        address = (
            Address.objects.get(location_name=location, users__id__exact=user_id)
            if user_id
            else Address.objects.get(location_name=location)
        )
        generated_code = address.generated_code
        return Response({"isLocation_exists": True, "code": generated_code})
    except Address.DoesNotExist:
        return Response({"isLocation_exists": False})


@api_view(["POST"])
def save_code(request):
    """Persist a code in the database.

    Parameter:
    address (object): A complete address object.

    Returns:
    Response: The persisted address with status code 201 or if an error occurs, status code 400.
    """
    data = JSONParser().parse(request)
    if not data.get("users_id"):
        data.pop("users_id")
    if data.get("uri", ""):
        serializer = AudioSerializer(data=data)
    else:
        serializer = AddressSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def get_code(request):
    """Retrieve a code and the audio (optionnal) in the database.

    Parameter:
    code (str): The code corresponding to the position we are looking for.

    Returns:
    Response: the latitude, the longitude of the position and the uri of the audio (if the code is retrieved).
    """
    try:
        code = request.GET.get("code")
        address = Address.objects.get(generated_code=code)
        latitude = address.latitude
        longitude = address.longitude
        audio = Audio.objects.filter(address=address)
        if audio:
            audio_uri = audio.last().uri
        else:
            audio_uri = None
        return Response(
            {"latitude": latitude, "longitude": longitude, "uri": audio_uri}
        )
    except Address.DoesNotExist:
        return Response({"latitude": None, "longitude": None})


@api_view(["GET"])
def get_my_addresses(request):
    user_id = request.GET.get("userId")
    if not user_id:
        return Response({"addresses": None})
    addresses = Address.objects.filter(users__id__exact=int(user_id))

    return Response({"addresses": addresses.values()})


@api_view(["GET"])
def generate_code(request):
    """Generate a code associated to a position.

    Parameters:
    latitude (float): The position's latitude.
    longitude (float): The position's longitude.

    Returns:
    Response: The code generated.
    """
    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")
    reverse = reverseGeocode(latitude, longitude)
    try:
        address_details = reverse.get("address", "")
        address_name = reverse.get("display_name", "")
        address_type = reverse.get("type", "")
        boundingbox = reverse.get("boundingbox", "")
        address = Address.objects.filter(location_name=address_name).last()

        if address:
            generated_code = address.generated_code
            return Response(generated_code, status=201)

        region, city, road = format_address(address_details)
        query = ""

        if road:
            query = region + "," + city + "," + road
        else:
            query = region + "," + city
        district_infos = get_district(query)[0]
        boundingbox_district = district_infos.get("boundingbox", "")
        print("Boundingbox DIstrict", boundingbox_district)
        region_code = format_code(region)
        city_code = format_code(city)
        extra_number = get_extra_number(boundingbox, boundingbox_district)

        if road:
            road_code = format_code(road)
            final_code = (
                region_code + "-" + city_code + "-" + road_code + "-" + extra_number
            )
        else:
            final_code = region_code + "-" + city_code + "-" + extra_number
        return Response({"code": final_code.upper()})
    except:
        raise ("No address found !")


def get_district(query):
    """Get the bounding box of a district of the position.

    Parameters:
    query (str): une localité sous la forme région, ville, commune ou arrondissement ou rue.

    Returns:
    Response: Les bordures correspondant à la commune ou arrondissement ou rue.
    """
    PARAMS = {"q": query, "format": "jsonv2", "countrycodes": "sn"}
    response = requests.get("https://nominatim.openstreetmap.org/search", params=PARAMS)
    boundingbox_district = response.json()
    return boundingbox_district


def reverseGeocode(latitude, longitude):
    """Retrieve a locality based on his geographical coordinates.

    Parameters:
    latitude (float): The position's latitude.
    longitude (float): The position's longitude.

    Returns:
    Response: The locality details.
    """
    PARAMS = {
        "lat": latitude,
        "lon": longitude,
        "email": "ibrahimabiram@gmail.com",
        "format": "jsonv2",
        "addressdetails": 1,
    }
    HEADERS = {"User-Agent": "myhalibackend"}
    response = requests.get(
        "https://nominatim.openstreetmap.org/reverse", params=PARAMS, headers=HEADERS
    )

    if response.status_code == 200:
        return response.json()
    return None


def format_code(text):
    """Format a given string to the requirements of the app.

    Parameters:
    text (float): Text to be formatted.

    Returns:
    Response: The formatted text.
    """
    new_code = ""
    if text.find("(") != -1:
        text = text.split("(")
        text = text[0].replace("(", "")

    if len(text.split(" ")) != 1 or len(text.split("-")) != 1:
        if text.find(" ") != -1:
            res = text.split(" ")
            char_tab = [item.strip()[0] for item in res]
            new_code = "".join(char_tab)
        if text.find("-") != -1:
            if len(text) < 6:
                text = text.replace("-", "")
                new_code = text
            else:
                res = text.split("-")
                char_tab = [item.strip()[0] for item in res]
                new_code = "".join(char_tab)
    else:
        new_code = text[:3]

    return new_code


def format_address(address_details):
    """Format address.

    Parameters:
    address_details (list): The position's address details.

    Returns:
    Response: The region, the city and the commune or street or district.
    """
    region = address_details.get("state", "")
    region_bis = address_details.get("region", "")
    county = address_details.get("county", "")
    city = address_details.get("city", "")
    locality = address_details.get("locality", "")
    town = address_details.get("town", "")
    suburb = address_details.get("suburb", "")
    road = address_details.get("road", "")
    street = address_details.get("street", "")
    district = address_details.get("district", "")
    hamlet = address_details.get("hamlet", "")
    village = address_details.get("village", "")

    if not region:
        if region_bis:
            region = region_bis
        else:
            region = city

    if not city:
        if county:
            city = county
        elif town:
            city = town
        elif locality:
            city = locality
        else:
            city = village

    if not suburb:
        if road:
            suburb = road
        elif not road and street:
            suburb = district
        else:
            suburb = district

    if not road:
        if street:
            road = street
        elif not street and district:
            road = district
        elif not district and suburb:
            road = suburb
        else:
            road = hamlet

    return region, city, road


def get_extra_number(boundingbox, boundingbox_road):
    """Get an extra number tha we calculate based on the position.

    Parameters:
    boundingbox (list): The specific point bounding box for a margin error.
    boundingbox_road (list): The district or street bounding box.

    Returns:
    Response: An extra number.
    """
    lat_step = 0.0001
    long_step = 0.0002
    unit_of_change = 5000

    code = ""
    house_position = 0
    boundingbox_road = [float(item) for item in boundingbox_road]
    boundingbox = [float(item) for item in boundingbox]
    lat_min, lat_max, long_min, long_max = boundingbox_road

    # i = lat_min
    # while i <= lat_max:
    for i in np.arange(lat_min, lat_max, lat_step):
        if i >= boundingbox[1]:
            break
        else:
            # y = long_min
            for y in np.arange(long_min, long_max, long_step):
                house_position += 1
                # y += long_step
                if y >= boundingbox[3]:
                    break
            # i += lat_step

    if house_position < unit_of_change:
        code = str(house_position) + "A"
    else:
        for key in letters:
            if house_position < letters[key] * unit_of_change:
                numericPart = house_position - (
                    ((letters[key] - 1) * unit_of_change) - 1
                )
                code = str(numericPart) + key
                break

    if code == None:
        code = "1A"
    return code
