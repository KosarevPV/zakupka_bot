Создать директорию: mkdir zakupka
Перейти в директорию: cd zakupka
Установка sudo: apt install sudo
Обновление пакетов: sudo apt update && sudo apt upgrade
Установка виртуального окружения: sudo apt install python3-venv
Создание виртуального окружения: python3 -m venv venvZak
Запуск виртуального окружения: source venvZak/bin/activate

Переносим файлы с компьютера на сервер через FileZilla 

Нобходимые библиотеки для работы с ботом: pip install -r requirements.txt

Установка screen: sudo apt install screen
Создаст новый screen: screen
Свернуть screen: CRTL + A, после чего нажмаем D
Что-бы посмотреть список запущенных screen: screen -ls
Что-бы вернуться к свёрнутому screen: screen -r
Что-бы завершить сессию/закрыть screen: exit