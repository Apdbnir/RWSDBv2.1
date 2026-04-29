import { useState, useEffect } from 'react';
import { validateField, getFieldPlaceholder, getFieldLabel } from '../utils/validation';

/**
 * Input component with real-time validation
 * @param {object} props
 * @param {string} props.tableName - Table name for validation rules
 * @param {string} props.name - Field name
 * @param {any} props.value - Field value
 * @param {function} props.onChange - Change handler
 * @param {boolean} props.disabled - Disabled state
 * @param {string} props.type - Input type (text, number, date, time)
 */
const ValidatedInput = ({
  tableName,
  name,
  value,
  onChange,
  disabled = false,
  type = 'text',
  required = false
}) => {
  const [touched, setTouched] = useState(false);
  const [validation, setValidation] = useState({ isValid: true, error: null });

  useEffect(() => {
    // Validate on value change (real-time)
    if (touched || value !== '') {
      const result = validateField(tableName, name, value);
      setValidation(result);
    }
  }, [value, tableName, name, touched]);

  const handleBlur = () => {
    setTouched(true);
  };

  const handleChange = (e) => {
    const newValue = e.target.value;
    onChange({ ...e, target: { ...e.target, value: newValue } });
  };

  const placeholder = getFieldPlaceholder(tableName, name);
  const label = getFieldLabel(name);

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        disabled={disabled}
        placeholder={placeholder}
        className={`input w-full ${
          touched && !validation.isValid
            ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
            : touched && validation.isValid && value !== ''
            ? 'border-green-500 focus:border-green-500 focus:ring-green-500'
            : ''
        }`}
      />
      
      {/* Real-time validation feedback */}
      {touched && (
        <div className="mt-1 text-xs">
          {validation.isValid && value !== '' ? (
            <p className="text-green-600 flex items-center gap-1">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Правільна
            </p>
          ) : validation.error ? (
            <p className="text-red-600 flex items-center gap-1">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {validation.error}
            </p>
          ) : null}
        </div>
      )}
    </div>
  );
};

export default ValidatedInput;
