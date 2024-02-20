from . import accessor
from ..post import accessor as post_accessor
from ..user import accessor as user_accessor

def validate_create_data(data, user_id, post_id):
    user = user_accessor.get_user_by_id(user_id)
    post = post_accessor.get_post_by_id(post_id)
    if user:
        if post:
            try:
                comment = data["comment"]
                if comment == "":
                    return "Fields are required", 400
                return "All valid", 200
            except:
                return "Error occurred", 400
        return "Post doesn't exists", 400
    return "User doesn't exists", 400


def validate_delete_comment(id):
    comment = accessor.get_comment_by_id(id)
    if comment != "None":
        comment.delete()
        return "Data Successfully deleted", 200
    return "Data doesn't exists", 400



def validate_update_comment(data, id):
    comment = accessor.get_comment_by_id(id)
    if comment:
        try:
            if data["comment"] == "":
                return "Fields cannot be empty", 400
            accessor.update_comment(data, comment)
            return "Data successfully updated", 200
        except:
            return "Error occurred", 400
    return "Comment doesn'nt exists", 400


def validate_comment_by_posts(id):
    post = post_accessor.get_post_by_id(id)
    if post:
        comments = accessor.get_comment_by_posts(post)
        if comments:
            return comments, 200
        return "Comments doesn't exists", 400
    return "Post doesn't exists"

