


from django.urls import path
# Импортируем созданные нами представления
from .views import (NewsList, NewDetail, NewsCreate, NewsUpdate, NewsDelete, CategoryListView, subscribe, unsubscribe)
from .views import upgrade_me
from django.urls import include

urlpatterns = [

   path('', NewsList.as_view()),

   path('<int:pk>', NewDetail.as_view()),

   path('create/', NewsCreate.as_view(), name='news_create'),

   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),

   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('upgrade/', upgrade_me, name = 'upgrade'),

   path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),

   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),

   path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),



]