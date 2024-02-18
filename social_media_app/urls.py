from django.urls import path
from .views import post_views, user_views, comment_views

urlpatterns = [
    path("get_user/", user_views.get_user, name = "users"),
    path("create_user/", user_views.create_user, name = "create-users"),
    path("get_user_by_id/<int:id>/", user_views.get_user_by_id, name = "user-by-id"),
    path("delete_user/<int:id>/", user_views.delete_user, name = "delete-user"),
    path("update_user/<int:id>/", user_views.update_user, name = "update-user"),
    path("get_posts/", post_views.get_posts, name = "posts"),
    path("create_post/<int:id>/", post_views.create_post, name = "create-post"),
    path("get_post_by_id/<int:id>/", post_views.get_post_by_id, name = "user-by-id"),
    path("delete_post/<int:id>/", post_views.delete_post, name = "delete-user"),
    path("update_post/<int:id>/", post_views.update_post, name = "update-user"),
    path("like_post/<int:user_id>/<int:post_id>/", post_views.like_post, name = "like-post"),
    path("get_total_like/<int:post_id>/", post_views.get_likes, name = "total-likes"),
    path("create_comment/<int:user_id>/<int:post_id>/", comment_views.create_comment, name = "create-comment"),
    path("get_comment_by_id/<int:id>/", comment_views.get_comment_by_id, name = "comment-by-id"),
    path("get_comment_by_post/<int:post_id>/", comment_views.get_comment_of_post, name = "post-comments"),
    path("delete_comment/<int:id>/",comment_views.delete_comment, name = "delete-comment"),
    path("update_comment/<int:id>/", comment_views.update_comment, name = "update-comment"),
    path("create_profile/<int:id>/", user_views.create_user_profile, name = "create-profile"),
    path("update_profile/<int:id>/", user_views.update_profile, name = "update-profile")
]