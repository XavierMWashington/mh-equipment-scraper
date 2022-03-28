from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.greet),
    path('hrhelms/', views.highRankHelms),
    path('lrhelms/', views.lowRankHelms),
    path('hrchests/', views.highRankChests),
    path('lrchests/', views.lowRankChests),
    path('hrarms/', views.highRankArms),
    path('lrarms/', views.lowRankArms),
    path('hrwaists/', views.highRankWaists),
    path('lrwaists/', views.lowRankWaists),
    path('hrlegs/', views.highRankLegs),
    path('lrlegs/', views.lowRankLegs)
]