/**
 * Real-time Validation Utilities for RWSDBv2.1
 * Belarusian Railway Station Database System
 */

// Validation rules for each table field
export const validationRules = {
  // Passenger table
  passenger: {
    passport_number: {
      required: true,
      minLength: 9,
      maxLength: 12,
      pattern: /^[A-Z]{2}\d{7}$/i,
      messages: {
        required: 'Партал нумар неабходны',
        minLength: 'Мінімальная даўжыня - 9 знакаў',
        maxLength: 'Максімальная даўжыня - 12 знакаў',
        pattern: 'Фармат: 2 літары + 7 лічбаў (напрыклад, MP3456789)'
      }
    },
    full_name: {
      required: true,
      minLength: 5,
      maxLength: 200,
      pattern: /^[А-Яа-яA-Za-z\s'-]+$/,
      messages: {
        required: "Імя абавязковае",
        minLength: 'Мінімальная даўжыня - 5 знакаў',
        maxLength: 'Максімальная даўжыня - 200 знакаў',
        pattern: 'Толькі літары, прабелы, злучкі і апострафы'
      }
    },
    mobile_phone: {
      required: false,
      minLength: 12,
      maxLength: 15,
      pattern: /^\+375\d{9}$/,
      messages: {
        minLength: 'Фармат: +375XXXXXXXXX',
        maxLength: 'Фармат: +375XXXXXXXXX',
        pattern: 'Фармат: +375XXXXXXXXX (9 лічбаў пасля кода)'
      }
    },
    feature: {
      required: false,
      maxLength: 100,
      messages: {
        maxLength: 'Максімальная даўжыня - 100 знакаў'
      }
    }
  },

  // Train table
  train: {
    speed: {
      required: true,
      min: 60,
      max: 350,
      type: 'number',
      messages: {
        required: 'Хуткасць абавязковая',
        min: 'Мінімальная хуткасць - 60 км/г',
        max: 'Максімальная хуткасць - 350 км/г',
        type: 'Толькі лічбы'
      }
    },
    year_of_manufacture: {
      required: true,
      min: 1950,
      max: new Date().getFullYear() + 1,
      type: 'number',
      messages: {
        required: 'Год выпуску абавязковы',
        min: 'Год не раней за 1950',
        max: `Год не пазней за ${new Date().getFullYear() + 1}`,
        type: 'Толькі лічбы'
      }
    },
    type: {
      required: true,
      minLength: 3,
      maxLength: 50,
      pattern: /^[А-Яа-яA-Za-z\s-]+$/,
      messages: {
        required: 'Тып абавязковы',
        minLength: 'Мінімальная даўжыня - 3 знакі',
        maxLength: 'Максімальная даўжыня - 50 знакаў',
        pattern: 'Толькі літары і прабелы'
      }
    },
    number_of_cars: {
      required: true,
      min: 1,
      max: 24,
      type: 'number',
      messages: {
        required: 'Колькасць абавязковая',
        min: 'Мінімум 1 вагон',
        max: 'Максімум 24 вагоны',
        type: 'Толькі лічбы'
      }
    }
  },

  // Platform table
  platform: {
    capacity: {
      required: true,
      min: 50,
      max: 2000,
      type: 'number',
      messages: {
        required: 'Умяшчальнасць абавязковая',
        min: 'Мінімум 50 пасажыраў',
        max: 'Максімум 2000 пасажыраў',
        type: 'Толькі лічбы'
      }
    },
    location: {
      required: true,
      minLength: 5,
      maxLength: 200,
      pattern: /^[А-Яа-яA-Za-z0-9\s,-]+$/,
      messages: {
        required: 'Размяшчэнне абавязковае',
        minLength: 'Мінімальная даўжыня - 5 знакаў',
        maxLength: 'Максімальная даўжыня - 200 знакаў',
        pattern: 'Толькі літары, лічбы, коскі і злучкі'
      }
    },
    number_of_tracks: {
      required: true,
      min: 1,
      max: 10,
      type: 'number',
      messages: {
        required: 'Колькасць шляхоў абавязковая',
        min: 'Мінімум 1 шлях',
        max: 'Максімум 10 шляхоў',
        type: 'Толькі лічбы'
      }
    }
  },

  // Ticket table
  ticket: {
    carriage_number: {
      required: true,
      min: 1,
      max: 24,
      type: 'number',
      messages: {
        required: 'Нумар вагона абавязковы',
        min: 'Мінімум 1',
        max: 'Максімум 24',
        type: 'Толькі лічбы'
      }
    },
    ticket_price: {
      required: true,
      min: 1,
      max: 10000,
      type: 'decimal',
      messages: {
        required: 'Цана абавязковая',
        min: 'Мінімум 1.00 BYN',
        max: 'Максімум 10000.00 BYN',
        type: 'Толькі лічбы (напрыклад, 45.50)'
      }
    },
    seat_number: {
      required: true,
      min: 1,
      max: 100,
      type: 'number',
      messages: {
        required: 'Нумар месца абавязковы',
        min: 'Мінімум 1',
        max: 'Максімум 100',
        type: 'Толькі лічбы'
      }
    },
    passenger_number: {
      required: true,
      min: 1,
      type: 'number',
      messages: {
        required: 'Нумар пасажыра абавязковы',
        min: 'Няправільны нумар',
        type: 'Толькі лічбы'
      }
    }
  },

  // Schedule table
  schedule: {
    arrival_time: {
      required: true,
      pattern: /^([01]\d|2[0-3]):([0-5]\d)$/,
      messages: {
        required: 'Час прыбыцця абавязковы',
        pattern: 'Фармат: ГГ:ХВ (напрыклад, 14:30)'
      }
    },
    departure_time: {
      required: true,
      pattern: /^([01]\d|2[0-3]):([0-5]\d)$/,
      messages: {
        required: 'Час адпраўлення абавязковы',
        pattern: 'Фармат: ГГ:ХВ (напрыклад, 14:45)'
      }
    },
    carriage_numbering: {
      required: false,
      maxLength: 50,
      messages: {
        maxLength: 'Максімальная даўжыня - 50 знакаў'
      }
    },
    date: {
      required: true,
      pattern: /^\d{4}-\d{2}-\d{2}$/,
      messages: {
        required: 'Дата абавязковая',
        pattern: 'Фармат: ГГГГ-ММ-ДД (напрыклад, 2026-03-25)'
      }
    },
    train_number: {
      required: true,
      min: 1,
      type: 'number',
      messages: {
        required: 'Нумар цягніка абавязковы',
        min: 'Няправільны нумар',
        type: 'Толькі лічбы'
      }
    },
    platform_number: {
      required: true,
      min: 1,
      type: 'number',
      messages: {
        required: 'Нумар платформы абавязковы',
        min: 'Няправільны нумар',
        type: 'Толькі лічбы'
      }
    },
    ticket_number: {
      required: false,
      min: 1,
      type: 'number',
      messages: {
        min: 'Няправільны нумар',
        type: 'Толькі лічбы'
      }
    }
  },

  // Employee table
  employee: {
    full_name: {
      required: true,
      minLength: 5,
      maxLength: 200,
      pattern: /^[А-Яа-яA-Za-z\s'-]+$/,
      messages: {
        required: "Імя абавязковае",
        minLength: 'Мінімальная даўжыня - 5 знакаў',
        maxLength: 'Максімальная даўжыня - 200 знакаў',
        pattern: 'Толькі літары, прабелы, злучкі і апострафы'
      }
    },
    position: {
      required: true,
      minLength: 3,
      maxLength: 100,
      pattern: /^[А-Яа-яA-Za-z\s-]+$/,
      messages: {
        required: 'Пасада абавязковая',
        minLength: 'Мінімальная даўжыня - 3 знакі',
        maxLength: 'Максімальная даўжыня - 100 знакаў',
        pattern: 'Толькі літары і прабелы'
      }
    },
    work_experience: {
      required: false,
      min: 0,
      max: 60,
      type: 'number',
      messages: {
        min: 'Мінімум 0 гадоў',
        max: 'Максімум 60 гадоў',
        type: 'Толькі лічбы'
      }
    },
    passport_information: {
      required: true,
      minLength: 6,
      maxLength: 50,
      messages: {
        required: 'Пашпартныя даныя абавязковыя',
        minLength: 'Мінімальная даўжыня - 6 знакаў',
        maxLength: 'Максімальная даўжыня - 50 знакаў'
      }
    }
  },

  // Service table
  service: {
    service_name: {
      required: true,
      minLength: 3,
      maxLength: 100,
      pattern: /^[А-Яа-яA-Za-z\s-]+$/,
      messages: {
        required: 'Назва паслугі абавязковая',
        minLength: 'Мінімальная даўжыня - 3 знакі',
        maxLength: 'Максімальная даўжыня - 100 знакаў',
        pattern: 'Толькі літары і прабелы'
      }
    },
    price: {
      required: true,
      min: 0.01,
      max: 10000,
      type: 'decimal',
      messages: {
        required: 'Цана абавязковая',
        min: 'Мінімум 0.01 BYN',
        max: 'Максімум 10000.00 BYN',
        type: 'Толькі лічбы (напрыклад, 25.00)'
      }
    },
    type: {
      required: true,
      minLength: 3,
      maxLength: 50,
      pattern: /^[А-Яа-яA-Za-z\s-]+$/,
      messages: {
        required: 'Тып абавязковы',
        minLength: 'Мінімальная даўжыня - 3 знакі',
        maxLength: 'Максімальная даўжыня - 50 знакаў',
        pattern: 'Толькі літары і прабелы'
      }
    },
    date: {
      required: true,
      pattern: /^\d{4}-\d{2}-\d{2}$/,
      messages: {
        required: 'Дата абавязковая',
        pattern: 'Фармат: ГГГГ-ММ-ДД (напрыклад, 2026-03-25)'
      }
    }
  }
};

/**
 * Validate a single field value in real-time
 * @param {string} tableName - Name of the table
 * @param {string} fieldName - Name of the field
 * @param {any} value - Value to validate
 * @returns {object} - { isValid: boolean, error: string|null }
 */
export const validateField = (tableName, fieldName, value) => {
  const tableRules = validationRules[tableName];
  if (!tableRules) {
    return { isValid: true, error: null };
  }

  const rules = tableRules[fieldName];
  if (!rules) {
    return { isValid: true, error: null };
  }

  // Handle empty/undefined values
  if (value === undefined || value === null || value === '') {
    if (rules.required) {
      return { isValid: false, error: rules.messages.required };
    }
    return { isValid: true, error: null };
  }

  // Convert value to string for pattern matching
  const stringValue = String(value).trim();

  // Type validation
  if (rules.type === 'number' || rules.type === 'decimal') {
    const numValue = parseFloat(stringValue);
    if (isNaN(numValue)) {
      return { isValid: false, error: rules.messages.type };
    }
    
    if (rules.min !== undefined && numValue < rules.min) {
      return { isValid: false, error: rules.messages.min };
    }
    
    if (rules.max !== undefined && numValue > rules.max) {
      return { isValid: false, error: rules.messages.max };
    }
    
    return { isValid: true, error: null };
  }

  // String validation
  if (rules.minLength && stringValue.length < rules.minLength) {
    return { isValid: false, error: rules.messages.minLength };
  }

  if (rules.maxLength && stringValue.length > rules.maxLength) {
    return { isValid: false, error: rules.messages.maxLength };
  }

  if (rules.pattern && !rules.pattern.test(stringValue)) {
    return { isValid: false, error: rules.messages.pattern };
  }

  return { isValid: true, error: null };
};

/**
 * Validate all fields in a form data object
 * @param {string} tableName - Name of the table
 * @param {object} formData - Form data object
 * @returns {object} - { isValid: boolean, errors: object }
 */
export const validateForm = (tableName, formData) => {
  const tableRules = validationRules[tableName];
  const errors = {};
  let isValid = true;

  if (!tableRules) {
    return { isValid: true, errors: {} };
  }

  for (const [fieldName, rules] of Object.entries(tableRules)) {
    const value = formData[fieldName];
    const validation = validateField(tableName, fieldName, value);
    
    if (!validation.isValid) {
      isValid = false;
      errors[fieldName] = validation.error;
    }
  }

  // Special validation: departure_time must be after arrival_time for schedule
  if (tableName === 'schedule' && formData.arrival_time && formData.departure_time) {
    const arrival = new Date(`2000-01-01T${formData.arrival_time}`);
    const departure = new Date(`2000-01-01T${formData.departure_time}`);
    
    if (departure <= arrival) {
      isValid = false;
      errors.departure_time = 'Час адпраўлення павінен быць пасля часу прыбыцця';
    }
  }

  return { isValid, errors };
};

/**
 * Get field placeholder based on validation rules
 * @param {string} tableName - Name of the table
 * @param {string} fieldName - Name of the field
 * @returns {string} - Placeholder text
 */
export const getFieldPlaceholder = (tableName, fieldName) => {
  const placeholders = {
    passenger: {
      passport_number: 'MP3456789',
      full_name: 'Іваноў Іван Іванавіч',
      mobile_phone: '+375291234567',
      feature: 'Пастаянны кліент'
    },
    train: {
      speed: '140',
      year_of_manufacture: '2020',
      type: 'Пасажырскі хуткі',
      number_of_cars: '12'
    },
    platform: {
      capacity: '500',
      location: 'Мінск-Пасажырскі, перон 1',
      number_of_tracks: '2'
    },
    ticket: {
      carriage_number: '1',
      ticket_price: '45.50',
      seat_number: '15',
      passenger_number: '1'
    },
    schedule: {
      arrival_time: '14:30',
      departure_time: '14:45',
      carriage_numbering: 'Ад галавы цягніка',
      date: '2026-03-25',
      train_number: '1',
      platform_number: '1',
      ticket_number: '1'
    },
    employee: {
      full_name: 'Каваленка Аляксей Мікалаевіч',
      position: 'Машыніст цягніка',
      work_experience: '15',
      passport_information: 'MP2345678'
    },
    service: {
      service_name: 'Харчовае абслугоўванне',
      price: '25.00',
      type: 'Пасажырская',
      date: '2026-03-25'
    }
  };

  return placeholders[tableName]?.[fieldName] || '';
};

/**
 * Get field label in Belarusian
 * @param {string} fieldName - Field name
 * @returns {string} - Label in Belarusian
 */
export const getFieldLabel = (fieldName) => {
  const labels = {
    passenger_number: 'Нумар пасажыра',
    passport_number: 'Нумар пашпарта',
    full_name: 'Поўнае імя',
    mobile_phone: 'Мабільны тэлефон',
    feature: 'Асаблівасць',
    train_number: 'Нумар цягніка',
    speed: 'Хуткасць (км/г)',
    year_of_manufacture: 'Год выпуску',
    type: 'Тып',
    number_of_cars: 'Колькасць вагонаў',
    platform_number: 'Нумар платформы',
    capacity: 'Умяшчальнасць',
    location: 'Размяшчэнне',
    number_of_tracks: 'Колькасць шляхоў',
    ticket_number: 'Нумар квітка',
    carriage_number: 'Нумар вагона',
    ticket_price: 'Цана квітка (BYN)',
    seat_number: 'Нумар месца',
    schedule_number: 'Нумар раскладу',
    arrival_time: 'Час прыбыцця',
    departure_time: 'Час адпраўлення',
    carriage_numbering: 'Нумарацыя вагонаў',
    date: 'Дата',
    employee_number: 'Нумар супрацоўніка',
    position: 'Пасада',
    work_experience: 'Стаж працы (гадоў)',
    passport_information: 'Пашпартныя даныя',
    service_number: 'Нумар паслугі',
    service_name: 'Назва паслугі',
    price: 'Цана (BYN)',
    employee_id: 'Супрацоўнік',
    service_id: 'Паслуга'
  };

  return labels[fieldName] || fieldName;
};
