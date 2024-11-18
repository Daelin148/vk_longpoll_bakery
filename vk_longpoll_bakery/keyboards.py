from abc import ABC, abstractmethod

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class BaseKeyboard(ABC):
    """Базовый класс клавиатуры."""

    def __init__(self):
        self.keyboard = VkKeyboard(one_time=False)

    @abstractmethod
    def get_keyboard(self) -> VkKeyboard:
        pass

    def add_main_menu_button(self):
        """Метод для добавления кнопки главного меню."""

        self.keyboard.add_button(
            'Главное меню', color=VkKeyboardColor.POSITIVE
        )
        return self.keyboard


class StartKeyboard(BaseKeyboard):

    def get_keyboard(self):
        self.keyboard.add_button('Начать', color=VkKeyboardColor.POSITIVE)
        return self.keyboard


class CategoryKeyboard(BaseKeyboard):

    def get_keyboard(self, commands: list[str]):
        [self.keyboard.add_button(button.capitalize()) for button in commands]
        return self.keyboard


class ProductsKeyboard(BaseKeyboard):

    def get_keyboard(self, commands: list[str]):
        [(self.keyboard.add_button(product),
          self.keyboard.add_line()) for product in commands]
        return self.add_main_menu_button()


class ProductDetailKeyboard(BaseKeyboard):

    def get_keyboard(self):
        return self.add_main_menu_button()
