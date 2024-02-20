from social_media_app.models import Post
import os
from ..user import accessor as user_accessor


def get_post_by_id(id):
    post = Post.objects.filter(id = id).first()
    return post


def get_posts():
    posts = Post.objects.all().values()
    return posts


def create_post(data, id):
    user = user_accessor.get_user_by_id(id)
    post = Post(caption = data["caption"], user = user)
    post_img_path = data["post_img"]
    if post_img_path != "":       
        filename = f"post_{post.id}.jpg"
        with open(post_img_path, 'rb') as img_file:
            post.post_img.save(filename, img_file)
    post.save()


def update_post(data, id):
    post = get_post_by_id(id)
    if post.post_img != "":
        old_post_img = post.post_img.path
        if os.path.exists(old_post_img):
            os.remove(old_post_img)
        post.caption = data["caption"]
        post_img_path = data["post_img"]
        if post_img_path != "":
            filename = f"post_{post.id}.jpg"
            with open(post_img_path, 'rb') as img_file:
                post.post_img.save(filename, img_file)
        post.save()
        
        
def get_likes(id):
    post = get_post_by_id(id)
    return post.like.count()