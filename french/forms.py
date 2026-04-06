from django import forms

CATEGORY_CHOICES = [
    ('Еда', 'Еда'),
    ('Животные', 'Животные'),
    ('Семья', 'Семья'),
    ('Путешествия', 'Путешествия'),
    ('Другое', '➕ Создать новую категорию'),
]

class CardForm(forms.Form):
    topic = forms.ChoiceField(
        label='Категория',
        choices=CATEGORY_CHOICES,
        error_messages={
            'required': 'Пожалуйста, выберите категорию',
        }
    )
    
    new_topic = forms.CharField(
        label='Название новой категории',
        required=False,
        max_length=100,
        help_text='Заполните, если выбрали "Создать новую категорию"',
        error_messages={
            'max_length': 'Название категории не может быть длиннее 100 символов'
        }
    )
    
    question = forms.CharField(
        label='Слово на русском',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите слово на русском',
            'max_length': 'Слово не может быть длиннее 200 символов'
        }
    )
    
    correct_answer = forms.CharField(
        label='Перевод на французский (правильный ответ)',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите перевод',
            'max_length': 'Перевод не может быть длиннее 200 символов'
        }
    )
    
    option_2 = forms.CharField(
        label='Вариант ответа 2 (неправильный)',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите вариант 2',
            'max_length': 'Вариант не может быть длиннее 200 символов'
        }
    )
    
    option_3 = forms.CharField(
        label='Вариант ответа 3 (неправильный)',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите вариант 3',
            'max_length': 'Вариант не может быть длиннее 200 символов'
        }
    )
    
    option_4 = forms.CharField(
        label='Вариант ответа 4 (неправильный)',
        max_length=200,
        error_messages={
            'required': 'Пожалуйста, введите вариант 4',
            'max_length': 'Вариант не может быть длиннее 200 символов'
        }
    )
    
    def clean_question(self):
        q = self.cleaned_data.get('question', '')
        if len(q.strip()) < 2:
            raise forms.ValidationError('Слово слишком короткое (минимум 2 символа)')
        if not q.strip():
            raise forms.ValidationError('Слово не может быть пустым')
        return q.strip()
    
    def clean_correct_answer(self):
        answer = self.cleaned_data.get('correct_answer', '')
        if len(answer.strip()) < 1:
            raise forms.ValidationError('Перевод не может быть пустым')
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
        topic = cleaned_data.get('topic')
        new_topic = cleaned_data.get('new_topic', '').strip()
        
        # Если выбрано "Другое", используем новую тему
        if topic == 'Другое':
            if not new_topic:
                raise forms.ValidationError('Если выбрали "Создать новую категорию", укажите её название')
            cleaned_data['topic'] = new_topic
        
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