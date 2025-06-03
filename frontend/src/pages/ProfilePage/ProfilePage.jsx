import styles from "./ProfilePage.module.css";
import EditIcon from "../../public/edit_button.svg?react";
import MailIcon from "../../public/mail.svg?react";
import CallIcon from "../../public/call.svg?react";
import MoreIcon from "../../public/more.svg?react";
import { useStudentById, useUpdateStudentById } from "../../hooks/useStudents";
import { useEffect, useState } from "react";
import getFullName from "../../utils/getFullName";
import { useParams } from "react-router-dom";
import { useUpdateUserById, useUserById } from "../../hooks/useUsers";
import { useTeacherById, useUpdateTeacherById } from "../../hooks/useTeachers";

const useUserMap = {
  student: useStudentById,
  user: useUserById,
  teacher: useTeacherById,
};

const useUpdateMap = {
  student: useUpdateStudentById,
  user: useUpdateUserById,
  teacher: useUpdateTeacherById,
};

const fields = {
  firstName: {
    title: "Имя",
    type: "text",
  },
  lastName: {
    title: "Фамилия",
    type: "text",
  },
  role: {
    title: "Роль",
    type: "text",
  },
  middleName: {
    title: "Отчество",
    type: "text",
  },
  email: {
    title: "Почта",
    type: "email",
  },
};
const Field = ({ title, isEditMode, type, value, onChange, name }) => (
  <label className={styles.field}>
    <div className={styles.filed_name}>{title || name}</div>
    <input
      name={name}
      readOnly={!isEditMode}
      className={styles.filed_input}
      type={type}
      value={value}
      onChange={onChange}
    />
  </label>
);

const ProfilePage = ({ role }) => {
  const useUser = useUserMap[role];
  const useUpdateUser = useUpdateMap[role];

  const { userId } = useParams();
  const { data: user, loading, error } = useUser(userId);

  const {
    update,
    loading: updateLoading,
    error: updateError,
  } = useUpdateUser();

  console.log(updateError)

  const [userData, setUserData] = useState({});

  useEffect(() => {
    if (user) {
      setUserData({ ...user, id: undefined });
    }
  }, [user]);

  const [isEditMode, setIsEditMode] = useState(false);

  const handleEditClick = () => {
    setIsEditMode((prev) => !prev);
  };

  const handleSaveClick = () => {
    console.log("userData", userData);
    update(userId, userData);
  };

  if (loading || updateLoading)
    return <div className={styles.main_block}>Loading...</div>;

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
        {(error || updateError) && (
          <span>Error: {error?.message || updateError?.response?.data?.detail?.[0]?.msg}</span>
        )}
      </div>
      <div className={styles.main_columns_container}>
        <div className={styles.fields_colomns_container}>
          {!loading &&
            user &&
            Object.keys(user).map(
              (key) =>
                key !== "id" && (
                  <Field
                    key={key}
                    title={fields[key]?.title}
                    name={key}
                    isEditMode={isEditMode}
                    type={fields[key]?.type}
                    value={isEditMode ? userData[key] : user[key]}
                    onChange={(e) =>
                      setUserData((prev) => ({
                        ...prev,
                        [key]: e.target.value,
                      }))
                    }
                  />
                )
            )}
        </div>

        <div>
          <div className={styles.avatar_block}>
            <div className={styles.avatar_description}>
              <div className={styles.avatar_fullname}>{getFullName(user)}</div>
              {user?.groupName && (
                <div className={styles.avatar_group}>
                  ГРУППА {isEditMode ? userData.groupName : user.groupName}
                </div>
              )}
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
