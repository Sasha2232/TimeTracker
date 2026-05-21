import datetime
from database import Database

db = Database()


class Bot:
    COMMANDS = {
        "/помощь": "Список всех команд",
        "/задачи": "Все задачи",
        "/сегодня": "Задачи за сегодня",
        "/итого": "Общее время",
        "/добавить [название]": "Добавить задачу",
        "/удалить [id]": "Удалить задачу",
        "/инфо [id]": "Подробности о задаче",
        "/очистить": "Удалить все задачи",
        "/история": "Последние 10 сообщений",
        "/дата": "Текущая дата и время",
        "/статистика": "Время по дням",
    }

    def handle(self, text):
        text = text.strip()
        if not text:
            return "Пустое сообщение. Введи /помощь для списка команд."

        msg = text.lower()

        if msg in ["/помощь", "/help", "помощь"]:
            return self._help()
        if msg in ["/задачи", "задачи"]:
            return self._list_tasks()
        if msg in ["/сегодня", "сегодня"]:
            return self._today()
        if msg in ["/итого", "итого"]:
            return self._total()
        if msg in ["/очистить", "очистить"]:
            return self._clear()
        if msg in ["/история", "история"]:
            return self._history()
        if msg in ["/дата", "дата"]:
            return self._date()
        if msg in ["/статистика", "статистика"]:
            return self._stats()
        if msg in ["привет", "hi", "/start", "/старт"]:
            return "Привет. Я Time Tracker бот. Введи /помощь."
        if msg.startswith("/добавить ") or msg.startswith("добавить "):
            return self._add(text)
        if msg.startswith("/удалить ") or msg.startswith("удалить "):
            return self._delete(text)
        if msg.startswith("/инфо ") or msg.startswith("инфо "):
            return self._info(text)

        return f'Неизвестная команда: "{text}". Введи /помощь.'

    def _help(self):
        lines = ["Доступные команды:\n"]
        for cmd, desc in self.COMMANDS.items():
            lines.append(f"  {cmd} — {desc}")
        return "\n".join(lines)

    def _list_tasks(self):
        tasks = db.get_all_tasks()
        if not tasks:
            return "Задач нет. Добавь через /добавить [название]"
        lines = ["Все задачи:\n"]
        for t in tasks:
            lines.append(f"  [{t['id']}] {t['name']} — {fmt(t['seconds'])} ({t['date']})")
        return "\n".join(lines)

    def _today(self):
        today = str(datetime.date.today())
        tasks = db.get_tasks_by_date(today)
        if not tasks:
            return "Сегодня задач нет."
        lines = [f"Задачи за {today}:\n"]
        for t in tasks:
            lines.append(f"  [{t['id']}] {t['name']} — {fmt(t['seconds'])}")
        return "\n".join(lines)

    def _total(self):
        tasks = db.get_all_tasks()
        if not tasks:
            return "Нет задач."
        total = sum(t["seconds"] for t in tasks)
        return f"Общее время по всем задачам: {fmt(total)}"

    def _add(self, text):
        name = text.split(" ", 1)[1].strip()
        if not name:
            return "Укажи название: /добавить [название]"
        db.add_task(name)
        return f'Задача "{name}" добавлена.'

    def _delete(self, text):
        parts = text.split(" ", 1)
        if len(parts) < 2 or not parts[1].strip().isdigit():
            return "Укажи ID: /удалить [id]"
        task_id = int(parts[1].strip())
        task = db.get_task_by_id(task_id)
        if not task:
            return f"Задача с ID {task_id} не найдена."
        db.delete_task(task_id)
        return f'Задача "{task["name"]}" удалена.'

    def _info(self, text):
        parts = text.split(" ", 1)
        if len(parts) < 2 or not parts[1].strip().isdigit():
            return "Укажи ID: /инфо [id]"
        task_id = int(parts[1].strip())
        task = db.get_task_by_id(task_id)
        if not task:
            return f"Задача с ID {task_id} не найдена."
        return (
            f"Задача #{task['id']}\n"
            f"  Название: {task['name']}\n"
            f"  Дата: {task['date']}\n"
            f"  Добавлена в: {task['time_added']}\n"
            f"  Время: {fmt(task['seconds'])}"
        )

    def _clear(self):
        db.delete_all_tasks()
        return "Все задачи удалены."

    def _history(self):
        messages = db.get_last_messages(10)
        if not messages:
            return "История пуста."
        lines = ["Последние сообщения:\n"]
        for m in messages:
            lines.append(f"  [{m['timestamp']}] {m['sender']}: {m['message']}")
        return "\n".join(lines)

    def _date(self):
        now = datetime.datetime.now()
        return f"Сейчас: {now.strftime('%d.%m.%Y %H:%M:%S')}"

    def _stats(self):
        tasks = db.get_all_tasks()
        if not tasks:
            return "Нет данных для статистики."
        stats = {}
        for t in tasks:
            stats[t["date"]] = stats.get(t["date"], 0) + t["seconds"]
        lines = ["Статистика по дням:\n"]
        for date, secs in sorted(stats.items(), reverse=True):
            lines.append(f"  {date}: {fmt(secs)}")
        return "\n".join(lines)


def fmt(seconds):
    if seconds < 60:
        return f"{seconds} сек"
    elif seconds < 3600:
        return f"{seconds // 60} мин {seconds % 60} сек"
    else:
        return f"{seconds // 3600} ч {(seconds % 3600) // 60} мин"
