from . import accessor
import os
from social_media_app.models import CustomUser, UserProfile


def validate_create_data(data):
    try:
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        if name == "" or email == "" or password == "":
            return "All fields are required", 400
        user = CustomUser.objects.filter(email = email).first()
        if user:
            return "Email already exists", 400
        accessor.create_user(data)
        return "Successfully created", 200
    except:
        return "Error occurred", 400

def validate_get_user_by_id(id):
    user, profile = accessor.user_profile_id(id)
    if user:
        data = {
            "user": user,
            "profile": profile
        }
        return data, 200
    return "User doesn't exists", 400

def validate_delete_user( id):
    user = accessor.get_user_by_id(id)
    profile = UserProfile.objects.filter(user = id).first()
    if profile.profile_img != "":
        old_post_img = profile.profile_img.path
        if os.path.exists(old_post_img):
            os.remove(old_post_img)
    if user:
        json_data = {
            "name": user.name,
            "email": user.email
        }
        user.delete()
        return "User deleted successfully", 200
    else:
        return "User doesn;t exists", 400
    
    
def validate_update_user(data,id):
    try:
        user1 = CustomUser.objects.exclude(id=id).filter(email=data["email"]).first()
        if user1:
            return "Email already exists", 400
        user, profile = accessor.get_user_by_id(id)
        if user != None:
            accessor.update_user(data, id)
            return "Successfully updated", 200
        return "User doesn't exists", 400
    except:
        return "Error occurred", 400
    
    
def validate_create_profile(data, id):
    user  = accessor.get_user_by_id(id)
    if user:
        try:
            address = data["address"]
            country = data["country"]
            phone_number = data["phone_number"]
            profile_img = data["profile_img"]
            if address == "" or country == "" or phone_number == "":
                return "Fields cannot be empty", 400
            if len(str(phone_number))!=10:
                return "Invalid number", 400
            accessor.create_profile(data, id)
            return "Profile created", 200
        except:
            return "Error occurred", 400
    return "User doesn't exists", 400

def validate_update_profile(data,id):
    try:
        phone_number = data.get('phone_number')
        address = data.get('address')
        country = data.get('country')
        profile_img_path = data.get('profile_img')
        user, profile = accessor.user_profile_id(id)
        if not user:
            return "User doesn't exist", 400
        if not profile:
            return "Profile doesn't exist", 400
        if len(str(phone_number)) != 10:
                return "Phone number not valid", 400     
        accessor.update_profile(data, id)
        return "Profile successfully updated", 200
    except:
        return "Error occurred", 400