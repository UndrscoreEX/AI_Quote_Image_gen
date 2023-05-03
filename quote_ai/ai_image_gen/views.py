from django.shortcuts import render
from django.views import View
from .db_interactions import DB_interactions
# from django.contrib.sessions.backends import signed_cookies



# Create your views here.
class Home_page(View):
    def get(self,request):

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
            'sumbissions_so_far' : submissions
            })