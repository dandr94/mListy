from django.contrib import admin

from mListy.list.models import List, ListEntry


@admin.register(List)
class List(admin.ModelAdmin):
    list_display = ['title', 'user']


@admin.register(ListEntry)
class ListEntry(admin.ModelAdmin):
    list_display = ['grade', 'would_recommend', 'list']

