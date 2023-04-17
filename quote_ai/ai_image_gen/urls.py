from django.urls import path
from .views import Home_page


urlpatterns =[
    path('home/', Home_page.as_view(), name='home')
]