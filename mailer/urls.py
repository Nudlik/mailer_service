from django.urls import path

from mailer import apps, views

app_name = apps.MailerConfig.name

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('send/', views.SendView.as_view(), name='send'),

    path('message/list', views.MessageListView.as_view(), name='message_list'),
    path('message/create', views.MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>', views.MessageDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/update', views.MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete', views.MessageDeleteView.as_view(), name='message_delete'),
]
