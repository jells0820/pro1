from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from .forms import CommentForm
from .models import Comment

# Create your views here.

def comment_thread(request, abc):
    obj = get_object_or_404(Comment, id=abc)
    comment_form = CommentForm(request.POST or None)
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

    context = {
        "comment": obj,
        "comment_form": comment_form,
    }
    return render(request, "qogether/comment_thread.html", context)