from django.http import JsonResponse
from social_media_app.models import Comment, Post, CustomUser
from django.views.decorators.csrf import csrf_exempt
import json
from . import validate_comment, accessor



@csrf_exempt
def create_comment(request, user_id, post_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            validate_data, status = validate_comment.validate_create_data(data, user_id, post_id)
            if status == 200:
                accessor.create_comment(data, user_id, post_id)
                return JsonResponse({"message": "User Successully create", "data": data})
            return JsonResponse({"message": validate_data, "status": status})
        except:
            return JsonResponse({"message": "Error occurred"})
    return JsonResponse({"message": "Invalid request method"})


def get_comment_by_id(request, id):
    if request.method == "GET":
        comment = accessor.get_comment_by_id(id)
        if comment:
            return JsonResponse({"status": 200,"message":"Data received", "data":comment})
        return JsonResponse({"status":400,"message": "Data doesn't exists"})
    return JsonResponse({"status": 400,"message":"Invalid request method"})

def get_comment_of_post(request, post_id):
    if request.method == "GET":
        message, status = validate_comment.validate_comment_by_posts(post_id)
        if status == 200:
            return JsonResponse({"status": 200, "message": "Data received", "data": list(message)})
        return JsonResponse({"status": 400, "message": message})
    return JsonResponse({"status": 400,"message":"Invalid request method"})





@csrf_exempt
def delete_comment(request, id):
    if request.method == "DELETE":
        message, status = validate_comment.validate_delete_comment(id)
        return JsonResponse({"status":status, "message": message})
    return JsonResponse({"status":400,"message": "Invalid request method"})


@csrf_exempt
def update_comment(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            message, status = validate_comment.validate_update_comment(data,id)
            return JsonResponse({"status": status, "message": message})
        except:
            return JsonResponse({"message": "Error occurred"})
    return JsonResponse({"message": "Invalid request method"})
    