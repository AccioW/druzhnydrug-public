# DruzhnyDrugBot

## О Боте
DruzhnyDrugBot - это бот для Telegram, созданный в первую очередь для развлечения Дружбы*, но его может использовать любой пользователь Telegram просто введя в поиске `@DruzhnyDrugBot`. 
Он включает в себя генератор случайного уровня дружбы и простую математическую игру, вдохновленную Евгосиком.

![image](https://github.com/AccioW/druzhnydrugbot/assets/149820811/224e1855-d971-48c7-be76-07304be655ee)

## Функции
- **Проверка уровня дружбы:** Позволяет пользователю узнать свой уровень дружбы на текущий день.
- **Обратный отсчет до Дня рождения:** Сообщает пользователю количество дней, оставшихся до его дня рождения.
- **Математическая игра:** Позволяет пользователю поучаствовать в простой математической игре для проверки своих арифметических навыков.

## Планы
- [ ] **Рандомизатор игры:** Реализовать рандомизатор игр с последующим опросом пользователей (только для Дружбы).
- [ ] **Улучшения диалога:** Улучшить разговорные возможности, возможно, интегрируя языковую модель.
- [x] **Еженедельная доставка жаб:** Автоматическая отправка жабки каждую среду (пока только для Дружбы)
- [ ] **Улучшение команды `/birthday`:** Добавить автоматические поздравления с днем рождения пользователей в их день рождения.
- [X] **Улучшение команды `/friend`:** Добавить лимит на одно отправление команды `/friend` в день.

## Использование
Для взаимодействия с DruzhnyDrugBot можно использовать различные команды, такие как:
- `/start` - отображение основного меню бота
- `/help` - отображение меню помощи
- `/friend` - получение случайного уровня дружбы на сегодня
- `/birthday` - получение информации о том, сколько осталось дней до дня рождения 
- `/math` - запуск арифметической игры 

Помимо команд бот может отвечать на сообщения пользователя. В групповых чатах это достигается упоминанием бота через `@` (если бот добавлен в чат и имеет соответствующие разрешения) или же ответом на любое сообщение от бота

> Дружба (имя собственное) - название группового чата в Telegram
