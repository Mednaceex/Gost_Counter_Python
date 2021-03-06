# Счётчик гостов
Данное приложение позволяет рассчитать результаты игры на основе предоставленных гостов и счетов реальных матчей. Программа разработана специально для целей турнира "UFO League".

## Установка
**Важно:** эта версия требует наличия на вашем устройстве интерпретатора Python 3 и библиотеки PyQt5 (рекомендуется версия Python 3.8 и выше и PyQt5 5.15.4 и выше, в противном случае мы не можем гарантировать работоспособность). Если у вас этого нет, вы можете скачать [версию с исполняемым файлом (.exe)](https://github.com/Mednaceex/Gost_Counter.git).

Приложение совместимо с операционными системами Windows и Linux.

Чтобы установить приложение, скачайте zip-архив (зелёная кнопка Code -> Download ZIP) и распакуйте его. (Можно также склонировать этот репозиторий, если умеете это делать, но вдаваться в подробности здесь не будем.)

Для запуска программы откройте файл "Счётчик гостов.py". Также в папке приложения есть ярлык, который вы можете перенести, например, на рабочий стол.

## Использование

### Настройка команд и тренеров
Для настройки названий команд и имён тренеров откройте вкладку "Изменить команды". Проверьте правильность имеющихся данных и при необходимости измените их. Чтобы сохранить введённые данные, нажмите "OK". Кнопка "Cancel" отменит все изменения.
Учтите, что при следующем запуске вкладки команды будут отсортированы в алфавитном порядке. Названия и имена, введённые по умолчанию, соответствуют таковым в турнире "UFO League" на момент 22 декабря 2021 года.

### Настройка матчей
Для настройки матчей зайдите во вкладку "Настройка матчей" и настройте матчи согласно расписанию тура, выбирая команды из выпадающего списка. Также можно прокручивать команды колёсиком мышки. Чтобы сохранить матчи, нажмите "OK". Кнопка "Cancel" отменит все изменения.

В случае, если какие-либо команды в расписании повторяются, об этом будет выведено сообщение при подсчёте результатов.

### Ввод счетов реальных матчей
Введите счета матчей госта по порядку в поля с номерами матчей в верхней части окна. Если хотя бы одно из двух окошек матча не заполнено, он не будет учитываться при подсчёте. Для быстрого переключения между окошками используйте Tab (перемещение на одно поле вправо) или Shift+Tab (на одно поле влево).

### Ввод текстов гостов
У каждой команды есть поле ввода текста, куда можно вставить скопированный текст госта. Текст ставки должен быть представлен в виде x-y (x и y — целые числа без разделительных знаков), где на месте "-" также могут быть символы "—", ":", "-:-", "—:—".

Если количество таких ставок в госте — 10, гост будет обработан, в противном случае программа выдаст ошибку при подсчёте и засчитает 0 голов. Чтобы посчитать неполный гост, выберите галочками под полем ввода номера матчей, которых нет в госте. Например, если в госте есть все матчи, кроме восьмого, нажмите галочку с номером 8.

В случае, если требуется исключить определённые ставки из госта (например, гост был сдан позднее дедлайна), это можно также сделать галочками, но только в том случае, если сданный гост полный (10 ставок).
Если же ставок меньше, необходимо удалить из текста все те, которые не должны быть посчитаны, и отменить галочками как их номера, так и изначально отсутствовавших матчей.

**Важно:** Из-за того что символы ":" и "-" используется как разделители в записи счетов, не допускайте их появления в тексте госта в непредвиденном месте. Например, удаляйте из текста время и дату дедлайна или время отправки сообщения, т.к. они могут содержать эти разделительные символы, окружённые цифрами, что будет воспринято как ставка.

### Сохранение, расчёт результатов и очистка полей.
Чтобы сохранить введённые данные, нажмите кнопку "Сохранить".

Для расчёта результатов нажмите кнопку "Рассчитать". В появившемся окне можно увидеть результаты и скопировать их. Помимо этого, будет выведена информация об имеющихся ошибках в гостах и расписании. Кнопка "Рассчитать" также сохраняет данные.

Кнопка "Очистить" сбрасывает введённые счета матчей, тексты гостов и нажатые галочки.

## Нашли ошибку?
Вы можете оставлять отчёты об ошибках на вкладке Issues. Мы будем вам очень признательны за вашу помощь.

## Дополнительно
Приложение использует Python 3.9 и библиотеку PyQt5, имеющие открытый исходный код.