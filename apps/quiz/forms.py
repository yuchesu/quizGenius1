from django import forms
from .models import Question, Choice, Category


class QuestionUpdateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'description', 'is_active']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['description', 'is_correct']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(ChoiceForm, self).__init__(*args, **kwargs)

        if question:
            self.fields['description'].queryset = question.choice_set.all()  # Filter choices based on the question
            self.fields['description'] = forms.ModelChoiceField(
                queryset=question.choice_set.all(),
                widget=forms.Select(attrs={'class': 'form-control'})
            )

            correct_choice = question.get_correct_choice()
            if correct_choice:
                self.fields['description'].initial = correct_choice
                self.fields['is_correct'].initial = correct_choice.is_correct


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_active']


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_active']
