import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateTeacher } from '../../hooks/useTeachers';
import styles from './CreateTeacherPage.module.css';

const GROUPS = ["2381", "2382", "2383"];
const SUBJECTS = ["Math", "English", "C++"];

const CreateTeacherPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    middleName: '',
    email: '',
    password: '',
    role: "teacher",
    assignedGroups: [],
    assignedSubjects: [],
  });
  
  
  const [error, setError] = useState(null);
  const { create, loading: createLoading } = useCreateTeacher();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleGroupChange = (groupId) => {
    setFormData(prev => {
      const newGroups = prev.assignedGroups.includes(groupId)
        ? prev.assignedGroups.filter(id => id !== groupId)
        : [...prev.assignedGroups, groupId];
      
      return { ...prev, assignedGroups: newGroups };
    });
  };

  const handleSubjectChange = (subjectId) => {
    setFormData(prev => {
      const newSubjects = prev.assignedSubjects.includes(subjectId)
        ? prev.assignedSubjects.filter(id => id !== subjectId)
        : [...prev.assignedSubjects, subjectId];
      
      return { ...prev, assignedSubjects: newSubjects };
    });
  };



  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await create(formData);
      navigate('/teachers');
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
      
      {error && <div className={styles.error}>{error.message}</div>}
      
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

        <div className={styles.formGroup}>
          <label>Группы</label>
          <div className={styles.groupsContainer}>
            {GROUPS.map(groupId => (
              <label 
                key={groupId} 
                className={styles.groupCheckbox}
              >
                <input
                  type="checkbox"
                  checked={formData.assignedGroups.includes(groupId)}
                  onChange={() => handleGroupChange(groupId)}
                />
                <span>{groupId}</span>
              </label>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>ПРЕДМЕТЫ</label>
          <div className={styles.groupsContainer}>
            {SUBJECTS.map(subjectId => (
              <label 
                key={subjectId} 
                className={styles.subjectCheckbox}
              >
                <input
                  type="checkbox"
                  checked={formData.assignedSubjects.includes(subjectId)}
                  onChange={() => handleSubjectChange(subjectId)}
                />
                <span>{subjectId}</span>
              </label>
            ))}
          </div>
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

export default CreateTeacherPage;