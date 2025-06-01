import { useState } from 'react';
import { useUpdateUserById } from '../../hooks/useUsers';
import styles from './UpdateUserPage.module.css';
import { useParams } from 'react-router-dom';

const UpdateUserPage = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    middleName: '',
    email: '',
  });
  
  const { userId } = useParams();
  const [error, setError] = useState(null);
  const { update, loading, status } = useUpdateUserById();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await update(userId, formData);
    } catch (err) {
      if (err.message.includes('Network Error') || err.message.includes('Failed to fetch')) {
        setError('Ошибка соединения с сервером. Проверьте CORS настройки бэкенда.');
      } else {
        setError(err.message || 'Ошибка при создании пользователя');
      }
    }
  };

  return (
    <div className={styles.container}>
      <h1>Обновление пользователя</h1>
      
      {error && <div className={styles.error}>{error}</div>}

      {
        !loading && status == 'ok' && 
        <div className={styles.status}>Пользователь успешно обновлён</div>
      }
      
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
        
        <button 
          type="submit" 
          disabled={loading}
          className={styles.submitButton}
        >
          {loading ? 'Обновление...' : 'Обновить пользователя'}
        </button>
      </form>
    </div>
  );
};

export default UpdateUserPage;