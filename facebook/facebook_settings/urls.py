"""facebook URL Configuration."""

# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include(('app.users.urls', 'users'), namespace='users')),
    path('', include(('app.posts.urls', 'posts'), namespace='posts')),
    path('', include(('app.groups.urls', 'groups'), namespace='groups')),
    path('', include(('app.fbpages.urls', 'pages'), namespace='pages')),
    path('', include(('app.chats.urls', 'chats'), namespace='chats'))
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
