"""
URL configuration for liferpg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shop/', views.shop, name='shop'),
    path('inventory/', views.inventory, name='inventory'),
    path('achievements/', views.achievements, name='achievements'),
    path('buy-item/<int:item_id>/', views.buy_item, name='buy_item'),
    path('create-quest/', views.create_quest, name='create_quest'),
    path('edit-quest/<int:quest_id>/', views.edit_quest, name='edit_quest'),
    path('delete-quest/<int:quest_id>/', views.delete_quest, name='delete_quest'),
    path('complete-quest/<int:quest_id>/', views.complete_quest, name='complete_quest'),
]

