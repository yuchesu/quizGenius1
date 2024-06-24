from django.contrib import admin
from .models import Category, Quiz, Question, Choice, QuizQuestion


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'time_start', 'time_end')
    inlines = [QuizQuestionInline]


admin.site.register(Quiz, QuizAdmin)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)

admin.site.register(Category)
# admin.site.register(Quiz)
# admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizQuestion)
