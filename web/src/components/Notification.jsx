import { useNotification } from '../context/NotificationContext';

const Notification = () => {
  const { notification, hideNotification } = useNotification();

  if (!notification) return null;

  const bgColors = {
    success: 'bg-green-600',
    error: 'bg-red-600',
    info: 'bg-primary-600',
  };

  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
  };

  return (
    <div
      className={`fixed bottom-4 right-4 px-6 py-4 rounded-lg shadow-lg transform transition-all duration-300 z-50 ${bgColors[notification.type]} text-white flex items-center gap-3 animate-slide-in`}
      onClick={hideNotification}
    >
      <span className="text-xl font-bold">{icons[notification.type]}</span>
      <span>{notification.message}</span>
    </div>
  );
};

export default Notification;
