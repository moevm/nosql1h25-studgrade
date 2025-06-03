import { Outlet, NavLink } from "react-router-dom";
import styles from "./PageLayout.module.css";
import ProfileIcon from "../../public/profile.svg?react";
import StatsIcon from "../../public/stats.svg?react";

const PageLayout = () => {
  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div className={styles.name}>ФИО</div>
      </header>
      <div className={styles.container}>
        <aside className={styles.aside_menu}>
          <NavLink to={"/users/create"} end className={styles.aside_menu__link}>
            Создать пользователя
          </NavLink>
          <NavLink to={"/teachers/create"} end className={styles.aside_menu__link}>
            Создать преподавателя 
          </NavLink>
          <NavLink to={"/users/"} end className={styles.aside_menu__link}>
            <StatsIcon /> Пользователи
          </NavLink>
          <NavLink to={"/teachers/"} end   className={styles.aside_menu__link}>
            <StatsIcon /> Преподаватели
          </NavLink>
        </aside>
        <div className={styles.main}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default PageLayout;
