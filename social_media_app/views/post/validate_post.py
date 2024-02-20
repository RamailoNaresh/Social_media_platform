from . import accessor
from ..user import accessor as user_accessor
import os

def validate_create_data(data, id):
    user = user_accessor.get_user_by_id(id)
    if user:
        try:
            if data["caption"] == "" and data["post_img"] == "":
                return "One of the Field is required", 400
            else:
                if data["post_img"] != "":
                    if  not os.path.exists(data["post_img"]):
                        return "File doesn't exists", 400
                return "Valid data", 200
        except:
            return "Error occurred", 400
    return "User doesn't exists", 400


def validate_get_posts():
    posts = accessor.get_posts()
    if posts:
        return posts, 200
    return "No data found", 400

def validate_get_post_by_id(id):
    post = accessor.get_post_by_id(id)
    if post:
        return post, 200
    return "Post doesn't exists", 400


def validate_delete_post(id):
    post = accessor.get_post_by_id(id)
    if post:
        post.delete()
        return "Successfully deleted", 200
    return "Post doesn't exists", 400

def validate_update_post(data,id):
    post = accessor.get_post_by_id(id)
    if post:
        try:
            if data["caption"] == "" and data["post_img"] == "":
                return "One of the Field is required", 400
            else:
                if data["post_img"] != "":
                    if  not os.path.exists(data["post_img"]):
                        return "File doesn't exists", 400
                accessor.update_post(data, id)
                return "Successfully updated", 200
        except:
            return "Error occurred", 400
    return "Post doesn't exists", 400

def validate_like_post(user_id, post_id):
    user = user_accessor.get_user_by_id(user_id)
    post = accessor.get_post_by_id(post_id)
    if user:
        if post:
            if post.like.filter(id = user.id).exists():
                post.like.remove(user)
                return "Disliked post", 200
            post.like.add(user)
            return "Liked post", 200
        return "Post doesn't exists", 400
    return "User doesn't exists", 400

def validate_get_likes(id):
    post = accessor.get_post_by_id(id)
    if post:
        return f"total like {accessor.get_likes(id)}", 200
    return "Post doesn't exists", 400