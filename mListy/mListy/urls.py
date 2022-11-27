from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('mListy.account.urls')),
                  path('', include('mListy.list.urls')),
                  path('', include('mListy.list_entry.urls')),
                  path('', include('mListy.movie.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
