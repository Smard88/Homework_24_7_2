# Homework_24_7_2
Тестовый проект к заданию 24_7_2 SkillFactory курса QAP

В директории /tests располагается файл с тестами

В директории /tests/images лежат картинки для теста добавления питомца и теста добавления картинки

В корневой директории лежит файл settings.py - содержит информацию о валидном и невалидном логине и пароле

В корневой директории лежит файл api.py, который является библиотекой к REST api сервису веб приложения Pet Friends

Библиотека api написана в классе, что соответствует принципам ООП и позволяет удобно пользоваться её методами. При инициализации библиотеки объявляется переменная base_url которая используется при формировании url для запроса.

Методы имеют подродное описание.

Код написан сгласно стандартам PEP8.

Тесты проверяют работу методов используя api библиотеку. Также имеются тесты проверки не добавление питомцев с некорректными данными.
