from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import QuestionUpdateForm, ChoiceForm, CategoryForm, CategoryUpdateForm
from .models import Category, Question, Quiz, Choice, QuizQuestion
from django.urls import reverse_lazy, reverse
from django.db.models import Prefetch
from apps.accounts.models import CustomUser


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "quiz/home.html"

    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # # Filter categories with ongoing quizzes
        # ongoing_quizzes = Category.objects.filter(
        #     quiz__time_end__isnull=True
        # ).distinct()
        #
        # if ongoing_quizzes.exists():
        #     context['category_list'] = ongoing_quizzes
        # else:
        #     # If no ongoing quizzes, show all categories
        #     context['category_list'] = Category.objects.all()

        # Fetch quiz history for the current user
        quizzes = Quiz.objects.filter(user=self.request.user).order_by('-time_end')

        # Prefetch related QuizQuestions and Choices for better performance
        quizzes = quizzes.prefetch_related(
            Prefetch('quizquestion_set', queryset=QuizQuestion.objects.select_related('question', 'user_choice')),
            'quizquestion_set__question__choice_set'
        )

        for quiz in quizzes:
            quiz.correct_answers = quiz.calculate_correct_answers()

        context['quizzes'] = quizzes
        return context


class NewQuizView(LoginRequiredMixin, View):
    template_name = 'quiz/quiz_new.html'

    def get(self, request, category_id, *args, **kwargs):
        # Retrieve 5 random questions for the quiz
        questions = Question.objects.filter(category__id=category_id, category__is_active=True,
                                            is_active=True).order_by('?')[:5]

        time_start = timezone.now()
        formatted_time_start = time_start.strftime("%A, %B %d, %Y %I:%M %p")
        quiz = Quiz.objects.create(user_id=request.user.id, category_id=category_id,
                                   name=f" New Quiz - {formatted_time_start}",
                                   time_start=time_start, time_end=None)
        context = {'questions': questions, 'quiz_id': quiz.id}

        return render(request, self.template_name, context)


class QuizSubmitView(LoginRequiredMixin, View):
    template_name = 'quiz/quiz_submit.html'

    def post(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.time_end = timezone.now()
        quiz.save()

        for question_key, choice_id in request.POST.items():
            if question_key == 'csrfmiddlewaretoken':
                continue

            question_id = question_key.replace('question_', '')
            question = get_object_or_404(Question, id=question_id)
            user_choice = get_object_or_404(Choice, id=choice_id)

            QuizQuestion.objects.create(quiz=quiz, question=question, user_choice=user_choice)

        return redirect('home')


class QuizResultView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/quiz_result.html'
    context_object_name = 'quiz'

    def get_object(self, queryset=None):
        return get_object_or_404(Quiz, id=self.kwargs['quiz_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()

        # Prefetch for better performance
        quiz_questions = quiz.quizquestion_set.select_related('question', 'user_choice', 'question__category')

        context['quiz_questions'] = quiz_questions
        context['correct_answers'] = quiz.calculate_correct_answers()
        context['total_questions'] = quiz_questions.count()
        return context


class UserManagementView(TemplateView):
    template_name = 'quiz/user_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        return context


def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    return redirect('user_management')


def suspend_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_management')


def quiz_results(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    quizzes = user.quiz_set.all()
    return render(request, 'quiz/quiz_result_management.html', {'user': user, 'quizzes': quizzes})


class QuizResultManagementView(ListView):
    model = Quiz
    template_name = 'quiz/quiz_result_management.html'
    context_object_name = 'quiz_results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['users'] = CustomUser.objects.all()
        context['selected_category'] = self.request.GET.get('category_filter', '')
        context['selected_user'] = self.request.GET.get('user_filter', '')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_category = self.request.GET.get('category_filter', '')
        selected_user = self.request.GET.get('user_filter', '')

        user_id = self.kwargs.get('user_id')
        if user_id:
            return Quiz.objects.filter(user_id=user_id).order_by('-time_end')
        else:
            # Apply filters
            if selected_category:
                queryset = queryset.filter(category_id=selected_category)
            if selected_user:
                queryset = queryset.filter(user_id=selected_user)

        return queryset.order_by('-time_end')


class QuestionListView(ListView):
    model = Question
    template_name = 'quiz/question_list.html'
    context_object_name = 'questions'


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'quiz/question_detail.html'
    context_object_name = 'question'

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionUpdateForm
    template_name = 'quiz/question_update.html'
    success_url = reverse_lazy('question_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the question's existing choices
        existing_choices = Choice.objects.filter(question=self.object)

        # Create a formset with extra=0
        ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, can_delete=False, extra=0)
        # Exclude existing choices from the queryset
        context['choice_formset'] = ChoiceFormSet(instance=self.object, queryset=existing_choices)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        existing_choices = Choice.objects.filter(question=self.object)

        ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, can_delete=False, extra=0)
        choice_formset = ChoiceFormSet(request.POST, instance=self.object, queryset=existing_choices)

        if form.is_valid() and choice_formset.is_valid():
            return self.form_valid(form, choice_formset)
        else:
            return self.form_invalid(form, choice_formset)

    def form_valid(self, form, choice_formset):
        self.object = form.save()

        choice_formset.save()

        return redirect(self.get_success_url())

    def form_invalid(self, form, choice_formset):
        return self.render_to_response(self.get_context_data(form=form, choice_formset=choice_formset))


class QuestionCreateView(CreateView):
    model = Question
    template_name = 'quiz/question_create.html'
    fields = ['category', 'description', 'is_active']
    success_url = reverse_lazy('question_list')


class ToggleQuestionStatusView(View):
    def post(self, request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, pk=question_id)
        question.is_active = not question.is_active
        question.save()

        return redirect(reverse('question_list'))


class CategoryListView2(ListView):
    model = Category
    template_name = 'quiz/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'quiz/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryUpdateForm
    template_name = 'quiz/category_form.html'
    success_url = reverse_lazy('category_list')


class ToggleCategoryStatusView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.is_active = not category.is_active
        category.save()
        return HttpResponseRedirect(reverse('category_list'))
