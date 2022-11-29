from django.contrib import admin

from mListy.list.models import List
from mListy.list_entry.models import ListEntry


@admin.register(List)
class List(admin.ModelAdmin):
    list_display = ['title', 'user']


@admin.register(ListEntry)
class ListEntry(admin.ModelAdmin):
    list_display = ['grade', 'would_recommend', 'list']

