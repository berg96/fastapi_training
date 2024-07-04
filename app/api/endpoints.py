from fastapi import Body, APIRouter

from app.schemas.schemas import Person

# Создаём объект роутера.
router = APIRouter()


# Меняем метод GET на POST, указываем статичный адрес.
# В декораторе подставляем объект роутера вместо app.
@router.post('/hello')
# Вместо множества параметра теперь будет только один - person,
# в качестве аннотации указываем класс Person.
def greetings(
    person: Person = Body(
        ..., examples=Person.Config.schema_extra['examples']
    )
) -> dict[str, str]:
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
