"""chemie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django_nyt.urls import get_pattern as get_nyt_pattern
from wiki.urls import get_pattern as get_wiki_pattern


urlpatterns = [
    url(r'^valg/', include('elections.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('home.urls'), name='frontpage'),
    url(r'^shitbox/', include('shitbox.urls')),
    url(r'^verv/', include('committees.urls')),
    url(r'^bokskap/', include('lockers.urls', namespace='bokskap')),
    url(r'^klassekatalog/', include('yearbook.urls')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^calendar/', include('webcalendar.urls')),
    url(r'^profile/', include('customprofile.urls')),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout, {'next_page': '/'}),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^notifications/', get_nyt_pattern()),
    url(r'^wiki/', get_wiki_pattern()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
