import { useMemo, useState } from "react";
import { Link } from "react-router-dom"
import styles from "./TeacherPage.module.css";
import DownloadIcon from "../../public/download.svg?react";
import UploadIcon from "../../public/upload.svg?react";
import ArrowBackIcon from "../../public/arrow_back.svg?react";
import ArrowForwardIcon from "../../public/arrow_forward.svg?react";
import { useTeachers } from "../../hooks/useTeachers";

import { useDebounce } from "../../hooks/useDebounce";
import getFullName from "../../utils/getFullName";

const ROLES = ["student", "teacher", "admin"];
const GROUPS = ["2381", "2382", "2383"];
const SUBJECTS = ["Math", "English", "C++"];

const TeacherPage = () => {
  const [selectedRoles, setSelectedRoles] = useState([]);
  const [selectedSubjects, setSelectedSubjects] = useState([]);
  const [selectedGroups, setSelectedGroups] = useState([]);
  const [userData, setUserData] = useState({
    firstName: "",
    lastName: "",
    middleName: "",
    email: "",
  });
  const debouncedUserData = useDebounce(userData, 500);
  const teachersParams = useMemo(() => {
    return {
      firstName: debouncedUserData.firstName || undefined,
      lastName: debouncedUserData.lastName || undefined,
      middleName: debouncedUserData.middleName || undefined,
      email: debouncedUserData.email || undefined,
      role: selectedRoles.length > 0 ? selectedRoles : undefined,
      assignedGroups: selectedGroups.length > 0 ? selectedGroups : undefined,
      assignedSubjects:
        selectedSubjects.length > 0 ? selectedSubjects : undefined,
    };
  }, [selectedRoles, selectedGroups, selectedSubjects, debouncedUserData]);
  const { teachers, loading, error } = useTeachers(teachersParams);
  console.log(teachersParams, teachers);

  const toggleRole = (role) => {
    setSelectedRoles((prev) =>
      prev.includes(role) ? prev.filter((f) => f !== role) : [...prev, role]
    );
  };
  const toggleGroup = (assignedGroups) => {
    setSelectedGroups((prev) =>
      prev.includes(assignedGroups)
        ? prev.filter((f) => f !== assignedGroups)
        : [...prev, assignedGroups]
    );
  };
  const toggleSubject = (assignedSubjects) => {
    setSelectedSubjects((prev) =>
      prev.includes(assignedSubjects)
        ? prev.filter((f) => f !== assignedSubjects)
        : [...prev, assignedSubjects]
    );
  };
  return (
    <div className={styles.main}>
      <div className={styles.generals_buttons}>
        <button
          className={styles.generals_buttons__button}
          onClick={() => {
            // NOT IMPLEMENTED
            alert("Export to Excel is not implemented yet.");
            console.log("Export to Excel clicked");
          }}
        >
          <DownloadIcon /> Export to Excel
        </button>
        <button
          className={styles.generals_buttons__button}
          onClick={() => {
            // NOT IMPLEMENTED
            alert("Import from Excel is not implemented yet.");
            console.log("Import from Excel clicked");
          }}
        >
          <UploadIcon /> Load data
        </button>
      </div>
      {/* <div className={styles.common_info}>
        <div className={styles.common_info__title}>Общая информация</div>
        <div className={styles.common_info__table}>
          <div className={styles.common_info__item}>
            <div className={styles.common_info__item__title}>Количество</div>
            <div className={styles.common_info__item__value}>399</div>
          </div>
          <div className={styles.common_info__item}>
            <div className={styles.common_info__item__title}>Посещаемость</div>
            <div className={styles.common_info__item__value}>69%</div>
          </div>
          <div className={styles.common_info__item}>
            <div className={styles.common_info__item__title}>Средний балл</div>
            <div className={styles.common_info__item__value}>4.5</div>
          </div>
          <div className={styles.common_info__item}>
            <div className={styles.common_info__item__title}>Магистры</div>
            <div className={styles.common_info__item__value}>12</div>
          </div>
          <div className={styles.common_info__item}>
            <div className={styles.common_info__item__title}>Бакалавры</div>
            <div className={styles.common_info__item__value}>111</div>
          </div>
          <div className={styles.common_info__item}>
            <div className={styles.common_info__item__title}>Аспиранты</div>
            <div className={styles.common_info__item__value}>5</div>
          </div>
        </div>
      </div> */}
      <div className={styles.filters}>
        <div className={styles.filter__title}>Фильтры</div>
        <fieldset className={styles.filter_group}>
          <label className={styles.field}>
            <div className={styles.filed_name}>Фамилия</div>
            <input
              className={styles.filed_input}
              type="text"
              value={userData.lastName}
              onChange={(e) => {
                setUserData((prev) => ({ ...prev, lastName: e.target.value }));
              }}
            />
          </label>
          <label className={styles.field}>
            <div className={styles.filed_name}>Имя</div>
            <input
              className={styles.filed_input}
              type="text"
              value={userData.firstName}
              onChange={(e) => {
                setUserData((prev) => ({ ...prev, firstName: e.target.value }));
              }}
            />
          </label>
          <label className={styles.field}>
            <div className={styles.filed_name}>Отчество</div>
            <input
              className={styles.filed_input}
              type="text"
              value={userData.middleName}
              onChange={(e) => {
                setUserData((prev) => ({
                  ...prev,
                  middleName: e.target.value,
                }));
              }}
            />
          </label>
          <label className={styles.field}>
            <div className={styles.filed_name}>Почта</div>
            <input
              className={styles.filed_input}
              type="text"
              value={userData.email}
              onChange={(e) => {
                setUserData((prev) => ({
                  ...prev,
                  email: e.target.value,
                }));
              }}
            />
          </label>
        </fieldset>
        <fieldset className={styles.filter_group}>
          <legend className={styles.filter_group__title}>ГРУППЫ</legend>
          {GROUPS.map((assignedGroups) => (
            <label key={assignedGroups} className={styles.filter_checkbox}>
              <input
                type="checkbox"
                onChange={() => toggleGroup(assignedGroups)}
                name={assignedGroups}
                checked={selectedGroups.includes(assignedGroups)}
              />
              <div>{assignedGroups}</div>
            </label>
          ))}
        </fieldset>
        
        {/* <fieldset className={styles.filter_group}>
          <legend className={styles.filter_group__title}>Балл</legend>
          <div className={styles.filter_range}>
            <label className={styles.filter_number}>
              <div>От</div>
              <input type="number" />
            </label>
            <label className={styles.filter_number}>
              <div>До</div>
              <input type="number" />
            </label>
          </div>
        </fieldset> */}
        <div className={styles.filter__buttons}>
          <button className={styles.filter_button}>Применить</button>
        </div>
      </div>
      <div className={styles.info}>
        <div className={styles.info__title}>Найдено: 399</div>
        <table className={styles.info_table}>
          <col className={styles.first_column} />
          <thead className={styles.info_table__header}>
            <tr>
              <th>ФИО</th>
              <th>Электронная почта</th>
              <th>Роль</th>
              <th>Группы</th>
              <th>Предметы</th>
              {/* <th>Посещаемость</th>
              <th>Средний балл</th> */}
            </tr>
          </thead>
          {loading && (
            <tbody className={styles.info_table__body}>
              <tr>
                <td colSpan="6" className={styles.info_table__loading}>
                  Загрузка...
                </td>
              </tr>
            </tbody>
          )}
          {error && (
            <tbody className={styles.info_table__body}>
              <tr>
                <td colSpan="6" className={styles.info_table__loading}>
                  Ошибка загрузки данных. {error.message}
                </td>
              </tr>
            </tbody>
          )}
          {!loading && !error && teachers.length === 0 && (
            <tbody className={styles.info_table__body}>
              <tr>
                <td colSpan="6" className={styles.info_table__loading}>
                  Нет данных
                </td>
              </tr>
            </tbody>
          )}
          {!loading && teachers.length > 0 && (
            <tbody className={styles.info_table__body}>
              {teachers.map((teacher) => (
                <tr key={teacher.id} className={styles.info_table__row}>
                  <Link to={`/users/${teacher.id}/`}>
                    <td>{getFullName(teacher)}</td>
                  </Link>
                    <td>{teacher.email}</td>
                    <td>{teacher.role}</td>
                    <td>{teacher.assignedGroups}</td>
                    <td>{teacher.assignedSubjects}</td>
                </tr>
              ))}
            </tbody>
          )}
        </table>
        <div className={styles.info_paginator}>
          <div className={styles.info_paginator__button}>
            <ArrowBackIcon />
            <div>Назад</div>
          </div>
          <div className={styles.info_paginator__button}>
            <div>Следующая страница</div>
            <ArrowForwardIcon />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeacherPage;
