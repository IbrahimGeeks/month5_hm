from datetime import date
from rest_framework.exceptions import ValidationError

def validate_user_age(birthdate_value):

    if not birthdate_value:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")

    if isinstance(birthdate_value, str):
        try:
            birthdate = date.fromisoformat(birthdate_value)
        except ValueError:
            raise ValidationError("Некорректный формат даты рождения.")
    else:
        birthdate = birthdate_value

    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")