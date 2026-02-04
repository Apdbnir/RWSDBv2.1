class TranslationManager:
    def __init__(self, language_code='en'):
        self.current_language = language_code
        self.selected_language = language_code

    def get_translation(self, key, language_code=None):
        """Get translated text based on key and language"""
        if language_code is None:
            language_code = self.current_language

        translations = {
            'language_changed_message': {
                'en': 'Language has been changed. Restart the application for changes to take effect.',
                'ru': 'Язык изменен. Перезапустите приложение для применения изменений.',
                'be': 'Мова зменена. Перазапусціце прыкладанне для ўжывання зменаў.'
            },
            'view_operation': {
                'en': 'View',
                'ru': 'Просмотр',
                'be': 'Прагляд'
            },
            'add_operation': {
                'en': 'Add',
                'ru': 'Добавить',
                'be': 'Дадаць'
            },
            'update_operation': {
                'en': 'Update',
                'ru': 'Обновить',
                'be': 'Абнавіць'
            },
            'delete_operation': {
                'en': 'Delete',
                'ru': 'Удалить',
                'be': 'Выдаліць'
            },
            'table': {
                'en': 'Table',
                'ru': 'Таблица',
                'be': 'Табліца'
            },
            'operation': {
                'en': 'Operation',
                'ru': 'Операция',
                'be': 'Аперацыя'
            },
            'filter': {
                'en': 'Filter',
                'ru': 'Фильтр',
                'be': 'Фільтр'
            },
            'execute_operation': {
                'en': 'Execute Operation',
                'ru': 'Выполнить операцию',
                'be': 'Выканаць аперацыю'
            },
            'special_queries_tab': {
                'en': 'Special Queries',
                'ru': 'Специальные запросы',
                'be': 'Спецыяльныя запыты'
            },
            'entity_operations_tab': {
                'en': 'Entity Operations',
                'ru': 'Операции с сущностями',
                'be': 'Аперацыі з сутнасцямі'
            },
            'query_editor_tab': {
                'en': 'Query Editor',
                'ru': 'Редактор запросов',
                'be': 'Рэдактар запытаў'
            },
            'query_history_tab': {
                'en': 'Query History',
                'ru': 'История запросов',
                'be': 'Гісторыя запытаў'
            },
            'table_view_tab': {
                'en': 'Table View',
                'ru': 'Просмотр таблиц',
                'be': 'Прагляд табліц'
            },
            'get_all_trains': {
                'en': 'Get all trains with their details',
                'ru': 'Получить все поезда с их деталями',
                'be': 'Атрымаць усе цягнікі з іх дэталей'
            },
            'get_all_employees': {
                'en': 'Get all employees with their positions',
                'ru': 'Получить всех сотрудников с их должностями',
                'be': 'Атрымаць усіх супрацоўнікаў з іх пасадамі'
            },
            'get_scheduled_arrivals': {
                'en': 'Get scheduled arrivals and departures',
                'ru': 'Получить запланированные прибытия и отправления',
                'be': 'Атрымаць запланаваныя прыбыцці і адпраўленні'
            },
            'get_passengers_with_tickets': {
                'en': 'Get passengers with tickets',
                'ru': 'Получить пассажиров с билетами',
                'be': 'Атрымаць пасажыраў з білетамі'
            },
            'get_employee_train_assignments': {
                'en': 'Get assignment of employees to trains',
                'ru': 'Получить назначение сотрудников на поезда',
                'be': 'Атрымаць прызначэнне супрацоўнікаў на цягнікі'
            },
            'execute_selected_query': {
                'en': 'Execute Selected Query',
                'ru': 'Выполнить выбранный запрос',
                'be': 'Выканаць выбраны запыт'
            },
            'save_results_excel': {
                'en': 'Export to...',
                'ru': 'Экспорт...',
                'be': 'Экспарт...'
            },
            'select_query': {
                'en': 'Select Query:',
                'ru': 'Выбрать запрос:',
                'be': 'Выбраць запыт:'
            },
            'parameters_required': {
                'en': 'Enter parameters separated by commas if required (e.g., param1, param2)',
                'ru': 'Введите параметры через запятую, если требуется (например, param1, param2)',
                'be': 'Увядзіце параметры праз коску, калі патрабуецца (напрыклад, парам1, парам2)'
            },
            'parameters': {
                'en': 'Parameters (if required):',
                'ru': 'Параметры (если требуются):',
                'be': 'Параметры (калі патрэбны):'
            },
            'entity_operations_instructions': {
                'en': 'Perform entity operations (Add, View, Update, Delete) on database tables:',
                'ru': 'Выполнить операции с сущностями (Добавить, Просмотр, Обновить, Удалить) над таблицами базы данных:',
                'be': 'Выканаць аперацыі з сутнасцямі (Дадаць, Прагляд, Абнавіць, Выдаліць) над табліцамі базы дадзеных:'
            },
            'select_table': {
                'en': 'Select Table:',
                'ru': 'Выбрать таблицу:',
                'be': 'Выбраць табліцу:'
            },
            'select_operation': {
                'en': 'Select Operation:',
                'ru': 'Выбрать операцию:',
                'be': 'Выбраць аперацыю:'
            },
            'id_parameter': {
                'en': 'ID/Parameter (for Update/Delete):',
                'ru': 'ID/Параметр (для обновления/удаления):',
                'be': 'ID/Параметр (для абнаўлення/выдалення):'
            },
            'filter_instructions': {
                'en': 'Enter filter condition (e.g., column_name=value)',
                'ru': 'Введите условие фильтра (например, column_name=value)',
                'be': 'Увядзіце ўмову фільтра (напрыклад, column_name=value)'
            },
            'Database Management System': {
                'en': 'Database Management System',
                'ru': 'Система управления базами данных',
                'be': 'Сістэма кіравання базамі дадзеных'
            },
            'Refresh Data': {
                'en': 'Refresh Data',
                'ru': 'Обновить данные',
                'be': 'Абнавіць дадзеныя'
            },
            'Add Row': {
                'en': 'Add Row',
                'ru': 'Добавить строку',
                'be': 'Дадаць радок'
            },
            'Delete Row': {
                'en': 'Delete Row',
                'ru': 'Удалить строку',
                'be': 'Выдаліць радок'
            },
            'Edit Row': {
                'en': 'Edit Row',
                'ru': 'Редактировать строку',
                'be': 'Рэдагаваць радок'
            },
            'Enter SQL query here...': {
                'en': 'Enter SQL query here...',
                'ru': 'Введите SQL-запрос здесь...',
                'be': 'Увядзіце SQL-запыт тут...'
            },
            'Execute Query': {
                'en': 'Execute Query',
                'ru': 'Выполнить запрос',
                'be': 'Выканаць запыт'
            },
            'Execute as Transaction': {
                'en': 'Execute as Transaction',
                'ru': 'Выполнить как транзакцию',
                'be': 'Выканаць як транзакцыю'
            },
            'Save Query': {
                'en': 'Save Query',
                'ru': 'Сохранить запрос',
                'be': 'Захаваць запыт'
            },
            'Export to...': {
                'en': 'Export to...',
                'ru': 'Экспорт...',
                'be': 'Экспарт...'
            },
            'Description': {
                'en': 'Description',
                'ru': 'Описание',
                'be': 'Апісанне'
            },
            'Query': {
                'en': 'Query',
                'ru': 'Запрос',
                'be': 'Запыт'
            },
            'Timestamp': {
                'en': 'Timestamp',
                'ru': 'Время',
                'be': 'Час'
            },
            'Load Query': {
                'en': 'Load Query',
                'ru': 'Загрузить запрос',
                'be': 'Загрузіць запыт'
            },
            'Delete Query': {
                'en': 'Delete Query',
                'ru': 'Удалить запрос',
                'be': 'Выдаліць запыт'
            },
            'Ready': {
                'en': 'Ready',
                'ru': 'Готов',
                'be': 'Гатова'
            },
            'File': {
                'en': 'File',
                'ru': 'Файл',
                'be': 'Файл'
            },
            'Connect to Database': {
                'en': 'Connect to Database',
                'ru': 'Подключиться к базе данных',
                'be': 'Падлучыцца да базы дадзеных'
            },
            'Create Backup': {
                'en': 'Create Backup',
                'ru': 'Создать резервную копию',
                'be': 'Стварыць рэзервовую копію'
            },
            'Restore from Backup': {
                'en': 'Restore from Backup',
                'ru': 'Восстановить из резервной копии',
                'be': 'Аднавіць з рэзервовай копіі'
            },
            'Transaction': {
                'en': 'Transaction',
                'ru': 'Транзакция',
                'be': 'Транзакцыя'
            },
            'Begin Transaction': {
                'en': 'Begin Transaction',
                'ru': 'Начать транзакцию',
                'be': 'Пачаць транзакцыю'
            },
            'Commit Transaction': {
                'en': 'Commit Transaction',
                'ru': 'Зафиксировать транзакцию',
                'be': 'Зафіксаваць транзакцыю'
            },
            'Rollback Transaction': {
                'en': 'Rollback Transaction',
                'ru': 'Откатить транзакцию',
                'be': 'Адкаціць транзакцыю'
            },
            'Add New Table': {
                'en': 'Add New Table',
                'ru': 'Добавить новую таблицу',
                'be': 'Дадаць новую табліцу'
            },
            'Delete Table': {
                'en': 'Delete Table',
                'ru': 'Удалить таблицу',
                'be': 'Выдаліць табліцу'
            },
            'Column': {
                'en': 'Column',
                'ru': 'Колонка',
                'be': 'Калонка'
            },
            'Add Column': {
                'en': 'Add Column',
                'ru': 'Добавить колонку',
                'be': 'Дадаць калонку'
            },
            'Delete Column': {
                'en': 'Delete Column',
                'ru': 'Удалить колонку',
                'be': 'Выдаліць калонку'
            },
            'Edit Column': {
                'en': 'Edit Column',
                'ru': 'Редактировать колонку',
                'be': 'Рэдагаваць калонку'
            },
            'Settings': {
                'en': 'Settings',
                'ru': 'Настройки',
                'be': 'Налады'
            },
            'Language': {
                'en': 'Language',
                'ru': 'Язык',
                'be': 'Мова'
            },
            'Русский': {
                'en': 'Русский',
                'ru': 'Русский',
                'be': 'Рускі'
            },
            'Беларускі': {
                'en': 'Беларускі',
                'ru': 'Беларуский',
                'be': 'Беларускі'
            },
            'English': {
                'en': 'English',
                'ru': 'Английский',
                'be': 'Англійская'
            },
            'ID or specific value for Update/Delete operations (if needed)': {
                'en': 'ID or specific value for Update/Delete operations (if needed)',
                'ru': 'ID или конкретное значение для операций Обновить/Удалить (если нужно)',
                'be': 'ID або канкрэтнае значэнне для аперацый Абнавіць/Выдаліць (калі патрэбна)'
            },
            'Select and execute predefined queries from lab work #5 and #6:': {
                'en': 'Select and execute predefined queries from lab work #5 and #6:',
                'ru': 'Выберите и выполните предопределенные запросы из лабораторной работы #5 и #6:',
                'be': 'Выберыце і выканайце прадвызначаныя запыты з лабараторнай працы #5 і #6:'
            },
            'get_all_scheduled_trains': {
                'en': 'Get all scheduled trains with platform information',
                'ru': 'Получить все запланированные поезда с информацией о платформе',
                'be': 'Атрымаць усе запланаваныя цягнікі з інфармацыяй пра платформу'
            },
            'get_passengers_tickets_trains': {
                'en': 'Get passengers with their tickets and train information',
                'ru': 'Получить пассажиров с их билетами и информацией о поезде',
                'be': 'Атрымаць пасажыраў з іх білетамі і інфармацыяй пра цягнік'
            },
            'get_employees_train_details': {
                'en': 'Get employees assigned to specific trains with their details',
                'ru': 'Получить сотрудников, назначенных на определенные поезда, с их деталями',
                'be': 'Атрымаць супрацоўнікаў, прызначаных на пэўныя цягнікі, з іх дэталей'
            },
            'get_services_employee_assignments': {
                'en': 'Get services with assignments to employees',
                'ru': 'Получить услуги с назначениями сотрудникам',
                'be': 'Атрымаць паслугі з прызначэннямі супрацоўнікам'
            },
            'get_detailed_schedule_passengers': {
                'en': 'Get detailed schedule with passenger information',
                'ru': 'Получить подробное расписание с информацией о пассажирах',
                'be': 'Атрымаць дэтальнае расклад з інфармацыяй пра пасажыраў'
            },
            'get_trains_specific_type': {
                'en': 'Get trains of specific type',
                'ru': 'Получить поезда определенного типа',
                'be': 'Атрымаць цягнікі пэўнага тыпу'
            },
            'get_employees_specific_position': {
                'en': 'Get employees with specific position',
                'ru': 'Получить сотрудников с определенной должностью',
                'be': 'Атрымаць супрацоўнікаў з пэўнай пасадай'
            },
            'get_employees_x_years_experience': {
                'en': 'Get employees with experience more than X years',
                'ru': 'Получить сотрудников с опытом более X лет',
                'be': 'Атрымаць супрацоўнікаў з вопытам больш за X гадоў'
            },
            'get_passengers_specific_passport': {
                'en': 'Get passengers with specific passport number',
                'ru': 'Получить пассажиров с определенным номером паспорта',
                'be': 'Атрымаць пасажыраў з пэўным нумарам пашпарту'
            },
            'get_tickets_specific_carriage': {
                'en': 'Get tickets for specific carriage number',
                'ru': 'Получить билеты для определенного номера вагона',
                'be': 'Атрымаць білеты для пэўнага нумара вагона'
            },
            'get_schedule_specific_date': {
                'en': 'Get schedule for specific date',
                'ru': 'Получить расписание на определенную дату',
                'be': 'Атрымаць расклад на пэўную дату'
            },
            'get_schedule_specific_train_id': {
                'en': 'Get schedule for specific train_id',
                'ru': 'Получить расписание для определенного идентификатора поезда',
                'be': 'Атрымаць расклад для пэўнага ідэнтыфікатара цягніка'
            },
            'get_all_passengers_by_train': {
                'en': 'Get all passengers by train',
                'ru': 'Получить всех пассажиров по поезду',
                'be': 'Атрымаць усіх пасажыраў па цягніку'
            },
            'get_employee_assignments_by_train_type': {
                'en': 'Get employee assignments by train type',
                'ru': 'Получить назначения сотрудников по типу поезда',
                'be': 'Атрымаць прызначэнні супрацоўнікаў па тыпу цягніка'
            },
            'get_platform_utilization': {
                'en': 'Get platform utilization',
                'ru': 'Получить использование платформ',
                'be': 'Атрымаць выкарыстанне платформ'
            },
            'get_tickets_by_price_range': {
                'en': 'Get tickets by price range',
                'ru': 'Получить билеты по диапазону цен',
                'be': 'Атрымаць білеты па дыяпазону коштаў'
            },
            'get_scheduled_trains_by_date': {
                'en': 'Get scheduled trains by date',
                'ru': 'Получить запланированные поезда по дате',
                'be': 'Атрымаць запланаваныя цягнікі па даты'
            },
            'parametrized_query_requires_params': {
                'en': "The selected query '{selected_query}' requires parameters. Please enter them in the parameters field.",
                'ru': "Выбранный запрос '{selected_query}' требует параметров. Введите их в поле параметров.",
                'be': "Выбраны запыт '{selected_query}' патрабуе параметраў. Увядзіце іх у поле параметраў."
            },
            'query_not_in_predefined_list': {
                'en': 'Selected query is not in the predefined queries list.',
                'ru': 'Выбранный запрос отсутствует в списке предопределенных запросов.',
                'be': 'Выбраны запыт адсутнічае ў спісе папярэдне вызначаных запытаў.'
            },
            'backup_creation_failed': {
                'en': 'Failed to create backup.',
                'ru': 'Не удалось создать резервную копию.',
                'be': 'Не ўдалося стварыць рэзервовую копію.'
            },
            'restore_failed': {
                'en': 'Failed to restore backup.',
                'be': 'Не ўдалося аднавіць рэзервовую копію.',
                'ru': 'Не удалось восстановить резервную копию.'
            },
            'enter_id_or_condition_for_delete': {
                'en': 'Please enter an ID or condition for the delete operation.',
                'ru': 'Пожалуйста, введите ID или условие для операции удаления.',
                'be': 'Калі ласка, увядзіце ID або ўмову для аперацыі выдалення.'
            },
            'enter_id_or_condition_for_update': {
                'en': 'Please enter an ID or condition for the update operation.',
                'ru': 'Пожалуйста, введите ID или условие для операции обновления.',
                'be': 'Калі ласка, увядзіце ID або ўмову для аперацыі абнаўлення.'
            },
            'transaction_started_successfully': {
                'en': 'Transaction started successfully',
                'ru': 'Транзакция успешно начата',
                'be': 'Транзакцыя паспяхова пачата'
            },
            'transaction_committed_successfully': {
                'en': 'Transaction committed successfully',
                'ru': 'Транзакция успешно зафиксирована',
                'be': 'Транзакцыя паспяхова зафіксавана'
            },
            'transaction_rolled_back_successfully': {
                'en': 'Transaction rolled back successfully',
                'ru': 'Транзакция успешно откачена',
                'be': 'Транзакцыя паспяхова адкачэна'
            },
            'special_query_executed_successfully_rows': {
                'en': 'Special query executed successfully. {count} rows returned.',
                'ru': 'Специальный запрос успешно выполнен. Возвращено {count} строк.',
                'be': 'Спецыяльны запыт паспяхова выкананы. Вярнуліся {count} радкоў.'
            },
            'special_query_executed_successfully': {
                'en': 'Special query executed successfully.',
                'ru': 'Специальный запрос успешно выполнен.',
                'be': 'Спецыяльны запыт паспяхова выкананы.'
            },
            'connected_to_database': {
                'en': 'Connected to {database}',
                'ru': 'Подключено к {database}',
                'be': 'Падключана да {database}'
            },
            'table_created_successfully': {
                'en': "Table '{table}' created successfully",
                'ru': "Таблица '{table}' успешно создана",
                'be': "Табліца '{table}' паспяхова створана"
            },
            'table_deleted_successfully': {
                'en': "Table '{table}' deleted successfully",
                'ru': "Таблица '{table}' успешно удалена",
                'be': "Табліца '{table}' паспяхова выдалена"
            },
            'column_added_to_table': {
                'en': "Column '{column}' added to table '{table}'",
                'ru': "Колонка '{column}' добавлена в таблицу '{table}'",
                'be': "Калонка '{column}' дададзеная ў табліцу '{table}'"
            },
            'column_deleted_from_table': {
                'en': "Column '{column}' deleted from table '{table}'",
                'ru': "Колонка '{column}' удалена из таблицы '{table}'",
                'be': "Калонка '{column}' выдаленая з табліцы '{table}'"
            },
            'row_added_to_table': {
                'en': "New row added to table '{table}'",
                'ru': "Новая строка добавлена в таблицу '{table}'",
                'be': "Новы радок дададзены ў табліцу '{table}'"
            },
            'row_deleted_from_table': {
                'en': "Row deleted from table '{table}'",
                'ru': "Строка удалена из таблицы '{table}'",
                'be': "Радок выдалены з табліцы '{table}'"
            },
            'query_executed_successfully_rows': {
                'en': 'Query executed successfully. {count} rows returned.',
                'ru': 'Запрос успешно выполнен. Возвращено {count} строк.',
                'be': 'Запыт паспяхова выкананы. Вярнуліся {count} радкоў.'
            },
            'query_executed_successfully': {
                'en': 'Query executed successfully.',
                'ru': 'Запрос успешно выполнен.',
                'be': 'Запыт паспяхова выкананы.'
            },
            'transaction_completed_operations': {
                'en': 'Transaction completed successfully with {count} operations.',
                'ru': 'Транзакция успешно завершена с {count} операциями.',
                'be': 'Транзакцыя паспяхова завершана з {count} аперацыямі.'
            },
            'query_saved_to_history': {
                'en': 'Query saved to history.',
                'ru': 'Запрос сохранен в историю.',
                'be': 'Запыт захаваны ў гісторыю.'
            },
            'backup_created_successfully': {
                'en': 'Backup created successfully: {path}',
                'ru': 'Резервная копия создана успешно: {path}',
                'be': 'Рэзервовая копія створана паспяхова: {path}'
            },
            'database_restored_successfully': {
                'en': 'Database restored successfully: {path}',
                'ru': 'База данных успешно восстановлена: {path}',
                'be': 'База дадзеных паспяхова адноўлена: {path}'
            },
            'table_exported_successfully': {
                'en': "Table '{table}' exported to {path}",
                'ru': "Таблица '{table}' экспортирована в {path}",
                'be': "Табліца '{table}' экспартавана ў {path}"
            },
            'query_results_exported_successfully': {
                'en': 'Query results exported to {path}',
                'ru': 'Результаты запроса экспортированы в {path}',
                'be': 'Вынікі запыту экспартаваны ў {path}'
            },
            'predefined_query_executed_successfully_rows': {
                'en': 'Predefined query executed successfully. {count} rows returned.',
                'ru': 'Предопределенный запрос успешно выполнен. Возвращено {count} строк.',
                'be': 'Папярэдне вызначаны запыт паспяхова выкананы. Вярнуліся {count} радкоў.'
            },
            'predefined_query_executed_successfully': {
                'en': 'Predefined query executed successfully.',
                'ru': 'Предопределенный запрос успешно выполнен.',
                'be': 'Папярэдне вызначаны запыт паспяхова выкананы.'
            },
            'view_operation_completed_successfully_rows': {
                'en': 'View operation completed successfully. {count} rows returned.',
                'ru': 'Операция просмотра успешно завершена. Возвращено {count} строк.',
                'be': 'Аперацыя прагляду паспяхова завершана. Вярнуліся {count} радкоў.'
            },
            'view_operation_completed_no_rows': {
                'en': 'View operation completed. No rows returned.',
                'ru': 'Операция просмотра завершена. Нет возвращенных строк.',
                'be': 'Аперацыя прагляду завершана. Няма вярнуліся радкоў.'
            },
            'delete_operation_completed_on_table': {
                'en': "Delete operation completed on table '{table}'.",
                'ru': "Операция удаления завершена в таблице '{table}'.",
                'be': "Аперацыя выдалення завершана ў табліцы '{table}'."
            },
            'update_operation_completed_on_table': {
                'en': "Update operation completed on table '{table}'.",
                'ru': "Операция обновления завершена в таблице '{table}'.",
                'be': "Аперацыя абнаўлення завершана ў табліцы '{table}'."
            },
            'select_table_for_select_queries': {
                'en': 'Select Table for SELECT Queries:',
                'ru': 'Выберите таблицу для SELECT запросов:',
                'be': 'Выберыце табліцу для SELECT запытаў:'
            },
            'select_query_type': {
                'en': 'Select Query Type:',
                'ru': 'Выберите тип запроса:',
                'be': 'Выберыце тып запыту:'
            },
            'select_queries_tab': {
                'en': 'SELECT Queries',
                'ru': 'SELECT Запросы',
                'be': 'SELECT Запыты'
            },
            'join_queries_tab': {
                'en': 'JOIN Queries',
                'ru': 'JOIN Запросы',
                'be': 'JOIN Запыты'
            },
            'aggregate_queries_tab': {
                'en': 'Aggregate & Set Queries',
                'ru': 'Агрегатные и Множественные запросы',
                'be': 'Агрэгатныя і Множныя запыты'
            },
            'Select and execute SELECT queries for individual tables:': {
                'en': 'Select and execute SELECT queries for individual tables:',
                'ru': 'Выберите и выполните SELECT запросы для отдельных таблиц:',
                'be': 'Выберыце і выканайце SELECT запыты для асобных табліц:'
            },
            'Select and execute JOIN queries between tables:': {
                'en': 'Select and execute JOIN queries between tables:',
                'ru': 'Выберите и выполните JOIN запросы между таблицами:',
                'be': 'Выберыце і выканайце JOIN запыты паміж табліцамі:'
            },
            'Select and execute aggregate, subquery, and set operation queries:': {
                'en': 'Select and execute aggregate, subquery, and set operation queries:',
                'ru': 'Выберите и выполните агрегатные, подзапросы и запросы операций с множествами:',
                'be': 'Выберыце і выканайце агрэгатныя, падзапыты і запыты аперацый з мноствамі:'
            },
            'User mode: Read-only access': {
                'en': 'User mode: Read-only access',
                'ru': 'Режим пользователя: только чтение',
                'be': 'Рэжым карыстальніка: толькі чытанне'
            },
            'Administrator mode: Full access': {
                'en': 'Administrator mode: Full access',
                'ru': 'Режим администратора: полный доступ',
                'be': 'Рэжым адміністратара: поўны доступ'
            },
            'Are you sure you want to exit the application? (User Mode)': {
                'en': 'Are you sure you want to exit the application? (User Mode)',
                'ru': 'Вы уверены, что хотите выйти из приложения? (Режим пользователя)',
                'be': 'Вы ўпэўненыя, што жадаеце выйсці з прыкладання? (Рэжым карыстальніка)'
            },
            'Are you sure you want to exit the application? (Administrator Mode)': {
                'en': 'Are you sure you want to exit the application? (Administrator Mode)',
                'ru': 'Вы уверены, что хотите выйти из приложения? (Режим администратора)',
                'be': 'Вы ўпэўненыя, што жадаеце выйсці з прыкладання? (Рэжым адміністратара)'
            },
            'Change Password': {
                'en': 'Change Password',
                'ru': 'Изменить пароль',
                'be': 'Змяніць пароль'
            },
            'Password changed successfully': {
                'en': 'Password changed successfully',
                'ru': 'Пароль успешно изменен',
                'be': 'Пароль паспяхова зменены'
            },
        }

        if key in translations and language_code in translations[key]:
            return translations[key][language_code]
        else:
            # Fallback to English if translation doesn't exist
            return translations[key]['en'] if key in translations else key

    def set_language(self, language_code):
        """Set the current language"""
        self.current_language = language_code
        self.selected_language = language_code