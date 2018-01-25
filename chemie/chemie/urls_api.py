from django.conf.urls import url
from django.conf.urls import include


api_urlpatterns = [
    url(r'^api/sladreboks/', include('shitbox.api.urls', namespace='shitbox-api')),
]

#api_urlpatterns = format_suffix_patterns(api_urlpatterns)
