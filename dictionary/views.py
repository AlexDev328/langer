from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from .forms import WordForm, WordCardCreate, FilterBard, TrainingSettings
from django.db.models import Q

from .models import WordCard, Word, WordCardProgress, Language
import random


@login_required
def mycards(request):
    filter_bar = FilterBard()
    query = Q(owner=request.user) | Q(is_public=True)

    if language := request.GET.get('text_language'):
        filter_bar.initial['text_language'] = language
        query = query & Q(word__language_id=language)

    cards_list = WordCard.objects.filter(query).order_by('id')
    paginator = Paginator(cards_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = WordCardCreate()

    return render(request, "mycards.html", context={"cards": page_obj, "form": form, 'filter': filter_bar})

@login_required
def index(request):
    return render(request, "index.html")


@login_required
def create_new_wordcard(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WordCardCreate(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data)
            data = form.cleaned_data
            word, _ = Word.objects.get_or_create(text=data['text'], language=data['text_language'])
            translation, _ = Word.objects.get_or_create(text=data['translation'], language=data['translation_language'])

            wordcard, _ = WordCard.objects.get_or_create(word=word, translation=translation,
                                                         description=data['description'], example=data['example'],
                                                         is_public=data['is_public'], owner=request.user)

            if data['group']:
                wordcard.cardgroup_set.add(data['group'])
            return HttpResponseRedirect('/mycardstest/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = WordCardCreate()

    return render(request, 'create_new.html', {'form': form})


class AnswerOption:
    word: Word
    is_correct: bool

    def __init__(self, word: Word, is_correct: bool) -> None:
        self.word = word
        self.is_correct = is_correct


class Task:
    card: WordCard
    answers: list[AnswerOption]

    def __init__(self, card: WordCard, answers: list[AnswerOption]) -> None:
        self.card = card
        self.answers = answers

@login_required
def start_training(request) -> list[Task]:
    user = request.user
    language = request.GET.get('language')
    task_count = request.GET.get('task_count')
    query = (Q(owner=user) | Q(is_public=True)) \
            & Q(word__language=language) \
            & (Q(wordcardprogress=None) | Q(wordcardprogress__user=user))
    word_cards = WordCard.objects.filter(query).order_by('wordcardprogress__score').limit(task_count)
    tasks = [prepare_task(card, user) for card in word_cards]
    return tasks


def prepare_task(card: WordCard, user) -> Task:
    answers = [AnswerOption(card.translation, True)]
    random_words = get_random_words(user, card.translation.language, card.translation.id, 3)
    for word in random_words:
        answer = AnswerOption(word, False)
        answers.append(answer)
    return Task(card, answers)


#todo: should be atomic
#todo: make model manager and add WordCard.visible = WordCard.objects.filter(Q(user=user) | Q(is_public=True))
def get_random_words(user, language: Language, except_id, count: int):
    condition = (Q(user=user) | Q(is_public=True)) & Q(language=language) & Q(id=except_id, _negated=True)
    query = WordCard.objects.filter(condition)
    card_count = query.count()
    if card_count <= count:
        return query.all()
    random_indexes = random.sample(range(0, card_count), k=count)
    random_words = [query.order_by('id').offset(random_int).limit(1).first() for random_int in random_indexes]
    return random_words
