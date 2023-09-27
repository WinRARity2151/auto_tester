from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_tester.pages.base_page import BasePage
import requests
import os


class SBISPage(BasePage):
    partners: None | WebElement = None

    def __init__(self):
        self.driver.get("https://sbis.ru/")

    @BasePage.logger('Открываем раздел "Контакты"')
    def open_contacts(self) -> None:
        contacts_button = self.driver.find_element(By.XPATH, '//a[@href="/contacts"]')
        contacts_button.click()

    @BasePage.logger("Находим баннер и кликаем по нему")
    def open_banner(self) -> None:
        banner_button = self.driver.find_element(By.XPATH, "//a[@title='tensor.ru']")
        banner_button.click()

    @BasePage.logger("Переходим на https://tensor.ru/")
    def open_tenz(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[-1])

    @BasePage.logger("Проверяем регион")
    def region_check(self, c_region: str) -> None:
        wait = WebDriverWait(self.driver, 10)
        region = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
            )
        )
        wait.until(lambda driver: c_region in region.text)
        assert c_region in region.text, "Регион не найден"

    @BasePage.logger("Проверяем партнеров")
    def partners_check(self) -> None:
        self.partners = self.driver.find_element(
            By.XPATH, "//div[@name='itemsContainer']"
        )
        assert self.partners.is_displayed(), "Партнеры не найдены"

    @BasePage.logger("Меняем регион на Камчатский край")
    def change_region(self) -> None:
        region = self.driver.find_element(
            By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']"
        )
        region.click()
        wait = WebDriverWait(self.driver, 10)
        n_region = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[@title="Камчатский край"]')
            )
        )
        n_region.click()

    @BasePage.logger("Проверяем новых партнеров")
    def change_check(self) -> None:
        new_partners = self.driver.find_element(
            By.XPATH, "//div[@name='itemsContainer']"
        )
        assert not (new_partners is self.partners), "Партнеры не обновились"

    @BasePage.logger("Проверяем url и title")
    def url_title_check(self) -> None:
        assert (
            "kamchatskij" in self.driver.current_url
            and "Камчатский" in self.driver.title
        ), "Ошибка в url и title"

    @BasePage.logger('Переходим в "Скачать СБИС"')
    def footer_find(self) -> None:
        footer = self.driver.find_element(By.XPATH, "//*[text()='Скачать СБИС']")
        footer.send_keys(Keys.PAGE_DOWN)
        footer.click()

    @BasePage.logger('Переходим в "Плагин"')
    def download_link(self) -> None:
        wait = WebDriverWait(self.driver, 10)
        plugin = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-id='plugin']"))
        )
        plugin.click()

    @BasePage.logger("Скачиваем  веб-установщик")
    def download_plugin(self) -> None:
        wait = WebDriverWait(self.driver, 10)
        download = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[text()='Скачать (Exe 3.64 МБ) ']")
            )
        )
        file_name = "plugin.exe"
        response = requests.get(download.get_attribute("href"))
        assert response.status_code == 200, "Файл не скачан"
        with open(file_name, "wb") as f:
            f.write(response.content)

    @BasePage.logger("Проверяем размер файла")
    def check_file(self) -> None:
        assert os.path.getsize("plugin.exe") == 3815296, "Файл поврежден"
