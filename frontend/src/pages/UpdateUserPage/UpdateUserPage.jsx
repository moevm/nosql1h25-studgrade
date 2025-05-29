import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styles from './UpdateUserPage.module.css';


const UpdateUserPage = () => {
  const { userId } = useParams();
  
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    middleName: '',
    birthDate: '',
    admissionYear: '',
    faculty: '',
    programName: '',
    course: '',
    groupName: '',
    email: '',
    password: ''
  });
  
  const [loading, setLoading] = useState(true);
  const [submitLoading, setSubmitLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/users/${userId}`);
        
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('Пользователь не найден');
          }
          throw new Error('Ошибка загрузки данных');
        }
        
        const userData = await response.json();
        
        // Преобразование snake_case в camelCase
        setFormData({
          firstName: userData.first_name || '',
          lastName: userData.last_name || '',
          middleName: userData.middle_name || '',
          birthDate: userData.birth_date ? userData.birth_date.split('T')[0] : '',
          admissionYear: userData.admission_year || '',
          faculty: userData.faculty || '',
          programName: userData.program_name || '',
          course: userData.course || '',
          groupName: userData.group_name || '',
          email: userData.email || '',
          password: '' // Пароль не загружаем
        });
        
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [userId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitLoading(true);
    setError(null);

    try {
      const requestData = {
        first_name: formData.firstName,
        last_name: formData.lastName,
        middle_name: formData.middleName,
        birth_date: formData.birthDate,
        admission_year: formData.admissionYear,
        faculty: formData.faculty,
        program_name: formData.programName,
        course: formData.course,
        group_name: formData.groupName,
        email: formData.email,
      };

      if (formData.password) {
        requestData.password = formData.password;
      }

      const response = await fetch(`http://localhost:8000/api/users/${userId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка при обновлении пользователя');
      }

      navigate(`/users/${userId}`);
    } catch (err) {
      setError(err.message || 'Произошла ошибка');
    } finally {
      setSubmitLoading(false);
    }
  };

  if (loading) {
    return <div className={styles.loading}>Загрузка данных пользователя...</div>;
  }

  return (
    <div className={styles.container}>
      <h1>Редактирование пользователя</h1>
      
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
          <label>Дата рождения</label>
          <input
            type="date"
            name="birthDate"
            value={formData.birthDate}
            onChange={handleChange}
            required
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
          <label>Новый пароль (оставьте пустым, если не хотите менять)</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Год поступления</label>
          <input
            type="number"
            name="admissionYear"
            value={formData.admissionYear}
            onChange={handleChange}
            min="2000"
            max="2030"
            required
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Факультет</label>
          <input
            type="text"
            name="faculty"
            value={formData.faculty}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Направление</label>
          <input
            type="text"
            name="programName"
            value={formData.programName}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Курс</label>
          <input
            type="number"
            name="course"
            value={formData.course}
            onChange={handleChange}
            min="1"
            max="6"
            required
          />
        </div>
        
        <div className={styles.formGroup}>
          <label>Группа</label>
          <input
            type="text"
            name="groupName"
            value={formData.groupName}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.buttonGroup}>
          <button 
            type="button" 
            onClick={() => navigate(`/users/${userId}`)}
            className={styles.cancelButton}
            disabled={submitLoading}
          >
            Отмена
          </button>
          <button 
            type="submit" 
            disabled={submitLoading}
            className={styles.submitButton}
          >
            {submitLoading ? 'Сохранение...' : 'Сохранить изменения'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UpdateUserPage;