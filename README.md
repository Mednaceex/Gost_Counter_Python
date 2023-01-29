# Счётчик гостов
Данное приложение позволяет рассчитать результаты игры на основе предоставленных гостов и счетов реальных матчей. Программа разработана специально для целей турнира "UFO League".

## Установка
**Важно:** эта версия требует наличия на вашем устройстве интерпретатора Python 3 и библиотеки PyQt5 (рекомендуется версия Python 3.8 и выше и PyQt5 5.15.4 и выше, в противном случае мы не можем гарантировать работоспособность). Если у вас этого нет, вы можете скачать [версию с исполняемым файлом (.exe)](https://github.com/Mednaceex/Gost_Counter.git).

Приложение совместимо с операционными системами Windows и Linux.

Чтобы установить приложение, скачайте zip-архив (зелёная кнопка Code -> Download ZIP) и распакуйте его.

Для запуска программы откройте файл "Счётчик гостов.py".

## Использование

### Общие настройки
Во вкладке "Настройки" можно установить количество участвующих команд, количество матчей в госте и наличие дополнительной ставки. Чтобы сохранить введённые настройки, нажмите "OK". После этого количество окошек для ввода будет соответствовать введённым значениям. Максимально допустимые значения - 200 игроков и 15 матчей.

### Настройка команд и тренеров
Для настройки названий команд и имён тренеров откройте вкладку "Изменить команды". Проверьте правильность имеющихся данных и при необходимости измените их. Чтобы сохранить введённые данные, нажмите "OK". Кнопка "Cancel" отменит все изменения.
Учтите, что при следующем запуске вкладки команды будут отсортированы в алфавитном порядке. Названия и имена, введённые по умолчанию, соответствуют таковым в турнире "UFO League" на момент 5 января 2022 года.

### Настройка матчей
Для настройки матчей зайдите во вкладку "Настройка матчей" и настройте матчи согласно расписанию тура, выбирая команды из выпадающего списка. Также можно прокручивать команды колёсиком мыши. Отметьте при необходимости поле "Домашний фактор", чтобы учесть преимущество домашнего поля (засчитывание гола домашней команде, если оба игрока угадали счёт матча). Чтобы сохранить матчи, нажмите "OK". Кнопка "Cancel" отменит все изменения.

В случае, если какие-либо команды в расписании повторяются, об этом будет выведено сообщение при подсчёте результатов.

### Ввод счетов реальных матчей
Введите счета матчей госта по порядку в поля с номерами матчей в верхней части окна. Если хотя бы одно из двух окошек матча не заполнено, он не будет учитываться при подсчёте. Для быстрого переключения между окошками используйте Tab (перемещение на одно поле вправо) или Shift+Tab (на одно поле влево).

### Ввод текстов гостов
У каждой команды есть поле ввода текста, куда можно вставить скопированный текст госта. Текст ставки должен быть представлен в виде x-y (x и y — целые числа без разделительных знаков), где на месте "-" также могут быть символы "—", ":", "-:-", "—:—".

Если количество таких ставок в госте нужное количество (по умолчанию — 10), гост будет обработан, в противном случае при подсчёте будет засчитано 0 голов и выведено сообщение об ошибке. Чтобы посчитать неполный гост, выберите галочками под полем ввода номера матчей, которых нет в госте. Например, если в госте есть все матчи, кроме восьмого, нажмите галочку с номером 8.

В случае, если требуется исключить определённые ставки из госта (например, гост был сдан позднее дедлайна), это можно также сделать галочками, но только в том случае, если сданный гост полный (10 ставок по умолчанию).
Если же ставок меньше, необходимо удалить из текста все те, которые не должны быть посчитаны, и отменить галочками как их номера, так и изначально отсутствовавших матчей.

**Важно:** Из-за того что символы ":" и "-" используется как разделители в записи счетов, не допускайте их появления в тексте госта в непредвиденном месте. Например, удаляйте из текста время и дату дедлайна или время отправки сообщения, т.к. они могут содержать эти разделительные символы, окружённые цифрами, что будет воспринято как ставка.

### Дополнительная ставка
В случае выбора дополнительной ставки в настройках, у каждого окошка для ввода и в строке со счетами матчей появляются окошки с галочками. В зависимости от ставки игрока и реального исхода выберите "Да" или "Нет" в каждом окошке. Если ответ на ставку был не "Да" или "Нет", вы можете отметить "Да" в строке со счетами матчей, а все окошки с гостами самостоятельно выбрать ответ в зависимости от того, сыграла ли ставка игрока или нет.

### Сохранение, расчёт результатов и очистка полей.
Чтобы сохранить введённые данные, нажмите кнопку "Сохранить".

Для расчёта результатов нажмите кнопку "Рассчитать". В появившемся окне можно увидеть результаты и скопировать их. Помимо этого, будет выведена информация об имеющихся ошибках в гостах и расписании. Кнопка "Рассчитать" также сохраняет данные.

Кнопка "Очистить" сбрасывает введённые счета матчей, тексты гостов и нажатые галочки.

## Нашли ошибку?
Вы можете оставлять отчёты об ошибках на вкладке Issues. Мы будем вам очень признательны за вашу помощь.
