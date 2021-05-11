from django.contrib import admin

# Register your models here.
from .models import Profile
from .forms import ProfileForm
from .models import Deadline


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm


@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'difficulty', 'task')