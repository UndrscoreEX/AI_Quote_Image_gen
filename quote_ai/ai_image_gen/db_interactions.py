from .models import Quotes,Theme_tags,Image_tags,Book, Salt, Saved_images
import random


class DB_interactions:
    tags = Theme_tags.objects
    salt = Salt.objects


    @classmethod
    def get_image_tags(cls, theme_tags):
        img_tags = cls.tags.filter(name= theme_tags)[0]
        return img_tags
    
    @classmethod
    def get_salt(cls):
        salt = cls.salt.all()
        # print(salt)
        salt = random.choice(salt)
        return salt
    
    @classmethod
    def save_new_image(cls, quote, url, prompt_text):
        Saved_images.objects.create(quote=quote, ai_image_url=url, prompt=prompt_text)

    @classmethod
    def get_saved_images(cls):

        # 5 random numbers 
        length =  Saved_images.objects.count()
        rand_nums = random.sample(range(1,length), 5)
        print(rand_nums)
        # rand_arr =  [Saved_images.objects.get(pk=4) for x in rand_nums]
        # rand_images = Saved_images.objects.get(pk=2)
        rand_images = Saved_images.objects.filter(pk__in=rand_nums)
        # print("all random images",rand_images)
        return rand_images



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