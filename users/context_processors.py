def menu(request):
    menu_list = [
        {'title': 'Главная', 'url_name': 'mailer:home'},
        {'title': 'Рассылки',
         'submenu': [
             {'title': 'Клиенты', 'url_name': 'client:client_list'},
             {'title': 'Добавить клиента', 'url_name': 'client:client_create'},
             {'title': 'Сообщения', 'url_name': 'mailer:message_list'},
             {'title': 'Добавить сообщение', 'url_name': 'mailer:message_create'},
             {'title': 'Рассылки', 'url_name': 'mailer:settings_list'},
             {'title': 'Добавить рассылку', 'url_name': 'mailer:settings_create'},
         ]},
        {'title': 'Статьи', 'submenu': [
            {'title': 'Все посты', 'url_name': 'blog:post_list'},
            {'title': 'Добавить пост', 'url_name': 'blog:post_create'},
        ]},
        # {'title': 'Контакты', 'url_name': 'catalog:contacts'},
    ]
    for i in menu_list:
        if 'submenu' in i:
            for j in i['submenu']:
                if j['url_name'] == request.resolver_match.view_name:
                    j['active'] = True
                    i['active'] = True
                    break

    return {'menu': menu_list}
