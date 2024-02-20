from django.shortcuts import render
from social_media_app.models import CustomUser, UserProfile
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from datetime import datetime
import os
from . import validate_user
from . import accessor


def get_user(request):
    if request.method == "GET":
        user = accessor.get_users()
        return JsonResponse({"status": 200, "message": user})
    return JsonResponse({"status": 400, "message": "Invalid request method"})

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message, status = validate_user.validate_create_data(data)
            return JsonResponse({"status": status, "message": message})
        except:
            return JsonResponse({"status":400,"message": "Error occurred"})
    return JsonResponse({"status": 400,"message": "Invalid request method"})


def get_user_by_id(request, id):
    if request.method == "GET":
        message, status = validate_user.validate_get_user_by_id(id)
        return JsonResponse({"status": status, "message": message})
    return JsonResponse({"status": 400,"message": "Invalid request method"})
 
@csrf_exempt   
def delete_user(request, id):
    if request.method == "DELETE":
        message, status = validate_user.validate_delete_user(id)
        return JsonResponse({"status": status, "message": message})
    return JsonResponse({"message": "Invalid request method"})
    
@csrf_exempt
def update_user(request, id):
    if request.method == "PUT":
        user = CustomUser.objects.filter(id = id).first()
        if user:
            try:               
                data = json.loads(request.body)
                message, status = validate_user.validate_update_user(data, id)
                return JsonResponse({"status": status, "message": message})
            except:
                return JsonResponse({"message": "Error occurred"})
        return JsonResponse({"message": "User doesn't exist"})
    return JsonResponse({"message": "Invalid request method"})



@csrf_exempt
def create_user_profile(request, id):
    if request.method == "POST":
        user = CustomUser.objects.filter(id = id).first()
        if user:
            try:
                data = json.loads(request.body)
                message, status  = validate_user.validate_create_profile(data, id)
                return JsonResponse({"status": status, "message": message})
            except:
                return JsonResponse({"message": "Error Occurred"})
        return JsonResponse({"message": "User doesn;t exist"})
    return JsonResponse({"message": "Invalid request method"})



@csrf_exempt
def update_profile(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            message, status = validate_user.validate_update_profile(data, id)
            return JsonResponse({"status": status, "message": message})
        except:
            return JsonResponse({"message": "Error occurred"})
    else:
        return JsonResponse({"message": "Invalid request method"})

    


