from social_media_app.models import Post, Comment, CustomUser
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os
from . import validate_post, accessor


@csrf_exempt
def create_post(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body) 
            message, status = validate_post.validate_create_data(data, id)
            if status == 200:
                accessor.create_post(data, id)
                return JsonResponse({"status": status, "message": "Post created"})
            else:
                return JsonResponse({"status": status, "message": message})
        except:
            return JsonResponse({"message": "Error occurred"})
    else:
        return JsonResponse({"message": "Invalid request method"})
    
    
def get_posts(request):
    if request.method == "GET":
        message, status = validate_post.validate_get_posts()
        if status == 200:
            return JsonResponse({"status": status, "message": list(message)})
        return JsonResponse({"status": status, "message": message})
    return JsonResponse({"status": 400, "message": "Invalid request method"})


def get_post_by_id(request, id):
    if request.method == "GET":
        message, status = validate_post.validate_get_post_by_id(id)
        return JsonResponse({"status": status, "message": message})
    return JsonResponse({"status": 400, "message": "Invalid request method"})

@csrf_exempt
def delete_post(request, id):
    if request.method == "DELETE":
        message, status = validate_post.validate_delete_post(id)
        return JsonResponse({"status": status, "message": message})
    return JsonResponse({"message": "Invalid request method"})

# method when data is passed in json format
@csrf_exempt
def update_post(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            message, status = validate_post.validate_update_post(data,id)
            return JsonResponse({"status": status, "message": message})
        except:
            return JsonResponse({"message": "Error occurred"})
    return JsonResponse({"message": "Invalid request method"})


def like_post(request, user_id, post_id):
    if request.method == "GET":
        message, status = validate_post.validate_like_post(user_id, post_id)
        return JsonResponse({"status": status, "message": message})
    return JsonResponse({"status": 400, "message": "Invalid request method"})

def get_likes(request, post_id):
    if request.method == "GET":
        message, status = validate_post.validate_get_likes(post_id)
        return JsonResponse({"status": status, "message": message})
    return JsonResponse({"status":400, "message": "Invalid request method"})
        