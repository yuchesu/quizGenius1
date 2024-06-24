from django.urls import path
from .views import CategoryListView, NewQuizView, QuizSubmitView, QuizResultView, UserManagementView, activate_user, \
    suspend_user, quiz_results, QuizResultManagementView, QuestionListView, QuestionDetailView, QuestionUpdateView, \
    QuestionCreateView, ToggleQuestionStatusView, CategoryListView2, ToggleCategoryStatusView, CategoryUpdateView, \
    CategoryCreateView

urlpatterns = [
    path("", CategoryListView.as_view(), name="home"),
    path('new_quiz/<int:category_id>/',NewQuizView.as_view(), name='quiz_new'),
    path('submit_quiz/<int:quiz_id>/', QuizSubmitView.as_view(), name='quiz_submit'),
    path('quiz_result/<int:quiz_id>/', QuizResultView.as_view(), name='quiz_result'),

    path('user_management/', UserManagementView.as_view(), name='user_management'),
    path('activate_user/<int:user_id>/', activate_user, name='activate_user'),
    path('suspend_user/<int:user_id>/', suspend_user, name='suspend_user'),
    path('quiz_results/<int:user_id>/', quiz_results, name='quiz_results'),
    path('quiz_result_management/', QuizResultManagementView.as_view(), name='quiz_result_management'),
    path('quiz_result_management/<int:user_id>/', QuizResultManagementView.as_view(), name='quiz_result_management_user'),

    path('question_list/', QuestionListView.as_view(), name='question_list'),
    path('question_detail/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question_update/<int:pk>/', QuestionUpdateView.as_view(), name='question_update'),
    path('question_create/', QuestionCreateView.as_view(), name='question_create'),
    path('toggle_question_status/<int:question_id>/', ToggleQuestionStatusView.as_view(), name='toggle_question_status'),

    path('category_list/', CategoryListView2.as_view(), name='category_list'),
    path('category_create/', CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('toggle_category_status/<int:pk>/', ToggleCategoryStatusView.as_view(), name='toggle_category_status'),
]