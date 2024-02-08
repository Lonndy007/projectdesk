from django.urls import path
from .views import  Postivew,PostDetail,PostCreate,PostUpdate,PostDelete,CommentCreate
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('',cache_page(60)(Postivew.as_view()),name='news'),
   path('<int:pk>',cache_page(300)(PostDetail.as_view()),name='news_detail'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('<int:pk>/comment/create/',CommentCreate.as_view(),name='comment_create')
]