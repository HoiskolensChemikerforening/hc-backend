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

from . import views
from ..customprofile.views import LoginView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from chemie.home.views import index, UserPermissionView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chemie.home.urls", namespace="frontpage")),
    # Temporary url for front page during Fadderperioden
    path("forside/", index),
    path("sladreboks/", include("chemie.shitbox.urls", namespace="shitbox")),
    path("undergrupper/", include("chemie.committees.urls", namespace="verv")),
    path("bokskap/", include("chemie.lockers.urls", namespace="bokskap")),
    path("bedrift/", include("chemie.corporate.urls", namespace="corporate")),
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
        "bilder/", include("chemie.picturecarousel.urls", namespace="carousel")
    ),
    path("valg/", include("chemie.elections.urls", namespace="elections")),
    path("web_push/", include("chemie.web_push.urls", namespace="web_push")),
    path("kontoret/", include("chemie.shop.urls", namespace="shop")),
    path("quiz/", include("chemie.quiz.urls", namespace="quiz")),
    path(
        "sugepodden/",
        include("chemie.sugepodden.urls", namespace="sugepodden"),
    ),
    path(
        "utleie/",
        include("chemie.rentalservice.urls", namespace="rentalservice"),
    ),
    path("cgp/",include("chemie.cgp.urls", namespace="cgp")),
    path("valgomat/",include("chemie.electofood.urls", namespace="valgomat")),
    path("reisebrev/", include("chemie.exchangepage.urls", namespace="reisebrev")),
    # For authentication
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/permissions/", UserPermissionView.as_view(), name="permissions"),
    path("api/404/", views.pictures_for_404ListCreate.as_view(), name="404"),
    path("api/sponsor/", views.SponsorListCreate.as_view(), name="sponsor"),
    path("api/404/<int:pk>/", views.pictures_for_404Detail.as_view()),
    path("api/sponsor/<int:pk>/", views.SponsorDetail.as_view()),
    path("merch/", include("chemie.merch.urls", namespace="merch")),
    path("refusjon/", include("chemie.refund.urls", namespace="refund")),
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
