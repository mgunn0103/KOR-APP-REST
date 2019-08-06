from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

""" The DefaultRouter automatically registers all of the appropriate urls for 
    all of the actions in our viewset
"""
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]