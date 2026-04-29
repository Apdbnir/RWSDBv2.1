import axios from 'axios';

const API_BASE_URL = '/api';

// Frontend logging utility
const logger = {
  info: (message, ...args) => {
    console.log(`[INFO] ${new Date().toISOString()} - ${message}`, ...args);
  },
  warn: (message, ...args) => {
    console.warn(`[WARN] ${new Date().toISOString()} - ${message}`, ...args);
  },
  error: (message, ...args) => {
    console.error(`[ERROR] ${new Date().toISOString()} - ${message}`, ...args);
  },
  debug: (message, ...args) => {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`[DEBUG] ${new Date().toISOString()} - ${message}`, ...args);
    }
  }
};

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
apiClient.interceptors.request.use((config) => {
  logger.info(`${config.method?.toUpperCase()} ${config.url}`);
  logger.debug('Request config:', config);
  
  const token = localStorage.getItem('superuser_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  logger.error('Request interceptor error:', error);
  return Promise.reject(error);
});

// Add response interceptor for logging
apiClient.interceptors.response.use(
  (response) => {
    logger.info(`Response ${response.status}: ${response.config.method?.toUpperCase()} ${response.config.url}`);
    logger.debug('Response data:', response.data);
    return response;
  },
  (error) => {
    if (error.response) {
      logger.error(`Response error ${error.response.status}: ${error.config?.method?.toUpperCase()} ${error.config?.url}`, error.response.data);
      if (error.response.status === 401) {
        logger.warn('Authentication failed, clearing token');
        localStorage.removeItem('superuser_token');
        window.dispatchEvent(new CustomEvent('auth-failed'));
      }
    } else if (error.request) {
      logger.error('No response received:', error.message);
    } else {
      logger.error('Request setup error:', error.message);
    }
    return Promise.reject(error);
  }
);

/**
 * API Service for RWSDBv2.1
 */
const api = {
  // Table operations
  getTableData: async (tableName, filters = {}, limit = 100, offset = 0) => {
    const params = new URLSearchParams({ limit: limit.toString(), offset: offset.toString() });
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
    
    const response = await apiClient.get(`/${tableName}?${params}`);
    return response.data;
  },

  getRecord: async (tableName, id) => {
    const response = await apiClient.get(`/${tableName}/${id}`);
    return response.data;
  },

  createRecord: async (tableName, data) => {
    const response = await apiClient.post(`/${tableName}`, data);
    return response.data;
  },

  updateRecord: async (tableName, id, data) => {
    const response = await apiClient.put(`/${tableName}/${id}`, data);
    return response.data;
  },

  deleteRecord: async (tableName, id) => {
    const response = await apiClient.delete(`/${tableName}/${id}`);
    return response.data;
  },

  // Predefined query execution
  executeQuery: async (queryName) => {
    logger.info(`Executing predefined query: ${queryName}`);
    try {
      const response = await apiClient.post('/queries', { query: queryName });
      logger.info(`Predefined query '${queryName}' completed: ${response.data?.count || 0} rows`);
      return response.data;
    } catch (error) {
      logger.error(`Predefined query '${queryName}' failed:`, error);
      throw new Error(error.response?.data?.error || error.message || 'Query execution failed');
    }
  },

  // Custom SQL query execution (SELECT only)
  executeCustomQuery: async (sqlQuery) => {
    logger.info(`Executing custom SQL query`);
    logger.debug('Query SQL:', sqlQuery);
    try {
      const response = await apiClient.post('/custom-query', { query: sqlQuery });
      logger.info(`Custom query completed: ${response.data?.count || 0} rows`);
      return response.data;
    } catch (error) {
      logger.error('Custom query failed:', error);
      throw new Error(error.response?.data?.error || error.message || 'Custom query execution failed');
    }
  },

  // Database statistics
  getStatistics: async () => {
    const response = await apiClient.get('/statistics');
    return response.data;
  },

  // Backup operations (superuser only)
  createBackup: async () => {
    const response = await apiClient.post('/backup');
    return response.data;
  },

  // Export operations
  exportData: async (format, tableName, query = null) => {
    const response = await apiClient.post('/export', {
      format,
      table: tableName,
      query,
    });
    return response.data;
  },

  // Authentication
  authenticate: async (password) => {
    const response = await apiClient.post('/login', { password });
    return response.data;
  },

  // BerkeleyDB conversion
  lab3Convert: async () => {
    logger.info('Starting BerkeleyDB conversion');
    try {
      const response = await apiClient.post('/lab3-convert', {});
      logger.info('BerkeleyDB conversion completed');
      return response.data;
    } catch (error) {
      logger.error('BerkeleyDB conversion failed:', error);
      throw new Error(error.response?.data?.error || error.message || 'Conversion failed');
    }
  },

  // Configuration
  getConfig: async () => {
    const response = await apiClient.get('/config');
    return response.data;
  },

  updateConfig: async (config) => {
    const response = await apiClient.post('/config', config);
    return response.data;
  },

  // Lookup tables (require superuser for modifications)
  isLookupTable: (tableName) => {
    const lookupTables = ['train', 'platform', 'service', 'employee'];
    return lookupTables.includes(tableName);
  },

  // Primary keys for each table
  getPrimaryKey: (tableName) => {
    const pkMap = {
      passenger: 'passenger_number',
      train: 'train_number',
      platform: 'platform_number',
      ticket: 'ticket_number',
      schedule: 'schedule_number',
      employee: 'employee_number',
      service: 'service_number',
      appointment: 'employee_number',
      work: 'train_number'
    };
    return pkMap[tableName] || 'id';
  }
};

export default api;
