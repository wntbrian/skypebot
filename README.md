# Инструкция по запуску бота:
## Меню
В паппке ironkabis_menu содержатся файлики с меню в формате json, их можно скоректировать по необходимости.

Имена файлов по порядковому номеру недели.

Если кол-во разнообразных недель уменьшается или увеличивается, надо изменить переменную ```NUMBER_OF_WEEKS``` в заголовке файла ```kabis.py```

Порядок последовательного выбора недель указан в переменной-списке ```week_number``` и содержит в себе имена файлов, которые читает бот.

## Деплой бота.
Что бы изменения попали на сервер, надо создать новый tag на ветку в который вы сделали изменения. 

Tag соберется автоматически, и опубликует бота.

Если бот не отвечает, вероятно вы ошиблись при исправлении файлов.


## Версия бота
Узнать текущую версию бота можно написав боту команду ```версия```