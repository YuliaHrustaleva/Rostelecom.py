import time
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from settings import *



@pytest.fixture(autouse=True)
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(6)
    driver.get('https://b2c.passport.rt.ru')
    yield driver
    driver.quit()




@pytest.mark.parametrize("negative_input", [russian_chars(1), russian_chars(31), russian_chars(256), english_chars(15), number_chars(18), chinese_chars(10), special_chars(19)], ids=['1 символ кир.', '31 символ кир.', '256 символов кир.', '15 символов лат.', '18 цифр', '10 иероглифов', '19 спецсимволов'])
def test_incorrect_name_reg(negative_input, browser):
    """Проверка, что система выводит ошибку сообщение-подсказку, при попытке сохранить в поле "Имя" при регистрации символы не соответствующие требованиям"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, "kc-register").click()
    driver.find_element(By.NAME, "firstName").send_keys(negative_input)
    driver.find_element(By.NAME, "lastName").click()

    assert driver.find_element(By.CLASS_NAME,"rt-input-container__meta").text == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."

@pytest.mark.parametrize("negative_input", [russian_chars(1), russian_chars(31), russian_chars(256), english_chars(15), number_chars(18), chinese_chars(10), special_chars(19)], ids=['1 символ кир.', '31 символ кир.', '256 символов кир.', '15 символов лат.', '18 цифр', '10 иероглифов', '19 спецсимволов'])
def test_incorrect_surname_reg(negative_input, browser):
    """Проверка, что система выводит ошибку (сообщение-подсказку), при попытке сохранить в поле "Фамилия" при регистрации символы не соответствующие требованиям"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, "kc-register").click()
    driver.find_element(By.NAME, "firstName").clear()
    driver.find_element(By.NAME, "lastName").send_keys(negative_input)
    driver.find_element(By.NAME, "firstName").click()
    assert driver.find_element(By.CLASS_NAME, "rt-input-container__meta").text == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@pytest.mark.parametrize("negative_input", ['Alikseryandex.ru', '@yandex.ru', 'Alikser@', 'Alik..ser@yandex.ru', '.alikser@yandex.ru', 'alikser@.yandex.ru.'], ids=['отсутствие @ в email', 'отсутствие лок. части', 'отсутствие дом. части', 'содержит две точки подряд', 'лок. часть начинается и/или заканчивается с точки', 'дом. часть начинается и/или заканчивается с точки'])
def test_incorrect_email_reg(negative_input, browser):
    """Проверка, что система выводит ошибку (сообщение-подсказку), при попытке сохранить в поле "email или телефон"
    при регистрации почты не соответствующей требованиям"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, "kc-register").click()
    driver.find_element(By.ID, "address").send_keys(negative_input)
    driver.find_element(By.ID, "password").click()
    assert driver.find_element(By.CLASS_NAME,
                               "rt-input-container__meta").text == "Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru"



@pytest.mark.parametrize("negative_input", ['+7 926 381-64-912', '+7 926 381-64-9', '+375 96 858-56-3', '+375 96 858-56-333', '+375 17 аа-37-41', '+7 962 381-之大-91'], ids=['12 цыфр', '10 цыфр', '11 цыфр', '13 цыфр', 'цыфры+буквы', 'цыфры+иероглифы'])
def test_incorrect_phone_reg(negative_input, browser):
    """Проверка, что система выводит ошибку (сообщение-подсказку), при попытке сохранить в поле "email или телефон" при
    регистрации номер телефона не соответствующий требованиям"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, "kc-register").click()
    driver.find_element(By.ID, "address").send_keys(negative_input)
    driver.find_element(By.ID, "password").click()
    assert driver.find_element(By.CLASS_NAME,
                               "rt-input-container__meta").text == "Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru"


@pytest.mark.parametrize("negative_input", ['(Alena', '(Aлена13', '№;:?(*(*)', '(alena1322)', 'AA12568-947', '(Alena1322)(Alena1322)', 'ALENA-ALENA'], ids=['6 символов', '8 символов с кирилицей', 'спецсимволы', 'строчный буквы', 'цыфры', 'более 20 символов', 'заглавные буквы и символ'])
def test_incorrect_password_reg(negative_input, browser):
    """Проверка, что система выводит ошибку (сообщение-подсказку), при попытке сохранить в поле "Пароль" пароль
    не соответствующий требованиям. Ожидаем, что при невалидно заполненных полях ошибка
    NoSuchElementException не возникнет (то есть что текст-предупреждение высвечивается)"""
    driver = browser
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, "kc-register").click()
    driver.find_element(By.ID, "password").send_keys(negative_input)
    driver.find_element(By.ID, "address").click()
    temporary = False
    try:
        driver.find_element(By.XPATH,
                                   "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[4]/div[1]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == False






