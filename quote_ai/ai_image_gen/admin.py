from django.contrib import admin
from .models import Quotes, Theme_tags, Image_tags, Book
# Register your models here.

@admin.register(Quotes)
class  Quote_class(admin.ModelAdmin):
    list_display = ['text','source']

@admin.register(Theme_tags)
class  Theme_tag_class(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Image_tags)
class  Image_tag_class(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Book)
class  Book_class(admin.ModelAdmin):
    list_display = ['name','author','quote']