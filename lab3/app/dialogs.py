from dataclasses import dataclass
from emoji import emojize


@dataclass(frozen=True)
class Messages:
    test: str = "Привет {name}. Работаю..."

    btn_online: str = f"{emojize(':bookmark_tabs:')} В процессе"
    btn_config: str = f"{emojize(':memo:')} Настройки"

    start_new_user: str = "Привет. Я помогу тебе с отслеживание твоих дедлайнов. "
    start_current_user: str = "Привет. С возвращением! " \
                              "Используй команды или меню внизу для продолжения."
    help: str = """
        Я помогу тебе с отслеживанием твоих дедлайнов.
Я могу помогу тебе рассчитать хорошую тактику для успешной сдачи любого задания в срок.
Так же я могу быть таймером для интенсивного занятия (45 минут работы/15 минут отдыха).
Если тебе стало грустно, то я попробую подбодрить тебя мотивационной цитатой.
        
- Что бы выбрать/изменить дедлайны нажмите 'Настройки'.
- Для проверки результатов нажмите 'В процессе'.
        """
    deadline_row: str = "{i}. {flag} {name}"
    config: str = "Сейчас выбраны:\n{deadlines}"
    btn_back: str = "<- Назад"
    btn_go: str = "Вперед ->"
    btn_save: str = "Сохранить"
    config_btn_edit: str = "Изменить"
    config_btn_delete: str = "Удалить данные"
    data_delete: str = "Данные успешно удалены"
    set_deadlines: str = "Выбери 3 дедлайна для отслеживания.\nВыбраны:\n{deadlines}"
    main: str = "Что будем делать?"
    db_saved: str = "Настройки сохранены"
    cb_not_saved: str = "Дедлайны не выбраны"
    cb_limit: str = "Превышен лимит. Максимум 3 дедлайна."
    results: str = "Все результаты за 48 часов\n{tasks}"
    no_results: str = "Нет задач за последние 48 часов"
    update_results: str = "Обновить результаты"
    cb_updated: str = f"{emojize(':white_heavy_check_mark:')} Готово"
    unknown_text: str = "Ничего не понятно, но очень интересно.\nПопробуй команду /help"


msg = Messages()
