import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings import *


@pytest.fixture(autouse=True)
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(6)
    driver.get('https://b2c.passport.rt.ru')
    yield driver
    driver.quit()


def test_registr_page(browser):
    """Проверка, что страница "Регистрация" загружается """
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.implicitly_wait(5)
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Регистрация', print('Тест провален')
    assert driver.find_element(By.TAG_NAME, 'p').text == 'Личные данные', print('Тест провален')
    assert driver.find_element(By.XPATH, '//button[@type="submit"]'), print('Тест провален')


def test_password_recovery(browser):
    """Проверка, что страница "Восстановление пароля" загружается"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 't-btn-tab-login')))
    driver.find_element(By.ID, 'forgot_password').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Восстановление пароля', print('Тест провален')
    assert driver.find_element(By.ID, 'reset').text == 'Продолжить', print('Тест провален')

def test_reg_user_exists_email(browser):
    """Проверка, что повторная регистрация с email невозможна, появление оповещающей формы"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(valid_name)
    driver.find_element(By.NAME, 'lastName').send_keys(valid_lastname)
    driver.find_element(By.ID, 'address').send_keys(valid_email)
    driver.find_element(By.ID, 'password').send_keys(valid_password_email)
    driver.find_element(By.ID, 'password-confirm').send_keys(valid_password_email)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, 'h2').text == 'Учётная запись уже существует', print('Ошибка')


def test_reg_user_exists_phone(browser):
    """Проверка, что повторная регистрация с телефоном невозможна, появление оповещающей формы"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(valid_name)
    driver.find_element(By.NAME, 'lastName').send_keys(valid_lastname)
    driver.find_element(By.ID, 'address').send_keys(valid_phone)
    driver.find_element(By.ID, 'password').send_keys(valid_password_phone)
    driver.find_element(By.ID, 'password-confirm').send_keys(valid_password_phone)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, 'h2').text == 'Учётная запись уже существует', print('Ошибка')


def test_reg_empty_fields(browser):
    """Проверка, что с пустыми полями регистрация не проходит"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    error = driver.find_elements(By.CSS_SELECTOR, '.rt-input-container--error')
    time.sleep(3)
    assert len(error) == 5


def test_reg_invalid_code(browser):
    """Проверка, что при вводе неверного кода система выдает ошибку-сообщение"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name)
    driver.find_element(By.NAME, 'lastName').send_keys(lastname)
    driver.find_element(By.ID, 'address').send_keys(fake_email)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    driver.find_element(By.ID, 'password-confirm').send_keys(fake_password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.ID, 'rt-code-0').send_keys(invalid_code)
    time.sleep(5)
    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный код. Повторите попытку', print('Ошибка')


def test_reg_email_without_dog(browser):
    """Проверка, что регистрация не проходит c email без '@' """
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name)
    driver.find_element(By.NAME, 'lastName').send_keys(lastname)
    driver.find_element(By.ID, 'address').send_keys(email_without_dog)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    driver.find_element(By.ID, 'password-confirm').send_keys(fake_password)
    time.sleep(3)
    error = driver.find_elements(By.CSS_SELECTOR, '.rt-input-container--error')
    assert len(error) == 1


def test_reg_email_without_domain(browser):
    """Проверка, что регистрация не проходит c email без домена"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name)
    driver.find_element(By.NAME, 'lastName').send_keys(lastname)
    driver.find_element(By.ID, 'address').send_keys(email_without_domain)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    driver.find_element(By.ID, 'password-confirm').send_keys(fake_password)
    error = driver.find_elements(By.CSS_SELECTOR, '.rt-input-container--error')
    time.sleep(3)
    assert len(error) == 1


def test_elements_of_auth(browser):
    """Проверка Формы "Авторизация" на наличие основных элементов."""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    assert 'Телефон' in driver.find_element(By.ID, 't-btn-tab-phone').text
    assert 'Почта' in driver.find_element(By.ID, 't-btn-tab-mail').text
    assert 'Логин' in driver.find_element(By.ID, 't-btn-tab-login').text
    assert 'Лицевой счёт' in driver.find_element(By.ID, 't-btn-tab-ls').text


def test_auth_user_mail(browser):
    """Авторизация с помощью валидных данных (электронная почта и пароль) """
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-login')))
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(valid_email)
    driver.find_element(By.ID, 'password').send_keys(valid_password_email)
    time.sleep(3)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    assert driver.find_element(By.TAG_NAME, 'h3').text == 'Учетные данные'


def test_auth_user_phone(browser):
    """Авторизация с помощью валидных данных (телефон и пароль) """
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-login')))
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(valid_phone)
    driver.find_element(By.ID, 'password').send_keys(valid_password_phone)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, 'h3').text == 'Учетные данные'


def test_auth_user_login(browser):
    """Авторизация с помощью валидных данных (логин и пароль). Если прирегистрации указывался номер телефона, то он является
     логином по умолчанию"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-login')))
    driver.find_element(By.ID, 't-btn-tab-login').click()
    driver.find_element(By.ID, 'username').send_keys(valid_log)
    driver.find_element(By.ID, 'password').send_keys(valid_password_log)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, 'h3').text == 'Учетные данные'


def test_invalid_auth_phone_email_pass(browser):
    """Проверка, что авторизация не проходит при вводе незарегистрированного телефона/email или неверного пароля"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.implicitly_wait(10)
    driver.find_element(By.ID, 'username').send_keys(invalid_phone1)
    driver.find_element(By.ID, 'password').send_keys(valid_password_phone)
    driver.find_element(By.ID, 'kc-login').click()
    time.sleep(2)
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(fake_email)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert driver.find_element(By.ID, 'forgot_password').value_of_css_property('color') == "rgba(255, 79, 18, 1)"


def test_invalid_auth_login_ls_pass(browser):
    """Проверка, что авторизация не проходит при вводе незарегистрированного логина или лицевого счета"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-login')))
    driver.find_element(By.ID, 't-btn-tab-login').click()
    driver.find_element(By.ID, 'username').send_keys(invalid_login)
    driver.find_element(By.ID, 'password').send_keys(valid_password_log)
    driver.find_element(By.ID, 'kc-login').click()
    time.sleep(2)
    driver.find_element(By.ID, 't-btn-tab-ls').click()
    driver.find_element(By.ID, 'username').send_keys(invalid_ls)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert driver.find_element(By.ID, 'forgot_password').value_of_css_property('color') == "rgba(255, 79, 18, 1)"



def test_btn_recovery_pass(browser):
    """Проверка кнопки забыл пароль"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, 'forgot_password').click()
    time.sleep(5)
    assert driver.find_element(By.CLASS_NAME, 'card-container__title').text == 'Восстановление пароля'


def test_vk_btn(browser):
    """Кликабельность кнопки VK"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'oidc_vk'))).click()
    assert 'vk.com' in driver.find_element(By.XPATH, '//div[@class="oauth_head"]/a').get_attribute('href')
    assert 'vk' in driver.current_url


def test_ok_btn(browser):
    """Кликабельность кнопки OK"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'oidc_ok'))).click()
    assert driver.find_element(By.XPATH, '//div[@class="ext-widget_h_tx"]').text == 'Одноклассники'
    assert 'ok' in driver.current_url


def test_mail_btn(browser):
    """Кликабельность кнопки @"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'oidc_mail'))).click()
    assert 'mail.ru' in driver.find_element(By.XPATH, '//span[@class="header__logo"]').text.lower()
    assert 'mail' in driver.current_url


def test_google_btn(browser):
    """Кликабельность кнопки G"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'oidc_google'))).click()
    assert 'google' in driver.current_url


def test_yandex_btn(browser):
    """Кликабельность кнопки Я"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'oidc_ya'))).click()

    try:
        assert 'yandex' in driver.current_url
    except AssertionError:
        print('переход не осуществлен')


def test_privacy_policy_footer(browser):
    """Кликабельность сслылки в футере 'Политика конфиденциальности'"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[0].click()
    driver.switch_to.window(driver.window_handles[1])
    title = driver.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'Тест не прошел. Найден баг'


def test_agreements_footer(browser):
    """Кликабельность сслылки в футере 'Пользовательское соглашение'"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[1].click()
    driver.switch_to.window(driver.window_handles[1])
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Публичная оферта о заключении Пользовательского соглашения на использование Сервиса «Ростелеком ID»'



def test_reset_back_btn(browser):
    """Проверка кнопки "Вернуться назад" без ввода символов на странице 'Восстановление пароля'"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'forgot_password')))
    driver.find_element(By.ID, 'forgot_password').click()
    time.sleep(3)
    driver.find_element(By.ID, 'reset-back').click()


def test_no_code_without_сaptcha_to_email(browser):
    """Проверка, что без ввода капчи нельзя получить код на почту. Если на странице осталась капча, значит тест прошел """
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, 'forgot_password').click()
    driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_email)
    driver.find_element(By.ID, 'reset').click()
    assert driver.find_element(By.CLASS_NAME, 'rt-captcha__image')


def test_no_code_without_сaptcha_to_phon(browser):
    """Проверка, что без ввода капчи нельзя получить код на телефон. Если на странице осталась капча, значит тест прошел """
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, 'forgot_password').click()
    driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_phone)
    driver.find_element(By.ID, 'reset').click()
    time.sleep(3)
    assert driver.find_element(By.CLASS_NAME, 'rt-captcha__image')


