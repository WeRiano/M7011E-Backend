from django.core.files import File
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
import base64
from rest_framework import status
import os
import re

from backend.settings import MEDIA_ROOT
from .models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = json.loads(request.body)
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    address = data['address']
    city = data['city']
    zip_code = data['zip_code']

    response = {}
    error = False

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(email_regex, email):
        response["email"] = "Enter a valid email address."
        error = True
    try:
        if int(zip_code) < 10000 or int(zip_code) >= 90000:
            response["zip_code"] = "Enter a valid zipcode, an integer on the interval [10000, 99000)."
            error = True
    except ValueError:
        response["zip_code"] = "A valid integer is required."
        error = True
    if len(email) > User.EMAIL_MAX_LENGTH:
        response["email"] = "Enter a valid email address length (not more than " + str(User.EMAIL_MAX_LENGTH) + " characters)."
        error = True
    if len(first_name) > User.FIRST_NAME_MAX_LENGTH:
        response["first_name"] = "Enter a valid first name length (not more than " + str(User.FIRST_NAME_MAX_LENGTH) + " characters)."
        error = True
    if len(last_name) > User.LAST_NAME_MAX_LENGTH:
        response["last_name"] = "Enter a valid last name length (not more than " + str(User.LAST_NAME_MAX_LENGTH) + " characters)."
        error = True
    if len(address) > User.ADDRESS_MAX_LENGTH:
        response["address"] = "Enter a valid address length (not more than " + str(User.ADDRESS_MAX_LENGTH) + " characters)."
        error = True
    if len(city) > User.CITY_MAX_LENGTH:
        response["city"] = "Enter a valid city length (not more than " + str(User.CITY_MAX_LENGTH) + " characters)."
        error = True

    if error:
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.address = address
    user.city = city
    user.zip_code = zip_code
    user.save()

    response = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'city': city,
        'zip_code': zip_code,
    }

    return Response(data=response, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    result = {
        'id': request.user.id,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'address': request.user.address,
        'city': request.user.city,
        'zip_code': request.user.zip_code
    }
    return Response(data=result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    os.getcwd()
    os.listdir() 

    response = {
        "user_id": request.user.id
    }
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def set_house_img(request):
    data = json.loads(request.body)
    enc_img = data['file']
    img_type = data['type']
    img_data = base64.b64decode(enc_img)

    old_file_path = MEDIA_ROOT + '/' + str(request.user.house_img)

    # FOR SOME REASON DJANGO DOESNT OVERWRITE EXISTING FILES
    # hence this is not actually the real new file name.
    # The real file name is new_file_name + some hash! Thanks django!
    new_file_name = str(request.user.id) + '_prof_pic.' + img_type
    new_file_path = MEDIA_ROOT + '/' + new_file_name

    # We create a temporary file so we can write data (given by the frontend) to it
    file_write = File(open(new_file_path, 'wb'))
    file_write.write(img_data)
    file_write.close()

    # Save the new file to the database. Again: HASH IS ADDED TO THE NAME!
    request.user.house_img.save(new_file_name, File(open(new_file_path, 'rb')))
    request.user.save()

    # Delete the temporary file
    os.remove(new_file_path)

    # We also delete the old file as long as its not the static default picture
    if old_file_path != MEDIA_ROOT + '/' + 'default_prof_pic.jpeg':
        os.remove(old_file_path)
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_house_img(request):
    file = request.user.house_img
    img_type = file.name.split('.')[1]
    img = open(MEDIA_ROOT + '/' + file.name, 'rb')
    return FileResponse(img, content_type='image/' + img_type)
