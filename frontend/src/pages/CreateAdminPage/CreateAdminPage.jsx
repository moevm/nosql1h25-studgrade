import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateUser } from '../../hooks/useUsers';
import styles from './CreateAdminPage.module.css';

const CreateAdminPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    middleName: '',
    email: '',
    password: '',
    role: "admin"
  });
  
  const [error, setError] = useState(null);
  const { create, loading: createLoading } = useCreateUser();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await create(formData);
      navigate('/users');
    } catch (err) {
      if (err.message.includes('Network Error') || err.message.includes('Failed to fetch')) {
        setError('Ошибка соединения с сервером. Проверьте CORS настройки бэкенда.');
      } else {
        setError(err.response?.data?.detail || err.message || 'Ошибка при создании пользователя');
      }
    }
  };

  return (
    <div className={styles.container}>
      <h1>Создание нового пользователя</h1>
      
      {error && <div className={styles.error}>{error}</div>}
      
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label>Имя</label>
          <input
            type="text"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
            minLength={2}
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Фамилия</label>
          <input
            type="text"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
            minLength={2}
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Отчество</label>
          <input
            type="text"
            name="middleName"
            value={formData.middleName}
            onChange={handleChange}
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Пароль</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength={6}
          />
        </div>
        
        <button 
          type="submit" 
          disabled={createLoading}
          className={styles.submitButton}
        >
          {createLoading ? 'Создание...' : 'Создать пользователя'}
        </button>
      </form>
    </div>
  );
};

export default CreateAdminPage;