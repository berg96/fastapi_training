from enum import Enum
from typing import Optional, Union

from fastapi import FastAPI
# Для работы с JSON в теле запроса
# импортируем из pydantic класс BaseModel
from pydantic import BaseModel

app = FastAPI()


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


# Создадим класс Person, унаследованный от BaseModel;
# в атрибутах класса перечислим ожидаемые параметры запроса.
# Аннотируем атрибуты класса.
class Person(BaseModel):
    name: str
    surname: Union[str, list[str]]
    age: Optional[int]
    is_staff: bool = False
    education_level: Optional[EducationLevel]


# Меняем метод GET на POST, указываем статичный адрес.
@app.post('/hello')
# Вместо множества параметра теперь будет только один - person,
# в качестве аннотации указываем класс Person.
def greetings(person: Person) -> dict[str, str]:
    # Обращение к атрибутам класса происходит через точку;
    # при этом будут работать проверки на уровне типов данных.
    # В IDE будут работать автодополнения.
    if isinstance(person.surname, list):
        surnames = ' '.join(person.surname)
    else:
        surnames = person.surname
    result = ' '.join([person.name, surnames])
    result = result.title()
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.education_level is not None:
        result += ', ' + person.education_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}
