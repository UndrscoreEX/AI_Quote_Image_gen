from .models import Quotes,Theme_tags,Image_tags,Book


class DB_interactions:
    tags = Theme_tags.objects

    @classmethod
    def get_image_tags(cls, theme_tags):
        img_tags = cls.tags.filter(name= theme_tags)[0]
        return img_tags


# eventually this will be needed to check the redis db so it is worth keeping it here in the DB interactions. 

# For later use:
# def tokens_check(value):
#     def decorator(fn):
#         def wrapper(*args, **kwargs):
#             if value <= 0:
#                 print('no more tokens left')
#             else:
#                 print('submission tokens checked')
#                 return fn(*args, **kwargs)
#         return wrapper
#     return decorator
    
def submissions_check(token):
    print(f'remaining tokens are : {token}')
    return token> 0