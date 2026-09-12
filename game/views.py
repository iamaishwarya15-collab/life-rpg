from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Character,Quest,ShopItem,InventoryItem,Achievement


def home(request):
    return render(request, 'game/home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'game/signup.html', {
                'error': 'Username already exists. Please choose another one.'
            })
        
        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'game/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'game/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'game/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    character, created = Character.objects.get_or_create(user=request.user)
    quests = Quest.objects.filter(user=request.user)

    return render(request, 'game/dashboard.html', {
        'character': character,
        'quests': quests
    })
@login_required
def create_quest(request):
    if request.method == 'POST':
        Quest.objects.create(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            category=request.POST['category'],
            xp_reward=10,
            gold_reward=5
        )

        return redirect('dashboard')

    return render(request, 'game/create_quest.html')

@login_required
def edit_quest(request, quest_id):
    quest = Quest.objects.get(
        id=quest_id,
        user=request.user
    )

    if request.method == 'POST':
        quest.title = request.POST['title']
        quest.description = request.POST['description']
        quest.category = request.POST['category']
        quest.save()

        return redirect('dashboard')

    return render(request, 'game/edit_quest.html', {
        'quest': quest
    })

@login_required
def delete_quest(request, quest_id):
    quest = Quest.objects.get(
        id=quest_id,
        user=request.user
    )

    if request.method == 'POST':
        quest.delete()

    return redirect('dashboard')

@login_required
def shop(request):
    items = ShopItem.objects.all()

    return render(request, 'game/shop.html', {
        'items': items
    })

@login_required
def buy_item(request, item_id):
    item = ShopItem.objects.get(id=item_id)
    character = Character.objects.get(user=request.user)

    if request.method == 'POST':
        if character.gold >= item.price:
            character.gold -= item.price
            character.save()

            inventory, created = InventoryItem.objects.get_or_create(
                user=request.user,
                item=item
            )

            if not created:
                inventory.quantity += 1
                inventory.save()

    return redirect('shop')

@login_required
def inventory(request):
    items = InventoryItem.objects.filter(user=request.user)

    return render(request, 'game/inventory.html', {
        'items': items
    })

@login_required
def achievements(request):
    achievements = Achievement.objects.filter(user=request.user)

    return render(request, 'game/achievement.html', {
        'achievements': achievements
    })

@login_required
def complete_quest(request, quest_id):

    if request.method != 'POST':
        return redirect('dashboard')
    
    quest = Quest.objects.get(
        id=quest_id,
        user=request.user
    )

    if not quest.completed:
        quest.completed = True
        quest.save()

        character, created = Character.objects.get_or_create(
           user=request.user
        )

        character.xp += quest.xp_reward
        character.gold += quest.gold_reward

        xp_needed = int(100 * (character.level ** 1.5))

        while character.xp >= xp_needed:
          character.xp -= xp_needed
          character.level += 1
          xp_needed = int(100 * (character.level ** 1.5))

        if quest.category == "Coding":
           character.intelligence += 1

        elif quest.category == "Study":
           character.wisdom += 1

        elif quest.category == "Exercise":
           character.strength += 1

        elif quest.category == "Creativity":
           character.creativity += 1

        from datetime import date, timedelta

        today = date.today()

        if character.last_completed_date == today:
           pass
        elif character.last_completed_date == today - timedelta(days=1):
           character.streak += 1
        else:
           character.streak = 1

        character.last_completed_date = today

        character.save()

        Achievement.objects.get_or_create(
          user=request.user,
          name="First Quest",
          defaults={
            "description": "Complete your first quest.",
            "unlocked": True
    }
)

    return redirect('dashboard')
