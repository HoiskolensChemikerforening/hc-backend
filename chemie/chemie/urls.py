"""chemie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path("blog/", include('blog.urls'))
"""
import django.contrib.auth.views as auth_views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from ..customprofile.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chemie.home.urls", namespace="frontpage")),
    path("sladreboks/", include("chemie.shitbox.urls", namespace="shitbox")),
    path("verv/", include("chemie.committees.urls", namespace="verv")),
    path("bokskap/", include("chemie.lockers.urls", namespace="bokskap")),
    path("nyheter/", include("chemie.news.urls", namespace="news")),
    path("", include("chemie.customprofile.urls", namespace="profile")),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        {"next_page": "/"},
        name="logout",
    ),
    path("arrangementer/", include("chemie.events.urls", namespace="events")),
    path("notifications/", include("django_nyt.urls")),
    path("wiki/_accounts/sign-up/", LoginView.as_view()),
    path("wiki/", include("wiki.urls")),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    path("chaining/", include("smart_selects.urls")),
    path(
        "bilder/",
        include("chemie.picturecarousel.urls", namespace="carousel"),
    ),
    path("valg/", include("chemie.elections.urls", namespace="elections")),
    path(
        "push-notifikasjoner/",
        include("chemie.web_push.urls", namespace="web_push"),
    ),
    path("kontoret/", include("chemie.shop.urls", namespace="shop")),
    path("quiz/", include("chemie.quiz.urls", namespace="quiz")),
]

handler404 = "chemie.chemie.views.page_not_found"

urlpatterns += [
    path(
        "s/",
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

    urlpatterns += [
        path("test404", page_not_found, name="404"),
        path("test500", server_error, name="404"),
    ]

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
