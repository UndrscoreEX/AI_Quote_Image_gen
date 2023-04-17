from django.shortcuts import render
from django.views import View
from .models import Theme_tags, Image_tags, Book, Quotes

# Create your views here.
class Home_page(View):

    def get(self,request):
        theme_tags_for_search = Theme_tags.objects.all()
        theme_tags_for_search = [x[0] for x in theme_tags_for_search.values_list("name")]


        return render(request,'index.html',{
            'theme_tag_results_raw':", ".join(theme_tags_for_search),
            'theme_tags_results_list': theme_tags_for_search
            })