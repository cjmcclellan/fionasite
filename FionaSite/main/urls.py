from django.urls import include, path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='home', permanent=False)),
    path('home', views.MainPage.as_view(), name='home'),
    path('research', views.ResearchPage.as_view(), name='research'),
    path('display', views.DisplayPage.as_view(), name='display'),
    # path('projects', views.ProjectsPage.as_view(), name='projects'),
    # path('hobbies', views.HobbiesPage.as_view(), name='hobbies'),
    path('contact_me', views.ContactMe.as_view(), name='contact_me'),
    # path('ajax/ajax_carousel_images', views.ajax_carousel_images, name='carousel_images'),
]