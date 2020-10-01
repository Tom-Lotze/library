# -*- coding: utf-8 -*-
# @Author: TomLotze
# @Date:   2020-08-11 13:32
# @Last Modified by:   TomLotze
# @Last Modified time: 2020-08-24 14:51

from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name="search"),
    path('<int:book_id>/', views.detail, name="detail"),
    path('<int:book_id>/changeList', views.changeList, name="changeList"),
    path('<int:book_id>/changeRating', views.changeRating,name="changeRating"),
    path('<int:book_id>/favorite', views.favorite, name="favorite"),
    path('<int:book_id>/delete', views.delete, name="delete"),
    path('<int:list_id>/listview', views.listview, name="listview"),
    path('<int:book_id>/review', views.review, name="review"),
    path('searchDB', views.searchDB, name="searchDB"),

]
