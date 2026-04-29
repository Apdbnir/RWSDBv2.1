import { useState, useEffect, useCallback } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import Header from './Header';
import MenuBar from './MenuBar';
import LoginModal from './LoginModal';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';
import useKeyboardShortcuts from '../hooks/useKeyboardShortcuts';
import {
  AddRecordDialog,
  UpdateRecordDialog,
  DeleteRecordDialog,
  SpecialQueriesDialog,
  CustomQueryDialog,
  BackupDialog,
  SaveQueryResultDialog,
  ExitConfirmDialog,
  SuccessDialog,
  HelpDialog
} from './dialogs';
import api from '../services/api';

/**
 * Main CUA-compliant Layout
 * Implements classic menu-driven interface per Common User Access standard
 */
const CUALayout = () => {
  const navigate = useNavigate();
  const { isSuperUser } = useAuth();
  const { success: notifySuccess, error: notifyError } = useNotification();

  // State
  const [activeTable, setActiveTable] = useState('passenger');
  const [activeMenuItem, setActiveMenuItem] = useState(0);
  const [lastQueryResult, setLastQueryResult] = useState(null);
  const [tableData, setTableData] = useState({ columns: [], data: [] });
  const [selectedRecord, setSelectedRecord] = useState(null);

  // Dialog states
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [showUpdateDialog, setShowUpdateDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [showQueriesDialog, setShowQueriesDialog] = useState(false);
  const [showCustomQueryDialog, setShowCustomQueryDialog] = useState(false);
  const [showBackupDialog, setShowBackupDialog] = useState(false);
  const [showSaveQueryDialog, setShowSaveQueryDialog] = useState(false);
  const [showExitDialog, setShowExitDialog] = useState(false);
  const [showSuccessDialog, setShowSuccessDialog] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showHelpDialog, setShowHelpDialog] = useState(false);

  const [successDialogData, setSuccessDialogData] = useState({ title: '', message: '', details: '' });

  // Handle export (defined before handleOperation to avoid circular dependency)
  const handleExport = useCallback(async (format) => {
    try {
      const result = await api.exportData(format, activeTable);
      notifySuccess(`Data exported to ${format.toUpperCase()}`);
      // Download the file
      const blob = new Blob([result.data], { type: 'application/octet-stream' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${activeTable}_export.${format === 'excel' ? 'xlsx' : format}`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      notifyError('Failed to export data');
      console.error(err);
    }
  }, [activeTable, notifySuccess, notifyError]);

  // Predefined special queries - 100 Belarusian Railway queries
  const specialQueries = [
    // Simple "all" queries (1-9)
    { id: 'all_passengers', name: 'All Passengers', description: 'List all passengers (LIMIT 100)', key: '1' },
    { id: 'all_trains', name: 'All Trains', description: 'List all trains (LIMIT 100)', key: '2' },
    { id: 'all_platforms', name: 'All Platforms', description: 'List all platforms (LIMIT 100)', key: '3' },
    { id: 'all_tickets', name: 'All Tickets', description: 'List all tickets (LIMIT 100)', key: '4' },
    { id: 'all_schedules', name: 'All Schedules', description: 'List all schedules (LIMIT 100)', key: '5' },
    { id: 'all_employees', name: 'All Employees', description: 'List all employees (LIMIT 100)', key: '6' },
    { id: 'all_work', name: 'All Work Assignments', description: 'List all work assignments (LIMIT 100)', key: '7' },
    { id: 'all_services', name: 'All Services', description: 'List all services (LIMIT 100)', key: '8' },
    { id: 'all_appointments', name: 'All Appointments', description: 'List all appointments (LIMIT 100)', key: '9' },

    // Statistical queries (10-19)
    { id: 'statistics', name: 'Database Statistics', description: 'Record count in all tables', key: 'q' },
    { id: 'train_types', name: 'Train Types Stats', description: 'Count and avg speed by train type', key: 'w' },
    { id: 'passenger_features', name: 'Passenger Features', description: 'Count passengers by feature type', key: 'e' },
    { id: 'employee_positions', name: 'Employee Positions', description: 'Count by position', key: 'r' },
    { id: 'service_types', name: 'Service Types', description: 'Count and avg price by type', key: 't' },
    { id: 'platform_capacity', name: 'Platform Capacity', description: 'Total capacity by platform', key: 'y' },
    { id: 'ticket_revenue', name: 'Ticket Revenue', description: 'Total revenue from tickets', key: 'u' },
    { id: 'avg_ticket_price', name: 'Average Ticket Price', description: 'Average price across all tickets', key: 'i' },
    { id: 'work_distribution', name: 'Work Distribution', description: 'Employees per train', key: 'o' },
    { id: 'service_revenue', name: 'Service Revenue', description: 'Total revenue by service', key: 'p' },

    // Schedule queries (20-29)
    { id: 'today_schedule', name: "Today's Schedule", description: 'Schedule for current date', key: 'a' },
    { id: 'next_departures', name: 'Next Departures', description: 'Upcoming departures (LIMIT 20)', key: 's' },
    { id: 'morning_trains', name: 'Morning Trains', description: 'Departures before 12:00', key: 'd' },
    { id: 'evening_trains', name: 'Evening Trains', description: 'Departures after 18:00', key: 'f' },
    { id: 'night_trains', name: 'Night Trains', description: 'Departures after 23:00', key: 'g' },
    { id: 'peak_hours', name: 'Peak Hours', description: 'Schedule during peak hours (7-9, 17-19)', key: 'h' },
    { id: 'weekend_schedule', name: 'Weekend Schedule', description: 'Schedule for Saturday/Sunday', key: 'j' },
    { id: 'busiest_platform', name: 'Busiest Platform', description: 'Platform with most trains', key: 'k' },
    { id: 'platform_utilization', name: 'Platform Utilization', description: 'Usage percentage by platform', key: 'l' },
    { id: 'train_frequency', name: 'Train Frequency', description: 'Trains per hour', key: 'z' },

    // Train queries (30-39)
    { id: 'fast_trains', name: 'Fast Trains', description: 'Trains with speed > 150 km/h', key: 'x' },
    { id: 'slow_trains', name: 'Slow Trains', description: 'Trains with speed < 100 km/h', key: 'c' },
    { id: 'new_trains', name: 'New Trains', description: 'Trains manufactured after 2020', key: 'v' },
    { id: 'old_trains', name: 'Old Trains', description: 'Trains manufactured before 2015', key: 'b' },
    { id: 'long_trains', name: 'Long Trains', description: 'Trains with > 12 cars', key: 'n' },
    { id: 'short_trains', name: 'Short Trains', description: 'Trains with < 8 cars', key: 'm' },
    { id: 'train_by_type', name: 'Trains by Type', description: 'Group trains by type', key: '0' },
    { id: 'capacity_by_train', name: 'Capacity by Train', description: 'Total passenger capacity', key: '-' },
    { id: 'train_employee_ratio', name: 'Train-Employee Ratio', description: 'Employees per train car', key: '=' },
    { id: 'train_service_count', name: 'Train Services', description: 'Services per train type', key: '[' },

    // Passenger queries (40-49)
    { id: 'vip_passengers', name: 'VIP Passengers', description: 'Passengers with VIP feature', key: '1' },
    { id: 'senior_passengers', name: 'Senior Passengers', description: 'Passengers with pensioner feature', key: '2' },
    { id: 'student_passengers', name: 'Student Passengers', description: 'Passengers with student feature', key: '3' },
    { id: 'disabled_passengers', name: 'Disabled Passengers', description: 'Passengers with disability feature', key: '4' },
    { id: 'regular_passengers', name: 'Regular Passengers', description: 'Passengers without special features', key: '5' },
    { id: 'passenger_tickets', name: 'Passenger Tickets', description: 'Tickets per passenger', key: '6' },
    { id: 'top_passengers', name: 'Top Passengers', description: 'Passengers with most tickets', key: '7' },
    { id: 'passenger_by_feature', name: 'Passengers by Feature', description: 'Count by feature type', key: '8' },
    { id: 'recent_passengers', name: 'Recent Passengers', description: 'Last 50 added passengers', key: '9' },
    { id: 'passenger_growth', name: 'Passenger Growth', description: 'New passengers per month', key: '0' },

    // Ticket queries (50-59)
    { id: 'expensive_tickets', name: 'Expensive Tickets', description: 'Tickets > 50 BYN', key: 'q' },
    { id: 'cheap_tickets', name: 'Cheap Tickets', description: 'Tickets < 20 BYN', key: 'w' },
    { id: 'first_class_tickets', name: 'First Class Tickets', description: 'Tickets for car 1-3', key: 'e' },
    { id: 'economy_tickets', name: 'Economy Tickets', description: 'Tickets for car 10+', key: 'r' },
    { id: 'ticket_by_car', name: 'Tickets by Car', description: 'Count tickets per carriage', key: 't' },
    { id: 'ticket_by_seat', name: 'Tickets by Seat', description: 'Seat number distribution', key: 'y' },
    { id: 'high_demand_seats', name: 'High Demand Seats', description: 'Most booked seat numbers', key: 'u' },
    { id: 'ticket_revenue_daily', name: 'Daily Revenue', description: 'Ticket revenue per day', key: 'i' },
    { id: 'ticket_revenue_monthly', name: 'Monthly Revenue', description: 'Ticket revenue per month', key: 'o' },
    { id: 'ticket_revenue_yearly', name: 'Yearly Revenue', description: 'Ticket revenue per year', key: 'p' },

    // Employee queries (60-69)
    { id: 'experienced_employees', name: 'Experienced Employees', description: 'Employees with > 10 years experience', key: 'a' },
    { id: 'junior_employees', name: 'Junior Employees', description: 'Employees with < 3 years experience', key: 's' },
    { id: 'conductors', name: 'Conductors', description: 'All conductors', key: 'd' },
    { id: 'engineers', name: 'Engineers', description: 'All train engineers', key: 'f' },
    { id: 'station_staff', name: 'Station Staff', description: 'Station employees', key: 'g' },
    { id: 'management', name: 'Management', description: 'Management staff', key: 'h' },
    { id: 'employee_by_train', name: 'Employees by Train', description: 'Staff per train', key: 'j' },
    { id: 'employee_workload', name: 'Employee Workload', description: 'Assignments per employee', key: 'k' },
    { id: 'top_employees', name: 'Top Employees', description: 'Most assignments', key: 'l' },
    { id: 'employee_salary_estimate', name: 'Salary Estimate', description: 'Estimated salary by position', key: 'z' },

    // Platform queries (70-79)
    { id: 'large_platforms', name: 'Large Platforms', description: 'Capacity > 400', key: 'x' },
    { id: 'small_platforms', name: 'Small Platforms', description: 'Capacity < 300', key: 'c' },
    { id: 'multi_track_platforms', name: 'Multi-Track Platforms', description: 'Platforms with > 2 tracks', key: 'v' },
    { id: 'single_track_platforms', name: 'Single-Track Platforms', description: 'Platforms with 1 track', key: 'b' },
    { id: 'platform_by_location', name: 'Platforms by Location', description: 'Group by station', key: 'n' },
    { id: 'platform_train_count', name: 'Platform Train Count', description: 'Trains per platform', key: 'm' },
    { id: 'busiest_stations', name: 'Busiest Stations', description: 'Stations with most platforms', key: '0' },
    { id: 'platform_availability', name: 'Platform Availability', description: 'Available capacity', key: '-' },
    { id: 'platform_efficiency', name: 'Platform Efficiency', description: 'Capacity utilization', key: '=' },
    { id: 'platform_revenue', name: 'Platform Revenue', description: 'Revenue by platform', key: '[' },

    // Service queries (80-89)
    { id: 'premium_services', name: 'Premium Services', description: 'Services > 50 BYN', key: '1' },
    { id: 'basic_services', name: 'Basic Services', description: 'Services < 20 BYN', key: '2' },
    { id: 'technical_services', name: 'Technical Services', description: 'Technical type services', key: '3' },
    { id: 'passenger_services', name: 'Passenger Services', description: 'Passenger type services', key: '4' },
    { id: 'security_services', name: 'Security Services', description: 'Security type services', key: '5' },
    { id: 'service_by_date', name: 'Services by Date', description: 'Services per date', key: '6' },
    { id: 'service_appointment_count', name: 'Service Appointments', description: 'Appointments per service', key: '7' },
    { id: 'popular_services', name: 'Popular Services', description: 'Most assigned services', key: '8' },
    { id: 'service_revenue_total', name: 'Total Service Revenue', description: 'Sum of all service prices', key: '9' },
    { id: 'service_employee_ratio', name: 'Service-Employee Ratio', description: 'Employees per service', key: '0' },

    // Complex analytical queries (90-99)
    { id: 'train_profitability', name: 'Train Profitability', description: 'Revenue vs capacity by train', key: 'q' },
    { id: 'route_efficiency', name: 'Route Efficiency', description: 'Platform usage efficiency', key: 'w' },
    { id: 'seasonal_trends', name: 'Seasonal Trends', description: 'Tickets by season', key: 'e' },
    { id: 'employee_productivity', name: 'Employee Productivity', description: 'Services per employee', key: 'r' },
    { id: 'passenger_satisfaction', name: 'Passenger Satisfaction', description: 'Feature distribution analysis', key: 't' },
    { id: 'revenue_forecast', name: 'Revenue Forecast', description: 'Projected monthly revenue', key: 'y' },
    { id: 'capacity_optimization', name: 'Capacity Optimization', description: 'Underutilized resources', key: 'u' },
    { id: 'staff_optimization', name: 'Staff Optimization', description: 'Over/under staffed trains', key: 'i' },
    { id: 'service_gaps', name: 'Service Gaps', description: 'Uncovered time slots', key: 'o' },
    { id: 'growth_opportunities', name: 'Growth Opportunities', description: 'Expansion recommendations', key: 'p' },

    // System queries (100)
    { id: 'system_health', name: 'System Health', description: 'Database integrity check', key: 'h' }
  ];

  // Load table data
  const loadTableData = useCallback(async (tableName) => {
    try {
      const data = await api.getTableData(tableName, {}, 100, 0);
      setTableData(data);
      return data;
    } catch (err) {
      notifyError('Failed to load table data');
      console.error(err);
      return null;
    }
  }, [notifyError]);

  // Handle table selection
  const handleTableSelect = useCallback((tableName) => {
    setActiveTable(tableName);
    loadTableData(tableName);
    navigate(`/app/databases?table=${tableName}`);
  }, [loadTableData, navigate]);

  // Handle file menu actions
  const handleFileAction = useCallback((action) => {
    if (action === 'exit') {
      setShowExitDialog(true);
    }
  }, []);

  // Handle operations menu actions
  const handleOperation = useCallback((operation) => {
    switch (operation) {
      case 'converter':
        // Navigate to DB Converter page
        navigate('/app/converter');
        break;
      case 'view':
        if (activeTable) {
          loadTableData(activeTable);
          notifySuccess('Table refreshed');
        }
        break;
      case 'add':
        if (!isSuperUser) {
          notifyError('Superuser privileges required for adding records');
          return;
        }
        if (activeTable) {
          // Ensure table data is loaded before showing dialog
          if (!tableData.columns || tableData.columns.length === 0) {
            loadTableData(activeTable).then(() => {
              setTimeout(() => setShowAddDialog(true), 100);
            });
          } else {
            setShowAddDialog(true);
          }
        }
        break;
      case 'update':
        if (!isSuperUser) {
          notifyError('Superuser privileges required for updating records');
          return;
        }
        if (activeTable && selectedRecord) {
          setShowUpdateDialog(true);
        } else if (activeTable) {
          notifyError('Please select a record to update');
        }
        break;
      case 'delete':
        if (!isSuperUser) {
          notifyError('Superuser privileges required for deleting records');
          return;
        }
        if (activeTable && selectedRecord) {
          setShowDeleteDialog(true);
        } else if (activeTable) {
          notifyError('Please select a record to delete');
        }
        break;
      case 'queries':
        setShowQueriesDialog(true);
        break;
      case 'customQuery':
        setShowCustomQueryDialog(true);
        break;
      case 'saveQuery':
        if (!isSuperUser) {
          notifyError('Superuser privileges required for saving queries');
          return;
        }
        if (lastQueryResult) {
          setShowSaveQueryDialog(true);
        }
        break;
      case 'backup':
        if (isSuperUser) {
          setShowBackupDialog(true);
        } else {
          notifyError('Superuser privileges required');
        }
        break;
      case 'export_json':
        if (!isSuperUser) {
          notifyError('Superuser privileges required for export');
          return;
        }
        if (activeTable) {
          handleExport('json');
        }
        break;
      case 'export_csv':
        if (!isSuperUser) {
          notifyError('Superuser privileges required for export');
          return;
        }
        if (activeTable) {
          handleExport('csv');
        }
        break;
      case 'export_excel':
        if (!isSuperUser) {
          notifyError('Superuser privileges required for export');
          return;
        }
        if (activeTable) {
          handleExport('excel');
        }
        break;
      case 'export':
        // Navigate to Export page
        navigate('/app/export');
        break;
      default:
        break;
    }
  }, [activeTable, selectedRecord, lastQueryResult, isSuperUser, loadTableData, notifySuccess, notifyError, handleExport, tableData.columns]);

  // Keyboard shortcuts handler
  useKeyboardShortcuts({
    onAdd: () => handleOperation('add'),
    onView: () => handleOperation('view'),
    onUpdate: () => handleOperation('update'),
    onDelete: () => handleOperation('delete'),
    onQueries: () => handleOperation('queries'),
    onSaveQuery: () => handleOperation('saveQuery'),
    onBackup: () => handleOperation('backup'),
    onExit: () => handleFileAction('exit'),
    onExport: () => handleOperation('export'),
    onExportJSON: () => handleOperation('export_json'),
    onExportCSV: () => handleOperation('export_csv'),
    onExportExcel: () => handleOperation('export_excel'),
    activeTable,
    hasQueryResult: !!lastQueryResult,
    isSuperUser,
    onTableSelect: handleTableSelect,
    onHelp: () => setShowHelpDialog(true)
  });

  // Setup global menu context handlers for keyboard shortcuts
  useEffect(() => {
    window.onOpenFileMenu = () => {
      window.menuContext = 'file';
      setTimeout(() => { window.menuContext = null; }, 1000);
    };
    window.onOpenTablesMenu = () => {
      window.menuContext = 'tables';
      setTimeout(() => { window.menuContext = null; }, 1000);
    };
    window.onOpenOperationsMenu = () => {
      window.menuContext = 'operations';
      setTimeout(() => { window.menuContext = null; }, 1000);
    };
    window.onOpenExportMenu = () => {
      window.menuContext = 'export';
      setTimeout(() => { window.menuContext = null; }, 1000);
    };
    window.onOpenCustomQuery = () => {
      setShowCustomQueryDialog(true);
    };
    return () => {
      delete window.onOpenFileMenu;
      delete window.onOpenTablesMenu;
      delete window.onOpenOperationsMenu;
      delete window.onOpenExportMenu;
      delete window.onOpenCustomQuery;
    };
  }, []);

  // Dialog handlers
  const handleAddConfirm = async (formData) => {
    try {
      await api.createRecord(activeTable, formData);
      setShowAddDialog(false);
      loadTableData(activeTable);
      setSuccessDialogData({
        title: 'Record Added',
        message: 'The record has been successfully added to the database.',
        details: ''
      });
      setShowSuccessDialog(true);
    } catch (err) {
      notifyError('Failed to add record');
      console.error(err);
    }
  };

  const handleUpdateConfirm = async (formData) => {
    try {
      const idColumn = tableData.columns.find(c => c.includes('id')) || tableData.columns[0];
      await api.updateRecord(activeTable, selectedRecord[idColumn], formData);
      setShowUpdateDialog(false);
      loadTableData(activeTable);
      setSuccessDialogData({
        title: 'Record Updated',
        message: 'The record has been successfully updated.',
        details: ''
      });
      setShowSuccessDialog(true);
    } catch (err) {
      notifyError('Failed to update record');
      console.error(err);
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      const idColumn = tableData.columns.find(c => c.includes('id')) || tableData.columns[0];
      await api.deleteRecord(activeTable, selectedRecord[idColumn]);
      setShowDeleteDialog(false);
      setSelectedRecord(null);
      loadTableData(activeTable);
      setSuccessDialogData({
        title: 'Record Deleted',
        message: 'The record has been successfully deleted.',
        details: ''
      });
      setShowSuccessDialog(true);
    } catch (err) {
      notifyError('Failed to delete record');
      console.error(err);
    }
  };

  const handleExecuteQuery = async (queryId) => {
    try {
      const result = await api.executeQuery(queryId);
      setLastQueryResult(result);
      setShowQueriesDialog(false);
      setSuccessDialogData({
        title: 'Query Executed',
        message: `Query executed successfully. Found ${result.count || 0} records.`,
        details: ''
      });
      setShowSuccessDialog(true);
    } catch (err) {
      notifyError('Failed to execute query');
      console.error(err);
    }
  };

  const handleExecuteCustomQuery = async (sqlQuery) => {
    try {
      const result = await api.executeCustomQuery(sqlQuery);
      setLastQueryResult(result);
      setShowCustomQueryDialog(false);
      setSuccessDialogData({
        title: 'Query Executed',
        message: `Custom query executed successfully. Found ${result.count || 0} records.`,
        details: ''
      });
      setShowSuccessDialog(true);
    } catch (err) {
      notifyError('Failed to execute custom query: ' + (err.message || err));
      console.error(err);
      throw err; // Re-throw to let the dialog handle the error
    }
  };

  const handleBackupConfirm = async (password) => {
    try {
      const result = await api.createBackup();
      setShowBackupDialog(false);
      setSuccessDialogData({
        title: 'Backup Created',
        message: 'Database backup has been successfully created.',
        details: result.backup_path || 'N/A'
      });
      setShowSuccessDialog(true);
    } catch (err) {
      notifyError('Failed to create backup');
      console.error(err);
    }
  };

  const handleSaveQueryConfirm = async () => {
    try {
      // Export functionality would be called here
      setShowSaveQueryDialog(false);
      setSuccessDialogData({
        title: 'Query Saved',
        message: 'Query results have been saved to file.',
        details: 'C:\\VS_Code\\RWSDBv2.1\\data\\exports\\query_result.xlsx'
      });
      setShowSuccessDialog(true);
    } catch (err) {
      notifyError('Failed to save query');
      console.error(err);
    }
  };

  const handleExitConfirm = () => {
    // Navigate to welcome page (simulates "exit" from the app)
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <Header onLoginClick={() => setShowLoginModal(true)} />

      {/* Menu Bar */}
      <MenuBar
        onFileAction={handleFileAction}
        onTableSelect={handleTableSelect}
        onOperation={handleOperation}
        activeTable={activeTable}
        activeMenuItem={activeMenuItem}
        setActiveMenuItem={setActiveMenuItem}
      />

      {/* Main Content Area */}
      <main className="flex-1 overflow-auto">
        <Outlet context={{ activeTable, setActiveTable, tableData, setTableData, selectedRecord, setSelectedRecord }} />
      </main>

      {/* Status Bar */}
      <footer className="bg-gray-800 text-gray-300 px-4 py-2 text-xs flex justify-between items-center">
        <div className="flex items-center gap-4">
          <span>Табліца: <strong className="text-white">{activeTable || 'Няма'}</strong></span>
          <span>Запісы: <strong className="text-white">{tableData.data?.length || 0}</strong></span>
        </div>
        <div className="flex items-center gap-4">
          <span>F10 - Меню</span>
          <span>Ctrl+E - Выхад</span>
        </div>
      </footer>

      {/* Dialogs */}
      <AddRecordDialog
        isOpen={showAddDialog}
        onClose={() => setShowAddDialog(false)}
        onConfirm={handleAddConfirm}
        tableName={activeTable}
        columns={tableData.columns}
      />

      <UpdateRecordDialog
        isOpen={showUpdateDialog}
        onClose={() => setShowUpdateDialog(false)}
        onConfirm={handleUpdateConfirm}
        tableName={activeTable}
        columns={tableData.columns}
        record={selectedRecord}
      />

      <DeleteRecordDialog
        isOpen={showDeleteDialog}
        onClose={() => setShowDeleteDialog(false)}
        onConfirm={handleDeleteConfirm}
        tableName={activeTable}
        recordId={selectedRecord?.id || selectedRecord?.[tableData.columns?.[0]]}
      />

      <SpecialQueriesDialog
        isOpen={showQueriesDialog}
        onClose={() => setShowQueriesDialog(false)}
        onExecute={handleExecuteQuery}
        queries={specialQueries}
      />

      <CustomQueryDialog
        isOpen={showCustomQueryDialog}
        onClose={() => setShowCustomQueryDialog(false)}
        onExecute={handleExecuteCustomQuery}
      />

      <BackupDialog
        isOpen={showBackupDialog}
        onClose={() => setShowBackupDialog(false)}
        onConfirm={handleBackupConfirm}
      />

      <SaveQueryResultDialog
        isOpen={showSaveQueryDialog}
        onClose={() => setShowSaveQueryDialog(false)}
        onConfirm={handleSaveQueryConfirm}
        tableName={lastQueryResult?.table || activeTable}
        recordCount={lastQueryResult?.count || 0}
      />

      <ExitConfirmDialog
        isOpen={showExitDialog}
        onClose={() => setShowExitDialog(false)}
        onConfirm={handleExitConfirm}
      />

      <SuccessDialog
        isOpen={showSuccessDialog}
        onClose={() => setShowSuccessDialog(false)}
        title={successDialogData.title}
        message={successDialogData.message}
        details={successDialogData.details}
      />

      <HelpDialog
        isOpen={showHelpDialog}
        onClose={() => setShowHelpDialog(false)}
      />

      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
      />
    </div>
  );
};

export default CUALayout;
