from django.contrib import admin

from .models import Question, Article, Profile

class ArticleInline(admin.StackedInline):
    model = Article
    extra = 1

class Questionadmin(admin.ModelAdmin):
    fieldssets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ArticleInline]


admin.site.register(Question, Questionadmin)
admin.site.register(Profile)
'''admin.site.register(Comment)'''

# Register your models here.
