import { useMemo, useState } from "react";
import styles from "./StatsMainPage.module.css";
import DownloadIcon from "../../public/download.svg?react";
import UploadIcon from "../../public/upload.svg?react";
import ArrowBackIcon from "../../public/arrow_back.svg?react";
import ArrowForwardIcon from "../../public/arrow_forward.svg?react";
import { useStudents } from "../../hooks/useStudents";
import { useDebounce } from "../../hooks/useDebounce";
import getFullName from "../../utils/getFullName";

const FACULTIES = ["Math", "Physics", "IT"];
const GROUP_NAMES = ["2323", "1421", "3501"];
const STUDENT_TYPES = ["bachelor", "master", "aspirant", "specialist"];

const StatsMainPage = () => {
  const [selectedFaculties, setSelectedFaculties] = useState([]);
  const [selectedGroupNames, setSelectedGroupNames] = useState([]);
  const [userData, setUserData] = useState({
    firstName: "",
    lastName: "",
    middleName: "",
  });
  const debouncedUserData = useDebounce(userData, 500);
  const [selectedStudentTypes, setSelectedStudentTypes] = useState([]);
  const studentsParams = useMemo(() => {
    return {
      faculty: selectedFaculties.length > 0 ? selectedFaculties : undefined,
      group_name:
        selectedGroupNames.length > 0 ? selectedGroupNames : undefined,
      first_name: debouncedUserData.firstName || undefined,
      last_name: debouncedUserData.lastName || undefined,
      middle_name: debouncedUserData.middleName || undefined,
      student_type:
        selectedStudentTypes.length > 0 ? selectedStudentTypes : undefined,
    };
  }, [
    selectedFaculties,
    selectedGroupNames,
    debouncedUserData,
    selectedStudentTypes,
  ]);
  const { students, loading } = useStudents(studentsParams);
  console.log(studentsParams, students);

  const toggleFaculty = (faculty) => {
    setSelectedFaculties((prev) =>
      prev.includes(faculty)
        ? prev.filter((f) => f !== faculty)
        : [...prev, faculty]
    );
  };

  const toggleGroupName = (groupName) => {
    setSelectedGroupNames((prev) =>
      prev.includes(groupName)
        ? prev.filter((g) => g !== groupName)
        : [...prev, groupName]
    );
  };

  const toggleStudentType = (studentType) => {
    setSelectedStudentTypes((prev) =>
      prev.includes(studentType)
        ? prev.filter((s) => s !== studentType)
        : [...prev, studentType]
    );
  };

  return (
    <div className={styles.main}>
      <div className={styles.generals_buttons}>
        <button className={styles.generals_buttons__button}>
          <DownloadIcon /> Export to Excel
        </button>
        <button className={styles.generals_buttons__button}>
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
        </fieldset>
        <fieldset className={styles.filter_group}>
          <legend className={styles.filter_group__title}>ФАКУЛЬТЕТ</legend>
          {FACULTIES.map((faculty) => (
            <label key={faculty} className={styles.filter_checkbox}>
              <input
                type="checkbox"
                onChange={() => toggleFaculty(faculty)}
                name={faculty}
                checked={selectedFaculties.includes(faculty)}
              />
              <div>{faculty}</div>
            </label>
          ))}
        </fieldset>
        <fieldset className={styles.filter_group}>
          <legend className={styles.filter_group__title}>Группа</legend>
          {GROUP_NAMES.map((groupName) => (
            <label key={groupName} className={styles.filter_checkbox}>
              <input
                type="checkbox"
                onChange={() => toggleGroupName(groupName)}
                name={groupName}
                checked={selectedGroupNames.includes(groupName)}
              />
              <div>{groupName}</div>
            </label>
          ))}
        </fieldset>
        <fieldset className={styles.filter_group}>
          <legend className={styles.filter_group__title}>Тип студента</legend>
          {STUDENT_TYPES.map((studentType) => (
            <label key={studentType} className={styles.filter_checkbox}>
              <input
                type="checkbox"
                onChange={() => toggleStudentType(studentType)}
                name={studentType}
                checked={selectedStudentTypes.includes(studentType)}
              />
              <div>{studentType}</div>
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
              <th>Факультет</th>
              <th>Группа</th>
              <th>Степень</th>
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
          {!loading && students.length === 0 && (
            <tbody className={styles.info_table__body}>
              <tr>
                <td colSpan="6" className={styles.info_table__loading}>
                  Нет данных
                </td>
              </tr>
            </tbody>
          )}
          {!loading && students.length > 0 && (
            <tbody className={styles.info_table__body}>
              {students.map((student) => (
                <tr key={student.id} className={styles.info_table__row}>
                  <td>{getFullName(student)}</td>
                  <td>{student.faculty}</td>
                  <td>{student.groupName}</td>
                  <td>{student.studentType}</td>
                  {/* <td>{student.attendance}</td>
                  <td>{student.average_score}</td> */}
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

export default StatsMainPage;
