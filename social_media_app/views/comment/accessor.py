from social_media_app.models import Comment
from ..post import accessor as post_accessor
from ..user import accessor as user_accessor


def create_comment(data, user_id, post_id):
    user = user_accessor.get_user_by_id(user_id)
    post = post_accessor.get_post_by_id(post_id)
    comment = Comment.objects.create(comment = data["comment"], user=user, post=post)
    
    
def get_comment_by_id(id):
    comment = Comment.objects.filter(id = id).first()
    return comment


def get_comment_by_posts(post):
    comments = Comment.objects.filter(post = post).values()
    return comments
    
def update_comment(data, post):
    post.comment = data["comment"]
    post.save()
    
    