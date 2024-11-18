import redis
from keyboards import (CategoryKeyboard, ProductDetailKeyboard,
                       ProductsKeyboard, StartKeyboard)
from models import Category, Product
from sqlalchemy.orm import Session


class BaseState:
    """Базовый класс состояний."""

    STATE_KEYBOARD = None
    STATE_COMMANDS = None
    NEXT_STATE = None
    PREVIOUS_STATE = None
    STATE_MESSAGE = None

    def __init__(self, db_session: Session):
        self.db_session = db_session

    @classmethod
    def get_commands(cls, msg: str, session: Session):
        return cls.STATE_COMMANDS

    @classmethod
    def get_keyboard(cls, msg: str, session: Session):
        return cls.STATE_KEYBOARD().get_keyboard()

    @classmethod
    def get_message(cls, msg: str, session: Session):
        return cls.STATE_MESSAGE


class StartState(BaseState):
    """Начальное состояние."""

    STATE_KEYBOARD = StartKeyboard
    STATE_COMMANDS = ('начать',)
    NEXT_STATE = 'EnterMenuState'
    PREVIOUS_STATE = None
    STATE_MESSAGE = 'Пожалуйста, нажмите кнопку Начать.'


class EnterMenuState(BaseState):
    """Состояние выбора категорий."""

    STATE_KEYBOARD = CategoryKeyboard
    STATE_COMMANDS = None
    NEXT_STATE = 'EnterCategoryState'
    PREVIOUS_STATE = 'StartState'
    STATE_MESSAGE = 'Пожалуйста, выберите интересующую вас категорию'

    @classmethod
    def get_commands(cls, msg, session):
        query = session.query(Category).all()
        return [category.title.lower() for category in query]

    @classmethod
    def get_keyboard(cls, msg, session):
        return cls.STATE_KEYBOARD().get_keyboard(
            commands=cls.get_commands(msg, session)
        )


class EnterCategoryState(BaseState):
    """Состояние выбора продуктов категории."""

    STATE_KEYBOARD = ProductsKeyboard
    STATE_COMMANDS = None
    NEXT_STATE = 'EnterProductState'
    PREVIOUS_STATE = 'EnterMenuState'
    STATE_MESSAGE = 'Пожалуйста, выберите интересующий вас товар'

    @classmethod
    def get_commands(cls, msg, session):
        category = session.query(Category).filter(
            Category.title == msg.capitalize()
        ).first()
        query = session.query(Product).filter(
            Product.category_id == category.id
        )
        return [product.title for product in query]

    @classmethod
    def get_keyboard(cls, msg, session):
        return cls.STATE_KEYBOARD().get_keyboard(
            commands=cls.get_commands(msg, session)
        )


class EnterProductState(BaseState):
    """Состояние выбора конкретного продукта."""

    STATE_KEYBOARD = ProductDetailKeyboard
    STATE_COMMANDS = None
    NEXT_STATE = None
    PREVIOUS_STATE = 'EnterCategoryState'
    STATE_MESSAGE = None

    @classmethod
    def get_message(cls, msg, session):
        obj = session.query(Product).filter(
            Product.title == msg.capitalize()
        ).first()
        title = obj.title
        descr = obj.description
        return (f'Название: {title}\n'
                f'Описание: {descr}\n')


class StateMachine:
    """Класс машины состояний."""

    def __init__(self, redis_conn: redis.Redis):
        self.redis = redis_conn
        self.user_id = None

    def get_current_state(self) -> BaseState:
        state_str = self.redis.get(self.user_id).decode()
        state = globals()[state_str]
        return state

    def set_user(self, user_id: int):
        self.user_id = str(user_id)
        self.set_state('StartState')

    def set_state(self, state: str):
        self.redis.set(self.user_id, state)

    def clear(self):
        self.set_state('EnterMenuState')
