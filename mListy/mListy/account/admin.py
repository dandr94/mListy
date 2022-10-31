from django.contrib import admin

from mListy.account.models import Profile, mListyUser

admin.site.site_header = 'mListy Administration'


@admin.register(mListyUser)
class mListyUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_superuser', ]


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'facebook', 'instagram', 'twitter', 'website']

