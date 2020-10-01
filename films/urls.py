# -*- coding: utf-8 -*-
# @Author: TomLotze
# @Date:   2020-08-14 10:27
# @Last Modified by:   TomLotze
# @Last Modified time: 2020-09-02 20:00


from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name="search"),
    path('<int:film_id>/', views.detail, name="detail"),
    path('<int:film_id>/changeStatus', views.changeStatus, name="changeStatus"),
    path('<int:film_id>/changeRating', views.changeRating,name="changeRating"),
    path('<int:film_id>/favorite', views.favorite, name="favorite"),
    path('<int:film_id>/delete', views.delete, name="delete"),
    path('<int:genre_id>/genre', views.genre, name="genre"),
    path('<int:actor_id>/actor', views.actor, name="actor"),
    path('<int:film_id>/review', views.review, name="review"),
    path('<int:list_id>/listview', views.listview, name="listview"),
    path('searchDB', views.searchDB, name="searchDB"),
]