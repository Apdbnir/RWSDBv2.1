/**
 * Best-in-Class Error Handling for RWSDBv2.1
 * Comprehensive error handling with user-friendly messages
 */

// Error types
export const ErrorTypes = {
  NETWORK: 'NETWORK_ERROR',
  DATABASE: 'DATABASE_ERROR',
  VALIDATION: 'VALIDATION_ERROR',
  AUTH: 'AUTHENTICATION_ERROR',
  PERMISSION: 'PERMISSION_ERROR',
  NOT_FOUND: 'NOT_FOUND_ERROR',
  SERVER: 'SERVER_ERROR',
  UNKNOWN: 'UNKNOWN_ERROR'
};

// Error messages in Belarusian
export const ErrorMessages = {
  [ErrorTypes.NETWORK]: {
    title: 'Памылка сеткі',
    default: 'Не ўдалося падключыцца да сервера. Праверце падключэнне да інтэрнэту.',
    retry: 'Паспрабаваць зноў'
  },
  [ErrorTypes.DATABASE]: {
    title: 'Памылка базы дадзеных',
    default: 'Памылка пры працы з базай дадзеных.',
    retry: 'Паспрабаваць зноў'
  },
  [ErrorTypes.VALIDATION]: {
    title: 'Памылка праверкі',
    default: 'Уведзены няправільныя даныя.',
    retry: 'Выправіць'
  },
  [ErrorTypes.AUTH]: {
    title: 'Памылка аўтэнтыфікацыі',
    default: 'Няправільны пароль або карыстальнік.',
    retry: 'Паспрабаваць зноў'
  },
  [ErrorTypes.PERMISSION]: {
    title: 'Няма доступу',
    default: 'У вас няма правоў для выканання гэтай аперацыі.',
    retry: 'Звярнуцца да адміністратара'
  },
  [ErrorTypes.NOT_FOUND]: {
    title: 'Не знойдзена',
    default: 'Запытаныя даныя не знойдзены.',
    retry: 'Вярнуцца назад'
  },
  [ErrorTypes.SERVER]: {
    title: 'Памылка сервера',
    default: 'Сервер не адказаў. Паспрабуйце пазней.',
    retry: 'Паспрабаваць зноў'
  },
  [ErrorTypes.UNKNOWN]: {
    title: 'Невядомая памылка',
    default: 'Адбылася нечаканая памылка.',
    retry: 'Паспрабаваць зноў'
  }
};

/**
 * Custom Error Class with additional context
 */
export class AppError extends Error {
  constructor(type, message, details = null, originalError = null) {
    super(message);
    this.name = 'AppError';
    this.type = type;
    this.details = details;
    this.originalError = originalError;
    this.timestamp = new Date().toISOString();
  }

  /**
   * Get user-friendly error message
   */
  getUserMessage() {
    const errorConfig = ErrorMessages[this.type] || ErrorMessages[ErrorTypes.UNKNOWN];
    return {
      title: errorConfig.title,
      message: this.message || errorConfig.default,
      details: this.details,
      retryText: errorConfig.retry
    };
  }

  /**
   * Log error for debugging
   */
  log() {
    console.error('=== AppError ===');
    console.error('Type:', this.type);
    console.error('Message:', this.message);
    console.error('Details:', this.details);
    console.error('Timestamp:', this.timestamp);
    if (this.originalError) {
      console.error('Original Error:', this.originalError);
    }
    console.error('===============');
  }
}

/**
 * Create specific error types
 */
export const createError = {
  network: (message, details) => new AppError(ErrorTypes.NETWORK, message, details),
  database: (message, details) => new AppError(ErrorTypes.DATABASE, message, details),
  validation: (message, details) => new AppError(ErrorTypes.VALIDATION, message, details),
  auth: (message, details) => new AppError(ErrorTypes.AUTH, message, details),
  permission: (message, details) => new AppError(ErrorTypes.PERMISSION, message, details),
  notFound: (message, details) => new AppError(ErrorTypes.NOT_FOUND, message, details),
  server: (message, details) => new AppError(ErrorTypes.SERVER, message, details),
  unknown: (error, details) => new AppError(ErrorTypes.UNKNOWN, error?.message || 'Невядомая памылка', details, error)
};

/**
 * Handle API errors with proper error type detection
 */
export const handleApiError = (error) => {
  // Log original error for debugging
  console.error('API Error:', error);

  // Handle AppError instances
  if (error instanceof AppError) {
    error.log();
    return error;
  }

  // Handle fetch/network errors
  if (!navigator.onLine) {
    return createError.network('Адсутнічае падключэнне да інтэрнэту');
  }

  // Handle HTTP errors
  if (error.response) {
    const { status, data } = error.response;

    switch (status) {
      case 401:
        return createError.auth('Няправільныя ўліковыя даныя', data);
      case 403:
        return createError.permission('Доступ забаронены', data);
      case 404:
        return createError.notFound('Рэсурс не знойдзены', data);
      case 422:
        return createError.validation('Памылка праверкі даных', data.errors);
      case 500:
      case 502:
      case 503:
        return createError.server('Памылка сервера', { status, data });
      default:
        return createError.unknown(error, { status, data });
    }
  }

  // Handle request errors (timeout, CORS, etc.)
  if (error.request) {
    return createError.network('Сервер не адказвае', error.request);
  }

  // Handle other errors
  return createError.unknown(error);
};

/**
 * Async error handler wrapper
 * Usage: const result = await withErrorHandler(apiCall());
 * Returns: { success: boolean, data?: any, error?: AppError }
 */
export const withErrorHandler = async (promise) => {
  try {
    const data = await promise;
    return { success: true, data, error: null };
  } catch (error) {
    const appError = handleApiError(error);
    appError.log();
    return { success: false, data: null, error: appError };
  }
};

/**
 * Error boundary component props validator
 */
export const validateErrorBoundaryProps = (error, errorInfo) => {
  if (!error) {
    console.warn('ErrorBoundary: No error provided');
    return false;
  }
  return true;
};

/**
 * Retry function with exponential backoff
 */
export const retryWithBackoff = async (fn, maxRetries = 3, initialDelay = 1000) => {
  let lastError;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // Don't retry on certain error types
      if (error instanceof AppError && 
          [ErrorTypes.AUTH, ErrorTypes.PERMISSION, ErrorTypes.VALIDATION].includes(error.type)) {
        break;
      }
      
      // Wait before retrying (exponential backoff)
      const delay = initialDelay * Math.pow(2, attempt);
      console.log(`Retry attempt ${attempt + 1}/${maxRetries} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw handleApiError(lastError);
};

/**
 * Get error type from error message or code
 */
export const getErrorType = (error) => {
  if (error instanceof AppError) {
    return error.type;
  }
  
  if (error?.code) {
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      return ErrorTypes.NETWORK;
    }
    if (error.code === 'SQL_ERROR' || error.code === 'DB_ERROR') {
      return ErrorTypes.DATABASE;
    }
  }
  
  if (error?.message) {
    const msg = error.message.toLowerCase();
    if (msg.includes('network') || msg.includes('fetch')) return ErrorTypes.NETWORK;
    if (msg.includes('database') || msg.includes('sql')) return ErrorTypes.DATABASE;
    if (msg.includes('auth') || msg.includes('login')) return ErrorTypes.AUTH;
    if (msg.includes('permission') || msg.includes('forbidden')) return ErrorTypes.PERMISSION;
    if (msg.includes('not found') || msg.includes('404')) return ErrorTypes.NOT_FOUND;
  }
  
  return ErrorTypes.UNKNOWN;
};
