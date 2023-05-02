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