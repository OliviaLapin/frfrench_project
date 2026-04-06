from django import forms

class CardForm(forms.Form):
    topic = forms.CharField(
        label='Тема',
        max_length=100,
        error_messages={
            'required': 'Пожалуйста, укажите тему',
            'max_length': 'Название темы не может быть длиннее 100 символов'
        }
    )
    question = forms.CharField(
        label='Вопрос (по-французски)',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите вопрос',
            'max_length': 'Вопрос не может быть длиннее 200 символов'
        }
    )
    correct_answer = forms.CharField(
        label='Правильный ответ',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите правильный ответ',
            'max_length': 'Ответ не может быть длиннее 200 символов'
        }
    )
    option_2 = forms.CharField(
        label='Вариант 2',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите вариант 2',
            'max_length': 'Вариант не может быть длиннее 200 символов'
        }
    )
    option_3 = forms.CharField(
        label='Вариант 3',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите вариант 3',
            'max_length': 'Вариант не может быть длиннее 200 символов'
        }
    )
    option_4 = forms.CharField(
        label='Вариант 4',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите вариант 4',
            'max_length': 'Вариант не может быть длиннее 200 символов'
        }
    )
    
    def clean_question(self):
        q = self.cleaned_data.get('question', '')
        if len(q.strip()) < 3:
            raise forms.ValidationError('Вопрос слишком короткий (минимум 3 символа)')
        if not q.strip():
            raise forms.ValidationError('Вопрос не может быть пустым')
        return q.strip()
    
    def clean_correct_answer(self):
        answer = self.cleaned_data.get('correct_answer', '')
        if len(answer.strip()) < 1:
            raise forms.ValidationError('Правильный ответ не может быть пустым')
        return answer.strip()
    
    def clean_option_2(self):
        opt = self.cleaned_data.get('option_2', '')
        if len(opt.strip()) < 1:
            raise forms.ValidationError('Вариант 2 не может быть пустым')
        return opt.strip()
    
    def clean_option_3(self):
        opt = self.cleaned_data.get('option_3', '')
        if len(opt.strip()) < 1:
            raise forms.ValidationError('Вариант 3 не может быть пустым')
        return opt.strip()
    
    def clean_option_4(self):
        opt = self.cleaned_data.get('option_4', '')
        if len(opt.strip()) < 1:
            raise forms.ValidationError('Вариант 4 не может быть пустым')
        return opt.strip()
    
    def clean(self):
        cleaned_data = super().clean()
        correct = cleaned_data.get('correct_answer', '').strip().lower()
        opt2 = cleaned_data.get('option_2', '').strip().lower()
        opt3 = cleaned_data.get('option_3', '').strip().lower()
        opt4 = cleaned_data.get('option_4', '').strip().lower()
        
        # Проверка, что правильный ответ не совпадает с другими вариантами
        if correct and (correct == opt2 or correct == opt3 or correct == opt4):
            raise forms.ValidationError('Правильный ответ не должен совпадать с другими вариантами')
        
        # Проверка, что все варианты разные
        options = [opt2, opt3, opt4]
        if len(set(options)) != len(options):
            raise forms.ValidationError('Все варианты ответа должны быть разными')
        
        return cleaned_data