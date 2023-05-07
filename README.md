Итоговый проект Ростелеком
В рамках проекта был протестирован новый интерфейс регистрации/авторизации в личном кабинете от заказчика Ростелеком Информационные Технологии по предоставленным требованиям к сайту.
→ Требования заказчика  https://disk.yandex.ru/i/DUumu8VojbMTUg
→ Объект тестирования: https://b2c.passport.rt.ru

Во время выполнения проекта были протестированы требования, составлены тест-кейсы и оформлены дефекты.
→ Ссылка на документ https://docs.google.com/spreadsheets/d/1KX1ATuIko_4NeR6zK0Nu7ilOCoKLHS1TAEy8czKaxcY/edit?usp=sharing

Было проведено автоматизированное тестирование с использованием Selenium и PyTest:
1.В корневой папке находятся файлы settings.py с тестовыми данными, chromedriver.exe, requirements.txt 
2.Папка Тests содержит файлы для запуска автотестов:
•	tests_pages.py - тесты для страниц авторизации, регистрации и восстановление пароля, 
•	tests_input_field.py - тесты для полей ввода.
Запуск тестов осуществляется с помощью команд из консоли:
•	pytest -v --driver Chrome --driver-path Git\Rostelecom\chromedriver.exe   Tests\tests_pages.py,   
•	pytest -v --driver Chrome --driver-path Git\Rostelecom\chromedriver.exe Tests\tests_input_field.py  
•	или кнопкой Run Pycharm 
