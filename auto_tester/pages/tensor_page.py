from selenium.webdriver.common.by import By
from auto_tester.pages.base_page import BasePage


class TensorPage(BasePage):
    @BasePage.logger('Проверяем, что есть блок "Сила в людях"')
    def find_block(self) -> None:
        block = self.driver.find_element(By.XPATH, "//*[text()='Сила в людях']")
        assert block.is_displayed(), 'Блок "Сила в людях" не найден'

    @BasePage.logger('Переходим в "Подробнее" и проверяем https://tensor.ru/about')
    def find_about(self) -> None:
        about = self.driver.find_element(By.XPATH, '//a[@href="/about"]')
        about.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert (
            self.driver.current_url == "https://tensor.ru/about"
        ), '"Подробнее" недоступно'

    @BasePage.logger(
        "Находим раздел Работаем и проверяем, что у всех фотографий одинаковые высота и ширина"
    )
    def check_img(self) -> None:
        images = self.driver.find_elements(
            By.XPATH, '//div[@class="s-Grid-container"]//div/a/div/img'
        )
        first_image = images[0]
        first_width = first_image.get_attribute("width")
        first_height = first_image.get_attribute("height")
        assert all(
            image.get_attribute("width") == first_width
            and image.get_attribute("height") == first_height
            for image in images[1:]
        ), "Фотографии не равны"
