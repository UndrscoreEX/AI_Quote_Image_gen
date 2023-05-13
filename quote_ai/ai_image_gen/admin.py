from django.contrib import admin
from .models import Quotes, Theme_tags, Image_tags, Book, Salt, Saved_images
# Register your models here.

@admin.register(Quotes)
class  Quote_class(admin.ModelAdmin):
    list_display = ['text','book',]
    # list_display = [f.name for f in Book._meta.fields]

@admin.register(Theme_tags)
class  Theme_tag_class(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Image_tags)
class  Image_tag_class(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Book)
class  Book_class(admin.ModelAdmin):
    list_display = ['name','author']

@admin.register(Salt)
class Salt_class(admin.ModelAdmin):
    list_display = ['text']

@admin.register(Saved_images)
class Saved_images_class(admin.ModelAdmin):
    list_display = ['pk','quote', 'ai_img']
