import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="class")
def setup(request):
    print("Запуск chrome driver")
    driver = webdriver.Chrome("chromedriver.exe")
    driver.maximize_window()
    request.cls.driver = driver

    yield driver
    driver.close()


@pytest.mark.usefixtures("setup")
class TestLoginFormSuccess:

    def test_login_success(self):
        profile_true_name = 'Сиротюк Алексей'
        login = '137224'
        password = 'Criro1477'
        self.driver.delete_all_cookies()
        self.driver.get("https://my.selectel.ru/login/")
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".h2"), 'Вход в панель управления'))
        self.driver.find_element(By.ID, "login").click()
        self.driver.find_element(By.ID, "login").send_keys(login)
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".m-solid > .ng-scope").click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.t-wrap > .flex')))
        element_profile_name = self.driver.find_element(By.CSS_SELECTOR, '.t-wrap > .flex')
        assert profile_true_name == element_profile_name.get_attribute('title')

    def test_login_wrong(self):
        test_error_text = 'Неправильный логин или пароль'
        login = '1234'
        password = 'asdf'
        self.driver.delete_all_cookies()
        self.driver.get("https://my.selectel.ru/login/")
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".h2"), 'Вход в панель управления'))
        self.driver.find_element(By.ID, "login").click()
        self.driver.find_element(By.ID, "login").send_keys(login)
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".m-solid > .ng-scope").click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.f-danger')))
        error_text = self.driver.find_element(By.CSS_SELECTOR, '.f-danger').text
        assert test_error_text == error_text

    def test_enter_to_recovery_password(self):
        test_form_h2_text = 'Восстановление доступа'
        self.driver.delete_all_cookies()
        self.driver.get("https://my.selectel.ru/login/")
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".h2"), 'Вход в панель управления'))
        self.driver.find_element(By.LINK_TEXT, "Восстановить доступ к аккаунту").click()
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".h2"), test_form_h2_text))
        h2_text = self.driver.find_element(By.CSS_SELECTOR, '.h2').text
        assert test_form_h2_text == h2_text

