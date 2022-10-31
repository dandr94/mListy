from django.contrib import admin

from mListy.list.models import List


@admin.register(List)
class List(admin.ModelAdmin):
    list_display = ['title', 'user']