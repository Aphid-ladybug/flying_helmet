from django.urls import path
from . import views

app_name = 'flying_helmet'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.index, name='login_page'),
    path('verify', views.verify, name='verify'),
    path('signup', views.signup, name='signup'),
    path('recipe/<str:recipe_name>', views.recipe, name='recipe'),
    path('profile/<str:poster_username>', views.profile, name='profile'),
    path('upload', views.upload, name='upload'),
    path('post_recipe', views.post_recipe, name='post_recipe'),
    path('logout', views.logout_view, name='logout'),
    path('search', views.search, name='search'),
    path('filter', views.filter, name='filter'),
]