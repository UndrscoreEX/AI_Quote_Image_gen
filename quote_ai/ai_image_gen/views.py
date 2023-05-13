from django.shortcuts import render
from django.views import View
from .db_interactions import DB_interactions
# from django.contrib.sessions.backends import signed_cookies



# Create your views here.
class Home_page(View):
    def get(self,request):

        # getting the 5 random images for carousel
        images = DB_interactions.get_saved_images()
        # print(images)
        # print(dir(images[1].quote.theme_tag.all().values))
        # print(images[1].quote.theme_tag.all().values_list('name', flat=True))

        saved_images_dict = [{
                'quote': img.quote.text,
                'image_url' : img.ai_img,
                'author' : img.quote.book.author,
                'book' : img.quote.book.name,
                'img_tags' : list(img.quote.theme_tag.values_list('name', flat=True),),
                'theme_tags' : list(img.quote.image_tag.values_list('name', flat=True))
            } for img in images]

        print(saved_images_dict)


        print('checking sessions at the start: ',  request.session.session_key, request.session['submissions'] )
        if request.session.__contains__('submissions'):
            print('previous session')
            print('views, remaining tokens =',request.session.get('submissions'))
        else:
            request.session['submissions'] = 3
            # print('no sessions')
            request.session.save()
            # print('Session saved. Session ID:', request.session.session_key)

        # request.session.save()　　＝＝ use when we add our redis cache layer
        submissions = request.session.__getitem__('submissions')


        theme_tags_for_search = DB_interactions.tags.all()
        theme_tags_for_search = [x[0] for x in theme_tags_for_search.values_list("name")]
        # print(theme_tags_for_search)

        print('checking sessions after initial check: ',  request.session.session_key, request.session['submissions'] )

        return render(request,'index.html',{
            'theme_tag_results_raw':", ".join(theme_tags_for_search),
            'theme_tags_results_list': theme_tags_for_search,
            'sumbissions_so_far' : submissions,
            'carousel_images': saved_images_dict,
            })