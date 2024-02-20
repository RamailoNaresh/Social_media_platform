from social_media_app.models import CustomUser, UserProfile
from django.contrib.auth.hashers import make_password
import os

def create_user(data):
    CustomUser.objects.create(name = data["name"], email = data["email"], password = make_password(data["password"]))
    
def get_user_by_id(id):
    user = CustomUser.objects.filter(id =id).first()
    return user

def user_profile_id(id):
    user = CustomUser.objects.filter(id = id).values().first()
    profile = UserProfile.objects.filter(user = id).values().first()
    return user,profile

def get_users():
    users = CustomUser.objects.all().values()
    return list(users)


def update_user(data,id):
    user = get_user_by_id(id)
    user.name = data["name"]
    user.email = data["email"]
    user.password = make_password(data["password"])
    user.save()
    


def create_profile(data, id):
    user = get_user_by_id(id)
    profile1 = UserProfile(address=data["address"], country=data["country"], phone_number=data["phone_number"], user = user)
    profile_img_path = data["profile_img"]
    if profile_img_path != "":
        filename = f"post_{user.id}.jpg"
        with open(profile_img_path, 'rb') as img_file:
            profile1.profile_img.save(filename, img_file)
        
    profile1.save()
    
    
def update_profile(data, id):
    print("naresh")
    user = CustomUser.objects.filter(id = id).first()
    profile = UserProfile.objects.filter(user = user).first()
    if data["profile_img"] != "":
        if profile.profile_img != "":
            old_post_img = profile.profile_img.path
            if os.path.exists(old_post_img):
                os.remove(old_post_img)
    profile_img_path = data["profile_img"]
    filename = f"profile_{user.id}.jpg"
    with open(profile_img_path, 'rb') as img_file:
        profile.profile_img.save(filename, img_file)
    profile.phone_number = data["phone_number"]
    profile.address = data["address"]
    profile.country = data["country"]
    profile.save() 