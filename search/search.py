import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

LOGIN = '******'
PASSWORD = '*******'

class SearchNN:

    def __init__(self, login, password, mode):
        self.login = login
        self.password = password
        self.mode = mode

    def get_raz(self, stran):
    
        url = 'https://portal.unn.ru/stream/'
        driver = webdriver.Chrome(executable_path='chrome/chromedriver')
        driver.get(url)
        driver.find_element(By.XPATH, '//*[@id="login-popup"]/div[2]/form/div[1]/div[1]/div/div[1]/input').send_keys(self.login)
        driver.find_element(By.XPATH, '//*[@id="login-popup"]/div[2]/form/div[1]/div[1]/div/div[2]/input').send_keys(self.password)
        driver.find_element(By.XPATH, '//*[@id="login-popup"]/div[2]/form/div[2]/input').click()
        driver.find_element(By.XPATH, '//*[@id="bx_left_menu_menu_vuz_ruz"]/a/span[2]').click()
        
        
        for i in range(stran):
            data = []
            sleep(2)
            page = driver.page_source
            driver.find_element(By.XPATH, '//*[@id="workarea-content"]/div/ruz-root/div/ruz-main-index/ruz-list/div[1]/div[1]/div[5]/div/button[2]').click()
            soup = BeautifulSoup(page, 'html.parser')   
            samples = soup.find_all('div', class_="media day ng-star-inserted")
                
            date = []
            day_of_the_week = []
            time = []
            name_lesson = []
            class_lesson = []
            auditorium = []
            corpus = []
            lecturer = []

            for i in samples:
                date.append(i.find('div', class_='d-lg-none date clearfix').span.text[1:-6])
                day_of_the_week.append(i.find('span', class_="ml-2 font-italic").text[1:-1])
                time.append(i.find('span', class_="float-right").text.replace('\xa0', ' ')[1:-1])
                name_lesson.append(i.find('div', class_='title').span.text[1:-1])
                class_lesson.append(i.find('div', class_='text-muted kind ng-star-inserted').text[1:-1])
                auditorium.append(i.find('span', class_='auditorium').text[1:-1].replace('д.а.', 'Виртуальное'))
                corpus.append(i.find('span', class_='mr-2 text-muted ng-star-inserted').text[2:-2])
                lecturer.append(i.find('div', class_='lecturer').text[1:-1].replace('!Вакансия', 'Физруки'))

            dataframe = pd.DataFrame({
                'date': date,
                'day_of_the_week' : day_of_the_week,
                'time': time,
                'name_lesson': name_lesson,
                'class_lesson': class_lesson,
                'auditorium': auditorium,
                'corpus': corpus,
                'lecturer': lecturer})
            data.append(dataframe)
        dataframe_concat = pd.concat(data).drop_duplicates()

        if self.mode == 'file':
            dataframe_concat.to_excel('data/dataframe_raspisaniye_fsn.xlsx')
        else:
            return dataframe_concat

    def studednts(self, iter = 60):
        
        url = 'https://portal.unn.ru/stream/'
        driver = webdriver.Chrome(executable_path='chrome/chromedriver')
        driver.get(url)
        driver.find_element(By.XPATH, '//*[@id="login-popup"]/div[2]/form/div[1]/div[1]/div/div[1]/input').send_keys(self.login)
        driver.find_element(By.XPATH, '//*[@id="login-popup"]/div[2]/form/div[1]/div[1]/div/div[2]/input').send_keys(self.password)
        driver.find_element(By.XPATH, '//*[@id="login-popup"]/div[2]/form/div[2]/input').click()
        driver.find_element(By.XPATH, '//*[@id="bx_left_menu_menu_vuz_students"]/a/span[2]').click()
        sleep(3)
        driver.find_element(By.XPATH, '//*[@id="app-main-area"]/div/ng-component/div/app-search-student/div/glx-student-search/div/p-table/div/p-paginator/div/p-dropdown/div/div[2]').click()
        driver.find_element(By.XPATH, '//*[@id="app-main-area"]/div/ng-component/div/app-search-student/div/glx-student-search/div/p-table/div/p-paginator/div/p-dropdown/div/div[3]/div/ul/p-dropdownitem[5]/li').click()
        
        dict_ = {
            'name': [],
            'institut': [],
            'napravl': [],
            'group': [],
            'format': [],
            'kours': [],
            'prof': []
        }   


        for i in range(iter):
            sleep(2)
            page = driver.page_source
            driver.find_element(By.XPATH, '//*[@id="app-main-area"]/div/ng-component/div/app-search-student/div/glx-student-search/div/p-table/div/p-paginator/div/button[3]/span').click()
            soup = BeautifulSoup(page, 'html.parser')   
            samples = soup.find_all('tr', class_="p-selectable-row ng-star-inserted")
            for k in samples:
                
                name = k.find('div', class_="fullname mt-0 ng-star-inserted").text
                institut = k.find('div', class_="institut ng-star-inserted").text
                napravl = k.find('div', class_="direction ng-star-inserted").text
                group = k.find('div', class_="group ng-star-inserted").text
                format = k.find('div', class_="information").findAll('tr')[0].find('div', class_="information-value link").text
                kours = k.find('div', class_="information").findAll('tr')[1].find('div', class_="information-value link").text
                prof = k.find('div', class_="information").findAll('tr')[-1].find('div', class_="information-value link").text
                
                try:
                    prof = int(prof)
                    prof = napravl
                except:
                    None

                dict_['name'].append(name)
                dict_['institut'].append(institut)
                dict_['napravl'].append(napravl)
                dict_['group'].append(group)
                dict_['format'].append(format)
                dict_['kours'].append(kours)
                dict_['prof'].append(prof)
                 
        data = pd.DataFrame.from_dict(dict_)
        
        if self.mode == 'file':
            data.to_excel('data\dataframe_humans_unn.xlsx')
        else:
            return data
        

