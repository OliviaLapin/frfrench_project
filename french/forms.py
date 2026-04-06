from django import forms

class CardForm(forms.Form):
    topic = forms.CharField(label='Тема', max_length=100)
    question = forms.CharField(label='Вопрос (по-французски)', max_length=200)
    correct_answer = forms.CharField(label='Правильный ответ', max_length=200)
    option_2 = forms.CharField(label='Вариант 2', max_length=200)
    option_3 = forms.CharField(label='Вариант 3', max_length=200)
    option_4 = forms.CharField(label='Вариант 4', max_length=200)
    
    def clean_question(self):
        q = self.cleaned_data['question']
        if len(q) < 3:
            raise forms.ValidationError('Вопрос слишком короткий (минимум 3 символа)')
        return q
