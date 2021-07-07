
from django.urls import path
from . import views

#  url patterns. First argument is url address from host site. second argument is a page/view for that url. Third argument is a variable for page

urlpatterns = [
    path("", views.main, name="index"),
    #path("/API", views.main, name="main"),

]