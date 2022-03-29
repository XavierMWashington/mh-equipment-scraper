from django.urls import path, re_path
from . import views

# URLConf
urlpatterns = [
    path('', views.greet),
    re_path(r'^(?P<slug>[\w-]+)/$', views.scrapeData)
]