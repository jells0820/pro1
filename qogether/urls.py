from django.urls import path
from .views import AddQuestionView, AddArticleView, UpdateArticleView, DeleteArticleView, LikeView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_question/', AddQuestionView.as_view(), name='add_question'),
    path('add_article/<int:question_id>/', AddArticleView.as_view(), name='add_article'),
    path('article/edit/<int:pk>', UpdateArticleView.as_view(), name='update_article'),
    path('article/<int:question_id>/<int:pk>/delete/', DeleteArticleView.as_view(), name='delete_article'),
    path('q_list/', views.q_list, name='q_list'),
    path('q_list/<int:question_id>/', views.a_list, name='a_list'),
    path('q_list/<int:question_id>/<int:article_id>/', views.article, name='article'),
    path('like/<int:pk>', LikeView, name='like_article'),
]
