import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Kanji
from .models import SavedKanji
from django.shortcuts import get_object_or_404
from .forms import ProfileForm
from .models import Profile


# 🏠 Home page (guest + user)
def home(request):
    return render(request, 'home.html')


# 📝 Register page
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Username шалгах
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {
                'error': 'Username аль хэдийн байна'
            })

        # User үүсгэх
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Шууд login хийх
        login(request, user)
        return redirect('home')

    return render(request, 'registration/register.html')


# 🈶 Flashcards (login required)
@login_required
def flashcards(request):
    level = request.GET.get('level', 'N5')

    kanjis = list(
        Kanji.objects.filter(level=level).order_by('id')
    )

    if not kanjis:
        return render(request, 'flashcards/flashcard.html', {'kanji': None})

    index = request.session.get('kanji_index', 0)
    session_level = request.session.get('kanji_level')

    # level солигдвол index reset
    if session_level != level:
        index = 0
        request.session['kanji_level'] = level

    action = request.GET.get('action')

    if action == 'next' and index < len(kanjis) - 1:
        index += 1
    elif action == 'back' and index > 0:
        index -= 1

    request.session['kanji_index'] = index

    kanji = kanjis[index]

    is_saved = SavedKanji.objects.filter(
        user=request.user,
        kanji=kanji
    ).exists()

    return render(request, 'flashcards/flashcard.html', {
        'kanji': kanji,
        'level': level,
        'is_saved': is_saved,
        'can_go_back': index > 0,
        'can_go_next': index < len(kanjis) - 1,
        'position': f"{index + 1} / {len(kanjis)}"
    })


    
    
@login_required
def toggle_save_kanji(request, kanji_id):
    kanji = get_object_or_404(Kanji, id=kanji_id)
    
    level = request.POST.get('level', 'N5')

    saved = SavedKanji.objects.filter(user=request.user, kanji=kanji)

    if saved.exists():
        saved.delete()
    else:
        SavedKanji.objects.create(user=request.user, kanji=kanji)

    return redirect(f'/flashcards/?level={level}')


# 👤 My Account page
@login_required
def account(request):
    from .models import Profile
    
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )
    
    saved = SavedKanji.objects.filter(
        user=request.user
    ).select_related('kanji')
    
    return render(request, 'flashcards/account.html', {
        'profile': profile,
        'saved_kanji': saved
    })
    
@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'flashcards/edit_profile.html', {
        'form': form
    })



# 🚪 Logout
def logout_view(request):
    logout(request)
    return redirect('home')

def logout_success(request):
    return render(request, 'registration/logout.html')
