import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import Modal from './Modal';
import { useNotification } from '../context/NotificationContext';

const LoginModal = ({ isOpen, onClose }) => {
  const { login } = useAuth();
  const { error } = useNotification();
  const [password, setPassword] = useState('');
  const [touched, setTouched] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Real-time password validation
  const isValid = password.length >= 1;
  const showError = touched && !isValid && password === '';

  const handleSubmit = async () => {
    setTouched(true);
    
    if (!password.trim()) {
      error('Увядзіце пароль');
      return;
    }

    try {
      setSubmitting(true);
      const result = await login(password);

      if (result.success) {
        onClose();
        setPassword('');
        setTouched(false);
      } else {
        error(result.error || 'Памылка аўтэнтыфікацыі');
      }
    } catch (err) {
      error('Памылка пры ўваходзе');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleBlur = () => {
    setTouched(true);
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="🔐 Уваход для суперкарыстальніка"
      size="sm"
      actions={
        <>
          <button
            onClick={onClose}
            className="btn btn-secondary"
            disabled={submitting}
          >
            Адмена
          </button>
          <button
            onClick={handleSubmit}
            disabled={submitting || !isValid}
            className={`btn btn-primary disabled:opacity-50 ${!isValid ? 'cursor-not-allowed' : ''}`}
          >
            {submitting ? (
              <>
                <span className="animate-spin">⏳</span> Уваход...
              </>
            ) : (
              <>
                🚀 Увайсці
              </>
            )}
          </button>
        </>
      }
    >
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Пароль
          </label>
          <input
            type="password"
            className={`input w-full ${showError ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''}`}
            placeholder="Увядзіце пароль суперкарыстальніка"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onBlur={handleBlur}
            onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
            autoFocus
          />
          {/* Real-time validation feedback */}
          {touched && (
            <div className="mt-1 text-xs">
              {isValid ? (
                <p className="text-green-600 flex items-center gap-1">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Гатова да ўваходу
                </p>
              ) : showError ? (
                <p className="text-red-600 flex items-center gap-1">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  Пароль абавязковы
                </p>
              ) : null}
            </div>
          )}
        </div>
        <p className="text-sm text-gray-500">
          💡 Пароль па змаўчанні: <strong className="text-gray-700">4444</strong>
        </p>
      </div>
    </Modal>
  );
};

export default LoginModal;
