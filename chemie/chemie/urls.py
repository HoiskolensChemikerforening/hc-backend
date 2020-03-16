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
import django.contrib.auth.views as auth_views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django_nyt.urls import get_pattern as get_nyt_pattern
from wiki.urls import get_pattern as get_wiki_pattern
from ..customprofile.views import LoginView

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^", include("chemie.home.urls", namespace="frontpage")),
    url(r"^sladreboks/", include("chemie.shitbox.urls", namespace="shitbox")),
    url(r"^verv/", include("chemie.committees.urls", namespace="verv")),
    url(r"^bokskap/", include("chemie.lockers.urls", namespace="bokskap")),
    url(r"^news/", include("chemie.news.urls", namespace="news")),
    url(r"^", include("chemie.customprofile.urls", namespace="profile")),
    url(r"^login/$", LoginView.as_view(), name="login"),
    url(
        r"^logout/$",
        auth_views.LogoutView.as_view(),
        {"next_page": "/"},
        name="logout",
    ),
    url(r"^events/", include("chemie.events.urls", namespace="events")),
    url(r"^notifications/", include("django_nyt.urls")),
    url(r"^wiki/_accounts/sign-up/", LoginView.as_view()),
    url(r"^wiki/", include("wiki.urls")),
    url(
        r"^api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    url(r"^chaining/", include("smart_selects.urls")),
    url(
        r"^bilder/",
        include("chemie.picturecarousel.urls", namespace="carousel"),
    ),
    url(r"^valg/", include("chemie.elections.urls", namespace="elections")),
    url(r"^web_push/", include("chemie.web_push.urls", namespace="web_push")),
    url(r"^butikk/", include("chemie.shop.urls", namespace="shop")),
    url(r"^quiz/", include("chemie.quiz.urls", namespace="quiz")),
    url(
        r"^utleie/",
        include("chemie.rentalservice.urls", namespace="rentalservice"),
    ),
]

handler404 = "chemie.chemie.views.page_not_found"

urlpatterns += [
    url(
        r"^s/",
        include(
            ("django.contrib.flatpages.urls", "flatpages"),
            namespace="flatpages",
        ),
    )
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += staticfiles_urlpatterns()

    from chemie.chemie.views import page_not_found
    from django.views.defaults import server_error

    urlpatterns += [url(r"test404", page_not_found, name="404")]
    urlpatterns += [url(r"test500", server_error, name="404")]

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls))]
