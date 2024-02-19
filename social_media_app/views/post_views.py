from social_media_app.models import Post, Comment, CustomUser
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os

@csrf_exempt
def create_post(request, id):
    if request.method == "POST":
        caption = request.POST["caption"]
        post_img = request.FILES["post_img"]
        if post_img == "":
            if caption == "":
                return JsonResponse({"message": "Atleast one field is required"})
        user = CustomUser.objects.filter(id=id).first()
        if user:
            post = Post.objects.create(caption=caption, post_img=post_img, user=user)
            response_data = {
                "message": "Post successfully created",
                "data": {
                    "id": post.id,
                    "caption": post.caption,
                    "post_img": post.post_img.url,
                    "user": post.user.id
                }
            }
            return JsonResponse(response_data, status=200)  
        else:
            return JsonResponse({"message": "User doesn't exist"}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)
def get_posts(requets):
    posts = Post.objects.all()
    json_data = list(posts.values())
    return JsonResponse({"message": "Data Received", "data": json_data})


def get_post_by_id(request, id):
    post = Post.objects.filter(id = id).values().first()
    if post:
        return JsonResponse({"data":post})
    return JsonResponse({"message": "post doesn't exists"})

@csrf_exempt
def delete_post(request, id):
    if request.method == "DELETE":
        post = Post.objects.filter(id = id).first()
        if post:
            if post.post_img != "":
                old_post_img = post.post_img.path
                if os.path.exists(old_post_img):
                    os.remove(old_post_img)
            post.delete()
            return JsonResponse({"message": f"Post with id {id} is successfully deleted"})
        return JsonResponse({"message": "Post doesn't exist"})
    return JsonResponse({"message": "Error occurred"})

# method when data is passed in json format
@csrf_exempt
def update_post(request, id):
    if request.method == "PUT":
        post = Post.objects.filter(id = id).first()
        if post:
            if post.post_img != "":
                old_post_img = post.post_img.path
                if os.path.exists(old_post_img):
                    os.remove(old_post_img)
            data = json.loads(request.body)
            post.caption = data["caption"]
            post_img_path = data["post_img"]
            filename = f"post_{post.id}.jpg"
            with open(post_img_path, 'rb') as img_file:
                post.post_img.save(filename, img_file)
            post.save()
            return JsonResponse({"message": "User data successfully updated"})
        return JsonResponse({"message": "User doesn't exist"})
    return JsonResponse({"message": "Error occured"})


def like_post(request, user_id, post_id):
    user = CustomUser.objects.filter(id = user_id).first()
    post = Post.objects.filter(id = post_id).first()
    if post:
        if user:
            if post.like.filter(id = user.id).exists():
                post.like.remove(user)
                return JsonResponse({"message": f"Disliked post of id {post.id}"})
            post.like.add(user)
            return JsonResponse({"message": f"Liked post of id {post.id}"})
        return JsonResponse({"message": "User doesn't exist"})
    return JsonResponse({"message": "Post doesn't exist"})

def get_likes(request, post_id):
    post = Post.objects.filter(id = post_id).first()
    if post:
        likes = post.like.count()
        json_data = {
            "caption": post.caption,
            "post_img":post.post_img.url
        }
        return JsonResponse({"Post": json_data, "like": likes})
    return JsonResponse({"message": "Post doesn't exist"})
        