from django.shortcuts import render
from django.views import View
from .db_interactions import DB_interactions
# from django.contrib.sessions.backends import signed_cookies



# Create your views here.
class Home_page(View):
    def get(self,request):
        # request.session
        # setting session limit:
        # It will then be collected through the scope on the consumers.py side

        if not request.session.__contains__('submissions'):
            request.session.__setitem__('submissions', 3)
            print('no sessions')
        else:
            print('previous session')
            print(request.session.get('submissions'))

        # request.session.save()　　＝＝ use when we add our redis cache layer
        submissions = request.session.__getitem__('submissions')


        theme_tags_for_search = DB_interactions.tags.all()
        theme_tags_for_search = [x[0] for x in theme_tags_for_search.values_list("name")]
        # print(theme_tags_for_search)


        return render(request,'index.html',{
            'theme_tag_results_raw':", ".join(theme_tags_for_search),
            'theme_tags_results_list': theme_tags_for_search,
            'sumbissions_so_far' : submissions
            })