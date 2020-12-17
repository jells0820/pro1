from django.urls import path
from .views import comment_thread

from . import views

urlpatterns = [
    path('<abc>/', comment_thread, name='thread'),
    #path('article/<int:question_id>/<int:pk>/delete/', DeleteArticleView.as_view(), name='delete_article'),
]
