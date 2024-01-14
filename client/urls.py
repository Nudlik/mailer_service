from django.urls import path

from client import apps, views

app_name = apps.ClientConfig.name

urlpatterns = [
    path('client/list', views.ClientListView.as_view(), name='client_list'),
    path('client/create', views.ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>', views.ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/update', views.ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete', views.ClientDeleteView.as_view(), name='client_delete'),
]
