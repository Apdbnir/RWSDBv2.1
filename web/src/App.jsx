import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import WelcomePage from './pages/WelcomePage';
import CUALayout from './components/CUALayout';
import Dashboard from './pages/Dashboard';
import Databases from './pages/Databases';
import Queries from './pages/Queries';
import SpecialQueries from './pages/SpecialQueries';
import Export from './pages/Export';
import Backup from './pages/Backup';
import Lab3Page from './pages/Lab3Page';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <AuthProvider>
        <NotificationProvider>
          <Routes>
            {/* Welcome/Landing Page */}
            <Route path="/" element={<WelcomePage />} />
            
            {/* Protected Main App Layout */}
            <Route path="/app" element={<ProtectedRoute />}>
              <Route element={<CUALayout />}>
                <Route index element={<Dashboard />} />
              <Route path="databases" element={<Databases />} />
              <Route path="queries" element={<Queries />} />
              <Route path="special" element={<SpecialQueries />} />
              <Route path="export" element={<Export />} />
              <Route path="backup" element={<Backup />} />
              <Route path="converter" element={<Lab3Page />} />
            </Route>
            </Route>
            
            {/* Redirect unknown paths to welcome page */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </NotificationProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
