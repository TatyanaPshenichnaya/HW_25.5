import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # ставим величину неявного ожидания элементов в 10 секунд
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, 'email').send_keys('tinitta@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('Pet-42729595')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # перейдем в мои питомцы
    driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()


    yield driver

    driver.quit()


def test_check_pets_number(driver):
    # проверим, что присутствуют все наши питомцы

    # узнаем статистику питомцев
    #my_pets_number = driver.find_element(By.XPATH, '(/html/body/div[1]/div/div[1])[1]')
    # реализация явного ожидания ( второй аргумент - время максимального ожидания в сек)
    my_pets_number = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.XPATH, '(/html/body/div[1]/div/div[1])[1]'))
    )
    my_pets_number = my_pets_number.text.split()
    my_pets_number = int(my_pets_number[2])
    print(my_pets_number)

    # проверим, что присутствуют все питомцы, т.е. количество строк в таблице совпадает со статистикой
    pets = driver.find_elements(By.XPATH, '//tbody/tr')
    assert my_pets_number == len(pets)


def test_check_pets_photo(driver):
    # проверим, что хотя бы у половины питомцев есть фото
    # узнаем статистику питомцев
    #
    my_pets_number = driver.find_element(By.XPATH, '(/html/body/div[1]/div/div[1])[1]')
    my_pets_number = my_pets_number.text.split()
    my_pets_number = int(my_pets_number[2])

    pets = driver.find_elements(By.XPATH, '//tbody/tr')
    images = driver.find_elements(By.XPATH, '//th/img')
    img = 0
    for i in range(len(pets)):
       if images[i].get_attribute('src') != '':
          img += 1

    print(img)
    assert my_pets_number / 2 <= img


def test_check_pets_name_breed_age(driver):
    # проверим, что у всех питомцев есть имя, порода и возраст
    line = driver.find_elements(By.XPATH, '//tbody/tr/td')  # найдет в 4 раза больше элементов, т.к.в ряду 4 параметра

    for i in range(0, len(line), 4):  # поэтому тут я возьму только имена через цикл и шаг 4
       assert line[i].text != ''

    for i in range(1, len(line), 4):  # поэтому тут я возьму только породы через цикл и шаг 4
       # print(line[i].text)
       assert line[i].text != ''

    for i in range(2, len(line), 4):  # поэтому тут я возьму только возраст через цикл и шаг 4
       # print(line[i].text)
       assert line[i].text != ''


def test_check_pets_names_distinct(driver):
    # проверим, что у всех питомцев разные имена
    names = []
    line = driver.find_elements(By.XPATH, '//tbody/tr/td')  # найдет в 4 раза больше элементов, т.к.в ряду 4 параметра
    for i in range(0, len(line), 4):  # имена через цикл
       if line[i].text not in names:
          names.append(line[i].text)
       else:
          assert line[i].text not in names  # иначе  тест провален


def test_check_pets_distinct(driver):
    # проверим, что в списке нет повторяющихся питомцев
    pet_array = []
    line = driver.find_elements(By.XPATH, '//tbody/tr/td')  # найдет в 4 раза больше элементов, т.к.в ряду 4 параметра
    for i in range(0, len(line), 4):  # массив с питомцам с данными по именам, породе и возрасту
       a_pet = []
       a_pet.append(line[i].text)
       a_pet.append(line[i + 1].text)
       a_pet.append(line[i + 2].text)
       if a_pet not in pet_array:
          pet_array.append(a_pet)
          print(a_pet)
       else:
          assert a_pet not in pet_array

