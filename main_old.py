from enum import Enum
from typing import Optional

import uvicorn
from fastapi import FastAPI, Path, Query

# Создание объекта приложения.
app = FastAPI()


class EducationLevel(str, Enum):
    # Укажем значения с большой буквы, чтобы они хорошо смотрелись
    # в документации Swagger.
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


# Декоратор, определяющий, что GET-запросы к основному URL приложения
# должны обрабатываться этой функцией.
@app.get('/', tags=['common methods'])
def read_root() -> dict[str, str]:
    return {'Hello': 'FastAPI'}


@app.get(
    '/me',
    tags=['special methods'],
    summary='Приветствие автора',
    description='Приветствие автора без дополнительных аргументов'
)
def hello_author() -> dict[str, str]:
    return {'Hello': 'author'}


@app.get(
    '/{name}',
    tags=['common methods'],
    summary='Общее приветствие',
    response_description='Полная строка приветствия'
)
def greetings(
    *,
    # У параметров запроса name и surname значений по умолчанию нет,
    # поэтому в первый параметр ставим многоточие, Ellipsis.
    name: str = Path(
        ..., min_length=2, max_length=20,
        title='Полное имя', description='Можно вводить в любом регистре'
    ),
    # gt означает "больше чем", le — "меньше чем или равно".
    age: Optional[int] = Query(None, gt=4, le=99),
    # Добавляем псевдоним alias.
    is_staff: bool = Query(False, alias='is-staff', include_in_schema=False),
    education_level: Optional[EducationLevel] = None,
    # Теперь при использовании *, при необходимости,
    # можно перенести аргумент surname в конец для отображения в документации.
    surname: list[str] = Query(..., min_length=2, max_length=50),
) -> dict[str, str]:
    """
    Приветствие пользователя:

    - **name**: имя
    - **surname**: фамилия или несколько фамилий
    - **age**: возраст (опционально)
    - **education_level**: уровень образования (опционально)
    """
    surnames = ' '.join(surname)
    result = ' '.join([name, surnames])
    result = result.title()
    if age is not None:
        # Обязательно приводим age к строке.
        result += ', ' + str(age)
    if education_level is not None:
        # Чтобы текст смотрелся грамотно,
        # переведём строку education_level в нижний регистр.
        result += ', ' + education_level.lower()
    if is_staff:
        result += ', сотрудник'
    return {'Hello': result}


@app.get('/math-sum')
def get_math_sum(
    add: list[float] = Query(
        None, gt=0, lt=9.99,
        title='Полное имя', description='Можно вводить в любом регистре'
    )
) -> float:
    return sum(add)


if __name__ == '__main__':
    # Команда на запуск uvicorn.
    # Здесь же можно указать хост и/или порт при необходимости,
    # а также другие параметры.
    uvicorn.run('main:app', reload=True)
