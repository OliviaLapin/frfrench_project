from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CardForm
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_cards(category_filter=None):
    """Читает карточки из истории ваших сохранений"""
    cards = []
    file_path = os.path.join(BASE_DIR, 'data.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ';' in line:
                    parts = line.split(';')
                    if len(parts) >= 3:
                        category = parts[0]
                        russian = parts[1]
                        french = parts[2]
                        option_2 = parts[3] if len(parts) > 3 else "Неправильный вариант"
                        option_3 = parts[4] if len(parts) > 4 else "Другой вариант"
                        option_4 = parts[5] if len(parts) > 5 else "Ещё вариант"
                        
                        card = {
                            'category': category,
                            'russian': russian,
                            'french': french,
                            'option_2': option_2,
                            'option_3': option_3,
                            'option_4': option_4,
                        }
                        if category_filter is None or category == category_filter:
                            cards.append(card)
    except FileNotFoundError:
        pass
    return cards

def save_card(category, russian_word, french_word, option_2, option_3, option_4):
    """Добавляет новую карточку в файл"""
    file_path = os.path.join(BASE_DIR, 'data.txt')
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"\n{category};{russian_word};{french_word};{option_2};{option_3};{option_4}")
    return True

def home(request):
    return render(request, 'french/home.html')

def topics_list(request):
    topics = [
        {'id': 1, 'name': 'Еда', 'description': 'Фрукты, овощи, блюда'},
        {'id': 2, 'name': 'Животные', 'description': 'Домашние и дикие животные'},
        {'id': 3, 'name': 'Семья', 'description': 'Члены семьи'},
        {'id': 4, 'name': 'Путешествия', 'description': 'Транспорт, направления'},
    ]
    return render(request, 'french/topics.html', {'topics': topics})

@login_required
def quiz(request, topic_id):
    topics = {
        1: 'Еда', 
        2: 'Животные', 
        3: 'Семья', 
        4: 'Путешествия',
        5: 'Все категории'
    }
    topic_name = topics.get(topic_id, 'Французский')
    
 
    if topic_id == 5:
        cards = read_cards(category_filter=None)  
    else:
        cards = read_cards(category_filter=topic_name)  
    
    
    if request.method == 'POST':
        score = 0
        total = len(cards)
        unanswered = 0
        
        for i, card in enumerate(cards):
            user_answer = request.POST.get(f'q_{i}')
            if not user_answer:
                unanswered += 1
            elif user_answer.strip().lower() == card['french'].lower():
                score += 1
        
        percent = int(score / total * 100) if total > 0 else 0
        
        return render(request, 'french/result.html', {
            'score': score,
            'total': total,
            'percent': percent,
            'topic_name': topic_name,
            'topic_id': topic_id,
            'unanswered': unanswered,
        })
    
 
    return render(request, 'french/quiz.html', {
        'cards': cards,
        'topic_name': topic_name,
        'topic_id': topic_id
    })
@login_required
def card_add(request):
    """Страница с формой добавления карточки"""
    return render(request, 'french/card_add.html', {'form': CardForm()})

@login_required
def edit_card(request, card_id):
    """Страница с формой редактирования карточки"""
    return render(request, 'french/card_add.html', {'form': CardForm(), 'edit_mode': True})

@login_required
def send_card(request):
    """Обработка отправленной формы"""
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['topic']
            russian_word = form.cleaned_data['question']
            french_word = form.cleaned_data['correct_answer']
            option_2 = form.cleaned_data['option_2']
            option_3 = form.cleaned_data['option_3']
            option_4 = form.cleaned_data['option_4']
            
            save_card(category, russian_word, french_word, option_2, option_3, option_4)
            
            return render(request, 'french/card_result.html', {
                'success': True,
                'user': request.user.username,
                'comment': f'Карточка "{russian_word}" → "{french_word}" добавлена в категорию "{category}"!'
            })
        else:
            return render(request, 'french/card_result.html', {
                'success': False,
                'user': request.user.username,
                'comment': f'Ошибка валидации. Проверьте правильность заполнения полей: {form.errors}'
            })
    return redirect('french:card_add')

@login_required
def stats(request):
    cards = read_cards()
    total = len(cards)
    lengths = [len(card['russian']) + len(card['french']) for card in cards]
    avg_len = sum(lengths) // total if total > 0 else 0
    max_len = max(lengths) if lengths else 0
    min_len = min(lengths) if lengths else 0
    
    return render(request, 'french/stats.html', {
        'total_cards': total,
        'avg_length': avg_len,
        'max_length': max_len,
        'min_length': min_len,
    })