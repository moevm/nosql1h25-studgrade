import styles from "./ProfilePage.module.css";
import EditIcon from "../../public/edit_button.svg?react";
import MailIcon from "../../public/mail.svg?react";
import CallIcon from "../../public/call.svg?react";
import MoreIcon from "../../public/more.svg?react";
import { useStudentById, useUpdateStudentById } from "../../hooks/useStudents";
import { useEffect, useState } from "react";
import getFullName from "../../utils/getFullName";

const ProfilePage = () => {
  const {
    student: user,
    loading,
    error,
  } = useStudentById("6814fdae2fc966af516ab827");

  const {
    update,
    loading: updateLoading,
    error: updateError,
  } = useUpdateStudentById();

  const [userData, setUserData] = useState({});

  useEffect(() => {
    if (user) {
      setUserData(user);
    }
  }, [user]);

  const [isEditMode, setIsEditMode] = useState(false);

  const handleEditClick = () => {
    setIsEditMode((prev) => !prev);
  };

  const handleSaveClick = () => {
    console.log("userData", userData);
    update(userData._id, userData);
  };

  if (loading || updateLoading)
    return <div className={styles.main_block}>Loading...</div>;
  if (error || updateError)
    return (
      <div className={styles.main_block}>
        Error: {error?.message || updateError?.message}
      </div>
    );
  if (!user)
    return <div className={styles.main_block}>Пользователь не найден</div>;
  return (
    <div className={styles.main_block}>
      <div className={styles.main_head}>
        <div className={styles.main_header}>Профиль</div>
        <button className={styles.edit_button} onClick={handleEditClick}>
          <EditIcon />
        </button>
        {isEditMode && (
          <button className={styles.edit_button} onClick={handleSaveClick}>
            Сохранить
          </button>
        )}
      </div>
      <div className={styles.main_columns_container}>
        <div className={styles.fields_colomns_container}>
          <div className={styles.fields_colomn}>
            <div className={styles.fields_row}>
              <label className={styles.field}>
                <div className={styles.filed_name}>Фамилия</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="text"
                  value={isEditMode ? userData.lastName : user.lastName}
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      lastName: e.target.value,
                    }))
                  }
                />
              </label>
            </div>
            <div className={styles.fields_row}>
              <label className={styles.field}>
                <div className={styles.filed_name}>Имя</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="text"
                  value={isEditMode ? userData.firstName : user.firstName}
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      firstName: e.target.value,
                    }))
                  }
                />
              </label>
            </div>
            <div className={styles.fields_row}>
              <label className={styles.field}>
                <div className={styles.filed_name}>Отчество</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="text"
                  value={isEditMode ? userData.middleName : user.middleName}
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      middleName: e.target.value,
                    }))
                  }
                />
              </label>
            </div>

            <div className={styles.fields_row}>
              <label className={styles.field}>
                <div className={styles.filed_name}>Дата рождения</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="date"
                  value={
                    new Date(isEditMode ? userData.birthDate : user.birthDate)
                      .toISOString()
                      .split("T")[0]
                  }
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      birthDate: e.target.value,
                    }))
                  }
                />
              </label>
              <label className={styles.field}>
                <div className={styles.filed_name}>Год поступления</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="number"
                  value={
                    isEditMode ? userData.admissionYear : user.admissionYear
                  }
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      admissionYear: e.target.value,
                    }))
                  }
                />
              </label>
            </div>
          </div>

          <div className={styles.fields_colomn}>
            <div className={styles.fields_row}>
              <label className={styles.field}>
                <div className={styles.filed_name}>Уровень образования</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="text"
                  value={isEditMode ? userData.studentType : user.studentType}
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      studentType: e.target.value,
                    }))
                  }
                />
              </label>
            </div>

            <div className={styles.fields_row}>
              <label className={styles.field}>
                <div className={styles.filed_name}>Факультет</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="text"
                  value={isEditMode ? userData.faculty : user.faculty}
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      faculty: e.target.value,
                    }))
                  }
                />
              </label>
            </div>
            <div className={styles.fields_row}>
              <label className={styles.field}>
                <div className={styles.filed_name}>Направление</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="string"
                  value={isEditMode ? userData.programName : user.programName}
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      programName: e.target.value,
                    }))
                  }
                />
              </label>
            </div>

            <div className={styles.fields_row}>
              <label className={styles.field}>
                <div className={styles.filed_name}>Курс</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="number"
                  id="course"
                  value={isEditMode ? userData.course : user.course}
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      course: e.target.value,
                    }))
                  }
                />
              </label>
              <label className={styles.field}>
                <div className={styles.filed_name}>Группа</div>
                <input
                  readOnly={!isEditMode}
                  className={styles.filed_input}
                  type="number"
                  id="group"
                  value={isEditMode ? userData.groupName : user.groupName}
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      groupName: e.target.value,
                    }))
                  }
                />
              </label>
            </div>
          </div>
        </div>

        <div>
          <div className={styles.avatar_block}>
            <div className={styles.avatar_description}>
              <div className={styles.avatar_fullname}>{getFullName(user)}</div>
              <div className={styles.avatar_group}>
                ГРУППА {isEditMode ? userData.groupName : user.groupName}
              </div>
            </div>
            {/* <div className={styles.avatar_action_buttons}>
              <div className={styles.avatar_action_button}>
                <CallIcon />
              </div>
              <div className={styles.avatar_action_button}>
                <MailIcon />
              </div>
              <div className={styles.avatar_action_button}>
                <MoreIcon />
              </div>
            </div> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
