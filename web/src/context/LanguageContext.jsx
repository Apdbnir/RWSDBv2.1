import { createContext, useContext, useState, useEffect } from 'react';

const translations = {
  be: {
    // Navigation
    dashboard: 'Панэль кіравання',
    tables: 'Табліцы',
    databases: 'Базы даных',
    queries: 'Запыты',
    backup: 'Рэзэрваванне',
    export: 'Экспарт',
    lab3: 'Канвертар',
    specialQueries: 'Спецыяльныя запыты',
    logout: 'Выйсці',
    login: 'Уваход',
    
    // Common
    add: 'Дадаць',
    update: 'Абнавіць',
    delete: 'Выдаліць',
    view: 'Прагледзець',
    save: 'Захаваць',
    cancel: 'Адмена',
    ok: 'ОК',
    search: 'Пошук',
    filter: 'Фільтр',
    clear: 'Ачысціць',
    apply: 'Ужыць',
    close: 'Закрыць',
    refresh: 'Абнавіць',
    loading: 'Загрузка...',
    noData: 'Няма даных',
    error: 'Памылка',
    success: 'Поспех',
    confirm: 'Пацвердзіць',
    yes: 'Так',
    no: 'Не',
    
    // Table operations
    addRecord: 'Дадаць запіс',
    updateRecord: 'Абнавіць запіс',
    deleteRecord: 'Выдаліць запіс',
    viewRecords: 'Прагледзець запісы',
    createBackup: 'Стварыць рэзэрваванне',
    customQuery: 'Уласны запыт',
    saveQuery: 'Захаваць запыт',
    
    // Auth
    username: 'Імя карыстальніка',
    password: 'Пароль',
    adminPassword: 'Пароль адміністратара',
    loginAsAdmin: 'Уваход як адмін',
    loginAsUser: 'Уваход як карыстальнік',
    sessionExpired: 'Сесія скончылася',
    wrongPassword: 'Няправільны пароль',
    
    // Tables
    passenger: 'Пасажыры',
    train: 'Цягнікі',
    platform: 'Платформы',
    ticket: 'Квіткі',
    schedule: 'Расклад',
    employee: 'Супрацоўнікі',
    service: 'Паслугі',
    appointment: 'Прызначэнні',
    work: 'Праца',
    
    // Messages
    recordAdded: 'Запіс дададзены',
    recordUpdated: 'Запіс абноўлены',
    recordDeleted: 'Запіс выдалены',
    backupCreated: 'Рэзэрваванне створана',
    querySaved: 'Запыт захаваны',
    conversionComplete: 'Канвертацыя завершана',
    
    // Settings
    settings: 'Налады',
    theme: 'Тэма',
    lightTheme: 'Светлая',
    darkTheme: 'Цёмная',
    language: 'Мова',
    belarusian: 'Беларуская',
    russian: 'Руская',
    english: 'Англійская',
  },
  ru: {
    // Navigation
    dashboard: 'Панель управления',
    tables: 'Таблицы',
    databases: 'Базы данных',
    queries: 'Запросы',
    backup: 'Резервирование',
    export: 'Экспорт',
    lab3: 'Конвертор',
    specialQueries: 'Специальные запросы',
    logout: 'Выйти',
    login: 'Вход',
    
    // Common
    add: 'Добавить',
    update: 'Обновить',
    delete: 'Удалить',
    view: 'Просмотр',
    save: 'Сохранить',
    cancel: 'Отмена',
    ok: 'ОК',
    search: 'Поиск',
    filter: 'Фильтр',
    clear: 'Очистить',
    apply: 'Применить',
    close: 'Закрыть',
    refresh: 'Обновить',
    loading: 'Загрузка...',
    noData: 'Нет данных',
    error: 'Ошибка',
    success: 'Успех',
    confirm: 'Подтвердить',
    yes: 'Да',
    no: 'Нет',
    
    // Table operations
    addRecord: 'Добавить запись',
    updateRecord: 'Обновить запись',
    deleteRecord: 'Удалить запись',
    viewRecords: 'Просмотреть записи',
    createBackup: 'Создать резерв.копию',
    customQuery: 'Свой запрос',
    saveQuery: 'Сохранить запрос',
    
    // Auth
    username: 'Имя пользователя',
    password: 'Пароль',
    adminPassword: 'Пароль администратора',
    loginAsAdmin: 'Вход как админ',
    loginAsUser: 'Вход как пользователь',
    sessionExpired: 'Сессия истекла',
    wrongPassword: 'Неверный пароль',
    
    // Tables
    passenger: 'Пассажиры',
    train: 'Поезда',
    platform: 'Платформы',
    ticket: 'Билеты',
    schedule: 'Расписание',
    employee: 'Сотрудники',
    service: 'Услуги',
    appointment: 'Назначения',
    work: 'Работа',
    
    // Messages
    recordAdded: 'Запись добавлена',
    recordUpdated: 'Запись обновлена',
    recordDeleted: 'Запись удалена',
    backupCreated: 'Резервная копия создана',
    querySaved: 'Запрос сохранён',
    conversionComplete: 'Конвертация завершена',
    
    // Settings
    settings: 'Настройки',
    theme: 'Тема',
    lightTheme: 'Светлая',
    darkTheme: 'Тёмная',
    language: 'Язык',
    belarusian: 'Белорусский',
    russian: 'Русский',
    english: 'Английский',
  },
  en: {
    // Navigation
    dashboard: 'Dashboard',
    tables: 'Tables',
    databases: 'Databases',
    queries: 'Queries',
    backup: 'Backup',
    export: 'Export',
    lab3: 'Converter',
    specialQueries: 'Special Queries',
    logout: 'Logout',
    login: 'Login',
    
    // Common
    add: 'Add',
    update: 'Update',
    delete: 'Delete',
    view: 'View',
    save: 'Save',
    cancel: 'Cancel',
    ok: 'OK',
    search: 'Search',
    filter: 'Filter',
    clear: 'Clear',
    apply: 'Apply',
    close: 'Close',
    refresh: 'Refresh',
    loading: 'Loading...',
    noData: 'No data',
    error: 'Error',
    success: 'Success',
    confirm: 'Confirm',
    yes: 'Yes',
    no: 'No',
    
    // Table operations
    addRecord: 'Add Record',
    updateRecord: 'Update Record',
    deleteRecord: 'Delete Record',
    viewRecords: 'View Records',
    createBackup: 'Create Backup',
    customQuery: 'Custom Query',
    saveQuery: 'Save Query',
    
    // Auth
    username: 'Username',
    password: 'Password',
    adminPassword: 'Admin Password',
    loginAsAdmin: 'Login as Admin',
    loginAsUser: 'Login as User',
    sessionExpired: 'Session Expired',
    wrongPassword: 'Wrong Password',
    
    // Tables
    passenger: 'Passengers',
    train: 'Trains',
    platform: 'Platforms',
    ticket: 'Tickets',
    schedule: 'Schedule',
    employee: 'Employees',
    service: 'Services',
    appointment: 'Appointments',
    work: 'Work',
    
    // Messages
    recordAdded: 'Record Added',
    recordUpdated: 'Record Updated',
    recordDeleted: 'Record Deleted',
    backupCreated: 'Backup Created',
    querySaved: 'Query Saved',
    conversionComplete: 'Conversion Complete',
    
    // Settings
    settings: 'Settings',
    theme: 'Theme',
    lightTheme: 'Light',
    darkTheme: 'Dark',
    language: 'Language',
    belarusian: 'Belarusian',
    russian: 'Russian',
    english: 'English',
  }
};

const LanguageContext = createContext();

export const useLanguage = () => useContext(LanguageContext);

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    const saved = localStorage.getItem('language');
    return saved || 'be';
  });

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  const t = (key) => {
    return translations[language]?.[key] || translations['be'][key] || key;
  };

  const setLanguageCode = (code) => {
    if (translations[code]) {
      setLanguage(code);
    }
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage: setLanguageCode, t, languages: Object.keys(translations) }}>
      {children}
    </LanguageContext.Provider>
  );
};