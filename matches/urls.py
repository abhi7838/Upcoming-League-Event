from django.urls import path
from .views import upcoming_matches_view


urlpatterns = [
    path('upcoming/', views.upcoming_matches_view, name = 'upcoming_matches_view'),

]
