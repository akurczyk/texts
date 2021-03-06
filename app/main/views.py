from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now

from .forms import TextModelForm
from .models import Text
from .tasks import process_text


def show_texts(request, site_id, all_texts, page_id, author=None):
    paginator = Paginator(all_texts, 10)
    texts = paginator.get_page(page_id)
    last_page_id = paginator.num_pages
    current_page_id = page_id if 1 <= page_id <= last_page_id else last_page_id

    context = {
        'texts': texts,
        'show_prev_pg': True if current_page_id > 1 else False,
        'show_next_pg': True if current_page_id < last_page_id else False,
        'prev_pg_id': current_page_id - 1,
        'next_pg_id': current_page_id + 1,
        'author': author,
    }

    return render(request, 'main/texts.html', context)


def index(request, page_id=1):
    all_texts = Text.objects\
        .filter(processed=True)\
        .filter(published=True)\
        .order_by('-id')

    return show_texts(request, 'index', all_texts, page_id)


def waiting(request, page_id=1):
    all_texts = Text.objects\
        .filter(processed=True)\
        .filter(published=False)\
        .order_by('-id')

    return show_texts(request, 'waiting', all_texts, page_id)


def best(request, page_id=1):
    all_texts = Text.objects\
        .filter(processed=True)\
        .filter(published=True)\
        .annotate(votes_count=Coalesce(Sum('vote__vote'), 0))\
        .order_by('-votes_count')

    return show_texts(request, 'best', all_texts, page_id)


def user_texts(request, user_id, page_id=1):
    print(user_id)
    author = get_object_or_404(User, pk=user_id)

    all_texts = Text.objects\
        .filter(processed=True)\
        .filter(published=True)\
        .filter(author=user_id)\
        .annotate(votes_count=Coalesce(Sum('vote__vote'), 0))\
        .order_by('-id')

    return show_texts(request, 'user_texts', all_texts, page_id, author)


def random_text(request):
    all_texts = Text.objects\
        .filter(processed=True)\
        .filter(published=True)\
        .order_by('?')

    if all_texts.count() == 0:
        return HttpResponseNotFound()

    random_text_id = all_texts.first().id

    return redirect('show', text_id=random_text_id)


def show(request, text_id):
    text = get_object_or_404(Text, pk=text_id)

    can_edit = request.user.has_perm('main.edit_text')\
               or (request.user == text.author and not text.published)
    can_remove = request.user.has_perm('main.remove_text')\
               or (request.user == text.author and not text.published)
    can_publish = text.published == False and request.user.has_perm('main.publish_text')
    can_unpublish = text.published == True and request.user.has_perm('main.unpublish_text')

    context = {
        'text': text,
        'can_edit': can_edit,
        'can_remove': can_remove,
        'can_publish': can_publish,
        'can_unpublish': can_unpublish,
        'author': text.author,
    }

    return render(request, 'main/text.html', context)


def vote(request, plus_or_minus, text_id):
    if plus_or_minus not in ('plus', 'minus'):
        return HttpResponseNotFound('You can only vote on plus or minus')

    if not request.user.is_authenticated:
        return HttpResponseForbidden('You need to log in before voting')

    text = get_object_or_404(Text, pk=text_id)

    if plus_or_minus == 'plus': text.upvote(request.user)
    else: text.downvote(request.user)

    return HttpResponse(text.votes)


@login_required
def add(request):
    if request.method == 'POST':
        form = TextModelForm(request.POST)
    else:
        form = TextModelForm()

    submitted = False
    if form.is_valid():
        text = form.save(commit=False)
        text.author = User.objects.get(id=request.user.id)
        text.save()
        process_text.delay(text.id)
        submitted = True

    context = {
        'form': form,
        'submitted': submitted,
    }

    return render(request, 'main/add.html', context)


@login_required
def edit(request, text_id):
    text = get_object_or_404(Text, pk=text_id)

    no_rights = False
    submitted = False

    if not request.user.has_perm('main.edit_text')\
            and not (request.user == text.author and not text.published):
        no_rights = True

    if request.method == 'POST':
        form = TextModelForm(request.POST, instance=text)
    else:
        form = TextModelForm(instance=text)

    if not no_rights and form.is_valid():
        text = form.save(commit=False)
        text.updated = True
        text.updated_at = now()
        text.save()

        FileSystemStorage().delete(text.file_name)
        FileSystemStorage().delete(text.file_name_mini)

        process_text.delay(text.id)
        submitted = True

    context = {
        'form': form,
        'submitted': submitted,
        'no_rights': no_rights,
    }

    return render(request, 'main/edit.html', context)


@login_required
def publish(request, text_id):
    text = get_object_or_404(Text, pk=text_id)

    if request.user.has_perm('main.publish_text'):
        text.publish()

    return redirect('show', text_id)


@login_required
def unpublish(request, text_id):
    text = get_object_or_404(Text, pk=text_id)

    if request.user.has_perm('main.unpublish_text'):
        text.unpublish()

    return redirect('show', text_id)


@login_required
def remove(request, text_id):
    text = get_object_or_404(Text, pk=text_id)

    if request.user.has_perm('main.remove_text')\
            or (request.user == text.author and not text.published):
        FileSystemStorage().delete(text.file_name)
        FileSystemStorage().delete(text.file_name_mini)
        text.delete()

    return redirect('index')
