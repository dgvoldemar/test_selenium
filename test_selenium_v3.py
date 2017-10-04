# -*- coding: utf-8 -*-

#v3 Применение мыши и запуск каждый раз нового окна mozilla

from selenium import webdriver
from selenium.webdriver.remote.webdriver import  WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import sys, math, time, random



#work with file

array_search = []
with open ("C:\\geckodriver\\search_ya.txt") as f:
    for line in f:
        array_search.append(line.strip())
        print (line)
f.close()
random.shuffle(array_search)# перемешивание порядка запросов в поисковике

def Random_int(x,y):
    random_int = random.randint(x, y)
    return (random_int)

def Run_robot(zapros):

    #Создание драйвера
    driver = webdriver.Firefox(executable_path='C:\\geckodriver\\geckodriver.exe')

    #Вход на геолокацию яндекса
    driver.get("https://yandex.ru/tune/geo/")
    time.sleep(1)
    elem_geo = driver.find_element_by_id("city__front-input")
    ActionChains(driver).move_to_element(elem_geo).perform()
    print (elem_geo.get_attribute("value"))
    
    
    if (elem_geo.get_attribute("value") == "Краснодар"):
        print ("Гео выставлено краснодар")
        #Ждем перехода на yandex
    else:
        elem_geo.clear()
        elem_geo.send_keys("Краснодар")
        time.sleep(2)
        driver.find_element_by_css_selector("div.b-autocomplete-item__reg").click()
        time.sleep(2)
        elem_geo.submit()
        print ("Гео поменяли на Краснодар")
        #Ждем перехода на yandex
    time.sleep(3)


    #Вход на яндекс для отправки поискового запроса

    driver.get("http://www.yandex.ru")
    element = driver.find_element_by_id("text")
    ActionChains(driver).move_to_element(element).click().perform()
    element.send_keys(zapros)
    element.submit()
    try:
        #we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 10).until(EC.title_contains(zapros))
        print (driver.title)
    finally:
        print ("Страница загружена")

    time.sleep(Random_int(5,7))

    #JS код для замены _blank на _self в target всех ссылок на странице

    jscode = '''
    var elem = document.body.getElementsByTagName('a');
    for(var i=0; i<elem.length; i++) elem[i].setAttribute("target", "_self");
    '''


    #Поиск нужной ссылки на сайт в поисковой выдаче
    search_cycle = 0
    for i in range(1,22):
        driver.execute_script(jscode) #сразу превращаем все ссылки в _self
        try:
            driver.find_element_by_link_text("unika23.ru").click()
            print ("Должен был нажать на ссылку unika23.ru...")
            print ("\n" + zapros + ": НАЙДЕН на "+ str (search_cycle) +" стр."+"\n")
            break
        except NoSuchElementException:
            driver.find_element_by_link_text("дальше").click()
            search_cycle += 1
            time.sleep(4)#действия если не нашли

    time.sleep(2)
    if (search_cycle >= 21):
        print ("\n" + zapros + ": Нет на 20 первых стр."+"\n")
        driver.quit() # выход из драйвера
        return

    #Еще одна проверка нажатия на ссылку
    
    try:
        driver.find_element_by_link_text("unika23.ru").click()
        print ("Должен был ЕЩЕ нажать на ссылку unika23.ru...")
    except NoSuchElementException:
        time.sleep(3)#действия если не нашли
   
    # Блок хождения по сайту
    #Первый проход с задержкой
    WebDriverWait(driver, 60).until(lambda x: x.find_element_by_link_text('Контакты'))#ожидание загрузки целевого элемента
    print ("Перешел на unika23.ru...")
    driver.find_element_by_tag_name('body').send_keys('\ue015' * Random_int(3,8))
    ActionChains(driver).move_by_offset(Random_int(-20,20), Random_int(-30,30)).perform()
    time.sleep(25) #- ожидание для яндекс

    #Второй и следующие проходы
    array_links = ["Пуско-наладочные работы", "Портфолио", "Контакты","Проектирование систем вентиляции","Монтаж систем вентиляции","Сервисное обслуживание систем кондиционирования","Поставка и монтаж оборудования систем вентиляции и кондиционирования"]
    random.shuffle(array_links)# перемешивание порядка запросов в ссылках сайта юника
    array_link_cute = random.sample(array_links, Random_int(3,4))
    for link in array_link_cute:
        WebDriverWait(driver, 30).until(lambda x: x.find_element_by_partial_link_text(link))
        act_link = driver.find_element_by_partial_link_text(link)
        try:
            act_link.location_once_scrolled_into_view
            ActionChains(driver).move_to_element(act_link).click().perform()
        except MoveTargetOutOfBoundsException:
            print ("Вне зоны видимости")

        WebDriverWait(driver, 30).until(lambda x: x.find_element_by_partial_link_text(link))
        time.sleep(Random_int(4,10))
        driver.find_element_by_tag_name('body').send_keys('\ue015' * Random_int(3,7))
        time.sleep(Random_int(3,9))
        driver.find_element_by_tag_name('body').send_keys('\ue015' * Random_int(2,6))
        time.sleep(Random_int(4,8))

    print ("\n" + zapros + ": Пройден полностью"+"\n")

    time.sleep(Random_int(10,20))
    driver.quit() # выход из драйвера

    return 

for zapros in array_search:
    print ("Запуск: "+zapros+"\n")
    Run_robot(zapros)


