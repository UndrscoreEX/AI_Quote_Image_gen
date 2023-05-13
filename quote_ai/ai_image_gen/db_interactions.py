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
    
    # from a time when I didn't know that Dall-E will invalidate the links. 
    @classmethod
    def save_new_image(cls, quote, url, prompt_text):
        # Saved_images.objects.create(quote=quote, ai_image_url=url, prompt=prompt_text)
        Saved_images.create_from_url(quote=quote,image_url=url, prompt=prompt_text)

    @classmethod
    def get_saved_images(cls):

        # 5 random numbers 
        pks =  list(Saved_images.objects.values_list('id',flat=True))
        random.shuffle(pks)
        print(pks)
        rand_images = Saved_images.objects.filter(pk__in=pks[:5])
        return rand_images


def submissions_check(token):
    print(f'remaining tokens are : {token}')
    return token> 0