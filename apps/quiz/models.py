from django.db import models

from apps import accounts


# class User(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField()
#     password = models.CharField(max_length=255)
#     firstname = models.CharField(max_length=255)
#     lastname = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     phone = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_ongoing_quiz(self):
        return Quiz.objects.filter(category=self, time_end=None).first()


class Quiz(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    def calculate_correct_answers(self):
        quiz_questions = QuizQuestion.objects.filter(quiz=self)
        correct_answers = 0

        for quiz_question in quiz_questions:
            correct_choice = Choice.objects.filter(question=quiz_question.question, is_correct=True).first()

            if correct_choice and correct_choice == quiz_question.user_choice:
                correct_answers += 1

        return correct_answers

    @property
    def passed(self):
        return self.calculate_correct_answers() > 3


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    def get_correct_choice(self):
        return self.choice_set.filter(is_correct=True).first()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quiz.name} : {self.question.description}"
