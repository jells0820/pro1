from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Article
from comment.forms import CommentForm
from comment.models import Comment
from django.template import loader
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.contenttypes.models import ContentType
from django import forms

#from .forms import ArticleForm, EditForm
from .forms import *

# Create your views here.
def index(request):
    question_list = Question.objects.order_by('-pub_date')[:20]
    searched_question = request.POST.get("searched_question")
    search_choice = request.POST.get("search_choice")

    context = {
    'question_list': question_list,
    'searched_question': searched_question,
    'search_choice': search_choice,
    }

    return render(request, 'qogether/index.html', context)

def q_list(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:20]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'qogether/q_list.html', context)

def a_list(request, question_id):
    selected_question = get_object_or_404(Question, pk=question_id)
    latest_article = selected_question.article_set.all()
    latest_article_list = latest_article.order_by('-pub_date')[:20]
    context = {
        'selected_question': selected_question,
        'latest_article_list': latest_article_list
        }
    return render(request, 'qogether/a_list.html', context)
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'qogether/a_list.html', {'question': question})
'''
def article(request, question_id, article_id):
    question = get_object_or_404(Question, pk=question_id)
    article = get_object_or_404(Article, pk=article_id)

    initial_data = {
        "content_type": article.get_content_type,
        "object_id": article.id,
    }
    comments = article.comments
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model='article')
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() ==1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                                    user = request.user,
                                    content_type = content_type,
                                    object_id = obj_id,
                                    content = content_data,
                                    parent = parent_obj,
                                )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

        if created:
            print("Yeah it worked")

    total_likes = article.total_likes()
    liked = False
    if article.likes.filter(id=request.user.id).exists():
        liked = True
    context = {
        'question': question,
        'article': article,
        'total_likes': total_likes,
        'liked': liked,
        'comments': comments,
        'comment_form': comment_form,
        }
    return render(request, 'qogether/article.html', context)

def LikeView(request, pk):
    article = get_object_or_404(Article, pk=request.POST.get('article_id'))
    liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article', kwargs={'question_id': article.question_id, 'article_id': article.id}))


class AddQuestionView(CreateView):
    model = Question
    template_name = 'qogether/add_question.html'
    fields = ('question_text', 'question_tag')

class AddArticleView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'qogether/add_article.html'
    #fields = ('question', 'author', 'title', 'description', 'article_tag')
    def get_context_data(self, **kwargs):
        context = super(AddArticleView, self).get_context_data(**kwargs)
        question = Question.objects.get(pk=self.kwargs['question_id'])
        context['question_id'] = question.id
        context['question_text'] = question.question_text
        return context

    def get_success_url(self):
        question = Question.objects.get(pk=self.kwargs['question_id'])
        return reverse_lazy('a_list', kwargs={'question_id': question.id})

class UpdateArticleView(UpdateView):
    model = Article
    form_class = EditForm
    template_name = 'qogether/update_article.html'

class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'qogether/delete_article.html'
    def get_success_url(self):
        return reverse_lazy('a_list', kwargs={'question_id': self.object.question_id})
