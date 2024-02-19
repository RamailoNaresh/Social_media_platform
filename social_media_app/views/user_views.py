from django.shortcuts import render
from social_media_app.models import CustomUser, UserProfile
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from datetime import datetime


def get_user(request):
    datas = CustomUser.objects.all()
    json_data = list(datas.values())
    return JsonResponse({"data": json_data})

@csrf_exempt
def create_user(request):
    if request.method == "POST":
            data = json.loads(request.body)
            name = data["name"]
            email = data["email"]
            password = data["password"]
            if name == "" or email == "" or password == "":
                return JsonResponse({"error": "Fields cannot be empty"}, status = 400)
            user = CustomUser.objects.filter(email = email).first()
            if user:
                return JsonResponse({"error": "Email already exists"})
            user1 = CustomUser.objects.create(name = name, email = email, password = make_password(password))
            return JsonResponse({"message": "User created successfully", "data": data}, status = 200)
    return JsonResponse({"message": "Error occured"}, status = 500)


def get_user_by_id(request, id):
    user = CustomUser.objects.filter(id = id).values().first()
    if user:
        profile = UserProfile.objects.filter(user = user["id"]).values().first()
        return JsonResponse({"data": user, "profile": profile})
    else:
        return JsonResponse({"message": "User doesn't exist"})
 
@csrf_exempt   
def delete_user(request, id):
    if request.method == "DELETE":
        user = CustomUser.objects.filter(id = id).first()
        if user:
            json_data = {
                "name": user.name,
                "email": user.email
            }
            user.delete()
            return JsonResponse({"message": "User successfully deleted", "data": json_data})
        else:
            return JsonResponse({"message": "User doesn't exist"})
    return JsonResponse({"message": "Error occured"})
    
@csrf_exempt
def update_user(request, id):
    if request.method == "PUT":
        user = CustomUser.objects.filter(id = id).first()
        if user:
            data = json.loads(request.body)
            user1 = CustomUser.objects.exclude(id=user.id).filter(email=data["email"]).first()
            if user1:
                return JsonResponse({"message": "User already exist with give email"})
            user.name = data["name"]
            user.email = data["email"]
            user.password = make_password(data["password"])
            user.save()
            json_data = {
                "name": user.name,
                "email": user.email,
                "password": user.password
            }
            return JsonResponse({"message": "User data successfully updated","data": json_data})
        return JsonResponse({"message": "User doesn't exist"})
    return JsonResponse({"message": "Error occured"})



@csrf_exempt
def create_user_profile(request, id):
    if request.method == "POST":
        user = CustomUser.objects.filter(id = id).first()
        if user:
            phone_number = request.POST["phone_number"]
            address = request.POST["address"]
            country = request.POST["country"]
            profile_img = request.FILES["profile_img"]
            if phone_number == "" or address == "" or country == "":
                return JsonResponse({"message": "Fields cannot be empty"})
            userprofile = UserProfile.objects.create(phone_number= phone_number, address= address, country = country, user= user, profile_img = profile_img)
            return JsonResponse({"message": "user profile created"})
        return JsonResponse({"message": "User doesn;t exist"})
    return JsonResponse({"message": "Error occurred"})


# @csrf_exempt
# def update_profile(request, id):
#     if request.method == "PUT":
#         user = CustomUser.objects.filter(id  = id).first()
#         if user:
#             profile = UserProfile.objects.filter(user= user).first()
#             data = json.loads(request.body)
#             print(data)
#             # if profile:
#             #     profile.phone_number = data["number"]
#             #     profile.address = data["address"]
#             #     profile.country = data["country"]
#             #     profile.save()
#                 # return JsonResponse({"message": "SUccessfully updated"})
#             return JsonResponse({"message":"Profile doesn't exists"})
#         return JsonResponse({"message":"User doesn't exists"})
#     return JsonResponse({"message": "Error occurred"})


@csrf_exempt
def update_profile(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        address = data.get('address')
        country = data.get('country')
        profile_img_path = data.get('profile_img')
        user = CustomUser.objects.filter(id=id).first()
        if not user:
            return JsonResponse({"message": "User doesn't exist"})
        
        profile = UserProfile.objects.filter(user=user).first()
        if not profile:
            return JsonResponse({"message": "Profile doesn't exist"})
        filename = f"profile_{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        with open(profile_img_path, 'rb') as img_file:
            profile.profile_img.save(filename, img_file)
        profile.phone_number = phone_number
        profile.address = address
        profile.country = country
        profile.save()      
        return JsonResponse({"message": "Profile successfully updated"})
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)

    


