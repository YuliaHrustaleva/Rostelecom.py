from faker import Faker
import string
import random
import os

from dotenv import load_dotenv

load_dotenv()

base_url = "https://" + "b2c.passport.rt.ru"

"""валидные данные"""
valid_name = 'Юлия'
valid_lastname = 'Хрусталева'
valid_email = os.getenv('valid_email')
valid_password_phone = os.getenv('valid_password_phone')
valid_password_email = os.getenv('valid_password_email')
valid_password_log = os.getenv('valid_password_log')
valid_phone = os.getenv('valid_phone')
valid_log = os.getenv('valid_log')

"""невалидные данные"""
fake = Faker()
name = "Анжелла"
lastname = 'Ручкина'
fake_email = 'Alikser@yandex.ru'
fake_password = 'Angl-12!'
email_without_domain = 'Alikser@yandex'
email_without_dog = 'Alikseryandex.ru'
invalid_code = '321654'
invalid_phone1 = '+799919999991'
invalid_login = 'Test'
invalid_ls = '352010007897'

def russian_chars(num):
    text = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def english_chars(num):
    text = 'abcdefghijklmnopqrstuvwxyz'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def number_chars(num):
    text = '0123456789'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def chinese_chars(num):
    text = '的一是不了人我在有他这为之大来以个中上们'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def special_chars(num):
    text = '|/!@#$%^&*()-_=+`~?"№;:[]{}'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string


def password_random(num): # т.к. в пароле обязаны быть строчнаяб заглавная и спецсимвол/число, прибавляем их в начало. Остаток символов выбирается рандомно
    text = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    text1 = 'abcdefghijklmnopqrstuvwxyz'
    text2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text3 = '+-/*!&$#?=@<>1234567890'
    rand_string =  ''.join(random.choice(text1) for i in range(1)) + ''.join(random.choice(text2) for i in range(1)) + ''.join(random.choice(text3) for i in range(1)) + ''.join(random.choice(text) for i in range(num-3))
    return rand_string
