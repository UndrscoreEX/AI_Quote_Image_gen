from .models import Quotes,Theme_tags,Image_tags,Book


class DB_interactions:
    tags = Theme_tags.objects

    @classmethod
    def get_image_tags(cls, theme_tags):
        img_tags = cls.tags.filter(name= theme_tags)[0]
        return img_tags

