import styles from "./ProfilePage.module.css";
import EditIcon from "../../public/edit_button.svg?react";
import MailIcon from "../../public/mail.svg?react";
import CallIcon from "../../public/call.svg?react";
import MoreIcon from "../../public/more.svg?react";

const ProfilePage = () => {
  return (
    <div className={styles.main_block}>
      <div className={styles.main_head}>
        <div className={styles.main_header}>Профиль</div>
        <div className={styles.edit_button}>
            <EditIcon/>
        </div>
      </div>
      <div className={styles.main_columns_container}>
        <div className={styles.fields_colomns_container}>
          <div className={styles.fields_colomn}>
            
            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Фамилия</div>
                <input className={styles.filed_input} type="text" id="middle_name"/>
              </div>
            </div>
            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Имя</div>
                <input className={styles.filed_input} type="text" id="name"/>
              </div>
            </div>
            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Отчество</div>
                <input className={styles.filed_input} type="text" id="last_name"/>
              </div>
            </div>
            
            
            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Дата рождения</div>
                <input className={styles.filed_input} type="date" id="birth_date"/>
              </div>
              <div className={styles.field}>
                <div className={styles.filed_name}>Год поступления</div>
                <input className={styles.filed_input} type="number" id="admission_year"/>
              </div>
            </div>
          </div>


          <div className={styles.fields_colomn}>
            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Уровень образования</div>
                <input className={styles.filed_input} type="text" id="name" value="Бакалавриат"/>
              </div>
              <div className={styles.field}>
                <div className={styles.filed_name}>Форма обучения</div>
                <input className={styles.filed_input} type="text" id="name" value="Очная"/>
              </div>            
            </div>

            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Тип финансирования</div>
                <input className={styles.filed_input} type="text" id="funding_type" value="Бюджет"/>
              </div>
            </div>

            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Факультет</div>
                <input className={styles.filed_input} type="text" id="faculty" value="Факультет компьютерных технологий и информатики"/>
              </div>
            </div>
            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Код направления</div>
                <input className={styles.filed_input} type="string" id="specialty_code" value="01.03.02"/>
              </div>
              <div className={styles.field}>
                <div className={styles.filed_name}>Направление</div>
                <input className={styles.filed_input} type="string" id="specialty" value="Прикладная математика и информатика"/>
              </div>
              
            </div>
            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Образовательная программа</div>
                <input className={styles.filed_input} type="text" id="program_name" value="Математическое обеспечение программно-информационных систем"/>
              </div>
            </div>


            
            
            <div className={styles.fields_row}>
              <div className={styles.field}>
                <div className={styles.filed_name}>Курс</div>
                <input className={styles.filed_input} type="number" id="course" value="3"/>
              </div>
              <div className={styles.field}>
                <div className={styles.filed_name}>Группа</div>
                <input className={styles.filed_input} type="number" id="group" value="2381"/>
              </div>
              <div className={styles.field}>
                <div className={styles.filed_name}>Номер студенческого билета</div>
                <input className={styles.filed_input} type="number" id="student_number" value="238108"/>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div className={styles.avatar_block}>
            <div className={styles.avatar}>*автарка*</div>
            <div className={styles.avatar_description}>
              <div className={styles.avatar_fullname}>ФИО</div>
              <div className={styles.avatar_group}>ГРУППА</div>
            </div>
            <div className={styles.avatar_action_buttons}>
                <div className={styles.avatar_action_button}>
                  <CallIcon/>
                </div>
                <div className={styles.avatar_action_button}>
                  <MailIcon/>
                </div>
                <div className={styles.avatar_action_button}>
                  <MoreIcon/>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>

/*
    <div className={styles.main_block}>
      <div className={styles.profile}>Профиль</div>
      <div className={styles.horizontal_container}>
        <div className={styles.horizontal_block}>
          <div className={styles.form_field_block}>
            <div><label for="name">ФИО</label></div>
            <input type="text" className={styles.input_field} id="name"></input>
          </div>
        </div>
        <div className={styles.horizontal_block}>блок2</div>
      </div>
    </div>
*/
  );
};

export default ProfilePage;
