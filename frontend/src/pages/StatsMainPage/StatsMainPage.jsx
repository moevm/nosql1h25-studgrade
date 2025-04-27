import styles from "./StatsMainPage.module.css";
import DownloadIcon from "../../public/download.svg?react";
import UploadIcon from "../../public/upload.svg?react";
import ArrowBackIcon from "../../public/arrow_back.svg?react";
import ArrowForwardIcon from "../../public/arrow_forward.svg?react";

const StatsMainPage = () => {
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
      <div className={styles.common_info}>
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
      </div>
      <div className={styles.filters}>
        <div className={styles.filter__title}>Фильтры</div>
        <fieldset className={styles.filter_group}>
          <legend className={styles.filter_group__title}>ФАКУЛЬТЕТ</legend>
          <label className={styles.filter_checkbox}>
            <input type="checkbox" />
            <div>ФКТИ</div>
          </label>
          <label className={styles.filter_checkbox}>
            <input type="checkbox" />
            <div>ФКТИ</div>
          </label>
          <label className={styles.filter_checkbox}>
            <input type="checkbox" />
            <div>ФКТИ</div>
          </label>
        </fieldset>
        <fieldset className={styles.filter_group}>
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
        </fieldset>
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
              <th>Посещаемость</th>
              <th>Средний балл</th>
            </tr>
          </thead>
          <tbody className={styles.info_table__body}>
            <tr className={styles.info_table__row}>
              <td className={styles.info_table__cell}>Иванов И.И.</td>
              <td className={styles.info_table__cell}>ФКТИ</td>
              <td className={styles.info_table__cell}>2381</td>
              <td className={styles.info_table__cell}>Бакалавр</td>
              <td className={styles.info_table__cell}>80%</td>
              <td className={styles.info_table__cell}>4.5</td>
            </tr>
            <tr className={styles.info_table__row}>
              <td className={styles.info_table__cell}>Иванов И.И.</td>
              <td className={styles.info_table__cell}>ФКТИ</td>
              <td className={styles.info_table__cell}>2381</td>
              <td className={styles.info_table__cell}>Бакалавр</td>
              <td className={styles.info_table__cell}>80%</td>
              <td className={styles.info_table__cell}>4.5</td>
            </tr>
            <tr className={styles.info_table__row}>
              <td className={styles.info_table__cell}>Иванов И.И.</td>
              <td className={styles.info_table__cell}>ФКТИ</td>
              <td className={styles.info_table__cell}>2381</td>
              <td className={styles.info_table__cell}>Бакалавр</td>
              <td className={styles.info_table__cell}>80%</td>
              <td className={styles.info_table__cell}>4.5</td>
            </tr>
            <tr className={styles.info_table__row}>
              <td className={styles.info_table__cell}>Иванов И.И.</td>
              <td className={styles.info_table__cell}>ФКТИ</td>
              <td className={styles.info_table__cell}>2381</td>
              <td className={styles.info_table__cell}>Бакалавр</td>
              <td className={styles.info_table__cell}>80%</td>
              <td className={styles.info_table__cell}>4.5</td>
            </tr>
            {/* Add more rows as needed */}
          </tbody>
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
