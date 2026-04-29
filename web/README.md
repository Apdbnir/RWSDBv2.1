# RWSDBv2.1 React Client

Modern React-based web interface for the Railway Station Database System v2.1.

## Tech Stack

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API communication

## Features

- 📊 **Dashboard** - Overview of database statistics and quick access to tables
- 📚 **Tables** - Browse, filter, add, edit, and delete records with role-based access control
- 💻 **SQL Queries** - Execute custom SELECT queries with preset templates
- 🔍 **Special Queries** - Pre-defined analytical queries for common operations
- 📁 **Export** - Export data to JSON, CSV, or Excel formats
- 💾 **Backup** - Create database backups (superuser only)

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- RWSDBv2.1 backend server running on port 8080

### Installation

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

### Building for Production

```bash
npm run build
```

The production build will be generated in the `dist` folder.

## Project Structure

```
client/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── DataTable.jsx
│   │   ├── Header.jsx
│   │   ├── Layout.jsx
│   │   ├── LoginModal.jsx
│   │   ├── Modal.jsx
│   │   ├── Navigation.jsx
│   │   └── Notification.jsx
│   ├── context/          # React Context providers
│   │   ├── AuthContext.jsx
│   │   └── NotificationContext.jsx
│   ├── pages/            # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Tables.jsx
│   │   ├── Queries.jsx
│   │   ├── SpecialQueries.jsx
│   │   ├── Export.jsx
│   │   └── Backup.jsx
│   ├── services/         # API and external services
│   │   └── api.js
│   ├── App.jsx           # Main App component with routing
│   ├── main.jsx          # Application entry point
│   └── index.css         # Global styles with Tailwind
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
└── vite.config.js
```

## API Integration

The React client communicates with the backend server via REST API:

- **Base URL**: `/api` (proxied to `http://localhost:8080/api` in development)
- **Authentication**: Bearer token in Authorization header for superuser actions
- **Format**: JSON for all requests and responses

### API Endpoints Used

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{table}` | Get table data with pagination |
| POST | `/api/{table}` | Create new record |
| PUT | `/api/{table}/{id}` | Update record |
| DELETE | `/api/{table}/{id}` | Delete record |
| POST | `/api/custom_query` | Execute SQL query |
| GET | `/api/statistics` | Get database statistics |
| POST | `/api/backup` | Create database backup |
| POST | `/api/export` | Export data |

## Authentication

### Superuser Access

Default password: `4444`

Superusers can:
- Modify lookup tables (positions, subjects, lesson_types)
- Create database backups
- Access the backup page

## Features in Detail

### Dashboard
- Real-time database statistics
- Quick access buttons to all tables
- Visual cards showing key metrics

### Tables
- Sidebar navigation for all tables
- Filter records by name
- Pagination support (20 records per page)
- Add, edit, delete operations
- Lookup table protection (read-only for regular users)

### SQL Queries
- Custom SELECT query execution
- Preset query templates
- Query history
- Results displayed in data table

### Special Queries
- Pre-defined analytical queries organized by category:
  - Statistics & Analytics
  - Schedule & Trains
  - Employees & Assignments
  - Tickets & Passengers
  - Services & Works

### Export
- Export to JSON, CSV, or Excel formats
- Support for custom SQL queries
- Export history tracking
- Up to 10,000 records per export

### Backup
- Create full database backups
- View backup history
- File size and status tracking
- Superuser only feature

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Environment Variables

Create a `.env` file in the client directory for environment-specific configuration:

```env
VITE_API_URL=http://localhost:8080/api
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is part of the RWSDBv2.1 (Railway Station Database System v2.1).
