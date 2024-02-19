from django.http import JsonResponse
from social_media_app.models import Comment, Post, CustomUser
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def create_comment(request, user_id, post_id):
    if request.method == "POST":
        post = Post.objects.filter(id = post_id).first()
        user = CustomUser.objects.filter(id = user_id).first()
        if post:
            if user:
                try:
                    data = json.loads(request.body)
                    comment = data["comment"]
                    if comment == "":
                        return JsonResponse({"message": "Field is required"})
                    comment_obj = Comment.objects.create(comment=comment, user=user, post=post)
                    return JsonResponse({"message": "Comment added"})
                except:
                    return JsonResponse({"message": "Error occurred"})
            return JsonResponse({"message": "User doesn't exist"})
        return JsonResponse({"message": "Post doesn't exist"})
    return JsonResponse({"message": "Invalid request method"})


def get_comment_by_id(request, id):
    comment = Comment.objects.filter(id = id).values().first()
    if comment:
        return JsonResponse({"message": "Data received", "data": comment})
    return JsonResponse({"message": "Comment doesn't exist"})

def get_comment_of_post(request, post_id):
    post = Post.objects.filter(id = post_id).first()
    if post:
        comments = Comment.objects.filter(post = post).values()
        data = list(comments)
        return JsonResponse({"message": "data received", "data": data})
    return JsonResponse({"message": "Post doesn't exists"})


@csrf_exempt
def delete_comment(request, id):
    if request.method == "DELETE":
        comment = Comment.objects.filter(id = id).first()
        if comment:
            comment.delete()
            return JsonResponse({"message": "Comment successfully deleted"})
        return JsonResponse({"message": "Comment doesn't exists"})
    return JsonResponse({"message": "Invalid request method"})


@csrf_exempt
def update_comment(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            comment = data["comment"]
            comment_obj = Comment.objects.filter(id = id).first()
            if comment_obj:
                comment_obj.comment = comment
                comment_obj.save()
                return JsonResponse({"message": "comment updated"})
            return JsonResponse({"message": "comment doesn't exist"})
        except:
            return JsonResponse({"message": "Error occurred"})
    return JsonResponse({"message": "Invalid request method"})
    