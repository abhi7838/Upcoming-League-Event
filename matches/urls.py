from django.urls import path
from .views import upcoming_matches_view,basic


urlpatterns = [
    path('',upcoming_matches_view, name = 'upcoming_matches_view'),

]
  