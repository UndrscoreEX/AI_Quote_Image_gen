from django.db import models
from urllib import request
from django.core.files import File
import uuid


class Theme_tags(models.Model):
    def __str__(self) -> str:
        return str(self.name)

    name = models.CharField(max_length=50, blank=False,
                            null=False, unique=True)


class Image_tags(models.Model):
    def __str__(self) -> str:
        return str(self.name)

    name = models.CharField(max_length=50, blank=False,
                            null=False, unique=True)


class Book(models.Model):
    def __str__(self) -> str:
        return str(self.name)

    name = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=50, blank=False, null=False)


class Quotes(models.Model):
    def __str__(self) -> str:
        return str(self.text)

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField(null=False, blank=False)
    theme_tag = models.ManyToManyField(Theme_tags)
    image_tag = models.ManyToManyField(Image_tags)


class Salt(models.Model):
    def __str__(self) -> str:
        return str(self.text)
    text = models.CharField(max_length=150, null=False, blank=False)


class Saved_images(models.Model):
    def __str__(self) -> str:
        return str(self.quote)
    quote = models.ForeignKey(
        Quotes, on_delete=models.CASCADE, related_name='saved_image')
    ai_img = models.ImageField(upload_to='uploads/')
    prompt = models.TextField(max_length=500, null=False, blank=False)

    @classmethod
    def create_from_url(cls, quote, image_url, prompt):
        response = request.urlopen(image_url)
        img_temp = open('temp_image.jpg', 'wb')
        img_temp.write(response.read())
        img_temp.close()

        with open('temp_image.jpg', 'rb') as f:
            unique_filename = str(uuid.uuid4()) + '.jpg'
            new_saved_image = cls.objects.create(quote=quote, prompt=prompt)
            new_saved_image.ai_img.save(unique_filename, File(f), save=True)

        return new_saved_image
