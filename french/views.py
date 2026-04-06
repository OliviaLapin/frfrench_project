from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CardForm
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_cards():
    """Читает карточки из файла data.txt"""
    cards = []
    file_path = os.path.join(BASE_DIR, 'data.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ';' in line:
                    russian, french = line.split(';', 1)
                    cards.append({
                        'russian': russian,
                        'french': french,
                    })
    except FileNotFoundError:
        pass
    return cards

def save_card(russian_word, french_word):
    """Добавляет новую карточку в файл"""
    file_path = os.path.join(BASE_DIR, 'data.txt')
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"\n{russian_word};{french_word}")
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
    cards = read_cards()
    topics = {
        1: 'Еда', 2: 'Животные', 3: 'Семья', 4: 'Путешествия'
    }
    topic_name = topics.get(topic_id, 'Французский')
    
    if request.method == 'POST':
        score = 0
        total = len(cards)
        for i, card in enumerate(cards):
            user_answer = request.POST.get(f'q_{i}')
            if user_answer and user_answer.strip().lower() == card['french'].lower():
                score += 1
        percent = int(score / total * 100) if total > 0 else 0
        return render(request, 'french/result.html', {
            'score': score,
            'total': total,
            'percent': percent,
            'topic_name': topic_name,
            'topic_id': topic_id
        })
    
    return render(request, 'french/quiz.html', {
        'cards': cards,
        'topic_name': topic_name,
        'topic_id': topic_id
    })

@login_required
def add_card(request):
    return render(request, 'french/card_add.html', {'form': CardForm()})

@login_required
def edit_card(request, card_id):
    return render(request, 'french/card_add.html', {'form': CardForm(), 'edit_mode': True})

@login_required
def send_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            russian_word = form.cleaned_data['question']
            french_word = form.cleaned_data['correct_answer']
            save_card(russian_word, french_word)
            return render(request, 'french/card_result.html', {
                'success': True,
                'user': request.user.username,
                'comment': f'Карточка "{russian_word}" → "{french_word}" успешно добавлена!'
            })
        else:
            return render(request, 'french/card_result.html', {
                'success': False,
                'user': request.user.username,
                'comment': f'Ошибка валидации: {form.errors}'
            })
    return redirect('french:add_card')

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
