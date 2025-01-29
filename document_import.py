from docxtpl import DocxTemplate
from datetime import datetime
def docx_info_add(patient_data):


    # Отримати поточну дату
    current_date = datetime.now()

    # Форматувати дату у форматі "дд.мм.рррр"
    formatted_date = current_date.strftime("%d.%m.%Y")
    doc = DocxTemplate("f025-o.docx")

    def split_date(date, type_n):
        date_digits = date.replace(".", "")  # Видаляємо крапки
        return {
            f'{type_n}1': date_digits[0],
            f'{type_n}2': date_digits[1],
            f'{type_n}3': date_digits[2],
            f'{type_n}4': date_digits[3],
            f'{type_n}5': date_digits[6],
            f'{type_n}6': date_digits[7]
        }

    def split_num(date, type_n):
        date_digits = date.replace(".", "")  # Видаляємо крапки
        return {
            f'{type_n}1': date_digits[0],
            f'{type_n}2': date_digits[1],
            f'{type_n}3': date_digits[2],
            f'{type_n}4': date_digits[3],
            f'{type_n}5': date_digits[4],
            f'{type_n}6': date_digits[5]
        }

    patient_data.update(split_date(patient_data['birth_date'], 'b'))
    patient_data.update(split_date(formatted_date, 'a'))
    patient_data.update(split_num(patient_data['certificate_number'], 'c'))
    print(patient_data)
    doc.render(patient_data)
    doc.save(f"patient_data_docx\{patient_data['name']}_{patient_data['surname']}_{patient_data['patronymic']}.docx")