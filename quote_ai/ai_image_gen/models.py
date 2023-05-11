from django.db import models


class Theme_tags(models.Model):
    def __str__(self) -> str:
        return str(self.name)
    
    name = models.CharField(max_length=50, blank=False,null=False ,unique=True)


class Image_tags(models.Model):
    def __str__(self) -> str:
        return str(self.name)
    
    name = models.CharField(max_length=50, blank=False,null=False, unique=True)

    
class Book(models.Model):
    def __str__(self) -> str:
        return str(self.name)
    
    name= models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=50, blank=False, null=False)


class Quotes(models.Model):
    def __str__(self) -> str:
        return str(self.text)
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quotes')
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
    quote = models.ForeignKey(Quotes, on_delete=models.CASCADE, related_name='saved_image')
    ai_image_url = models.URLField(max_length=500)
    prompt = models.TextField(max_length=500, null=False, blank= False)
