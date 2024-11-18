from models import Category, Product, Session


test_categories = [
    {"title": "Круассаны", "slug": "croissants"},
    {"title": "Торты", "slug": "cakes"},
    {"title": "Пирожные", "slug": "pies"}
]

test_products = [
    {
        "title": "Класический круассан",
        "description": "Бессмертная классика",
        "category_id": 1
    },
    {
        "title": "Круассан с миндалем",
        "description": "Шикарный вид и вкус",
        "category_id": 1
    },
    {
        "title": "Морковный торт",
        "description": "Очень вкусный торт",
        "category_id": 2
    },
    {
        "title": "Наполеон",
        "description": "Знаком всем с детства",
        "category_id": 2
    },
    {
        "title": "Пирожное картошка",
        "description": "Из всего что осталось к чаю",
        "category_id": 3
    },
    {
        "title": "Эклер",
        "description": "Не советуем на диете",
        "category_id": 3
    }
]


def load_test_data():
    """Функция для загрузки тестовых записей в БД."""

    with Session() as session:
        if session.query(Category).count() == 0:
            for category in test_categories:
                session.add(Category(
                    title=category['title'], slug=category['slug']
                ))
            session.commit()
            for product in test_products:
                session.add(Product(
                    title=product['title'],
                    description=product['description'],
                    category_id=product['category_id']
                ))
        session.commit()
