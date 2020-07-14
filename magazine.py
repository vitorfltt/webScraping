from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pymysql
import time

try:
    db = pymysql.connect("localhost", "root", "", "crawler")
    cursor = db.cursor()
except:
    print("Erro na conexão") 

url = "https://www.magazineluiza.com.br/iphone/celulares-e-smartphones/s/te/teip/"

nav = webdriver.Firefox()
nav.get(url)
wait = WebDriverWait(nav,10)

try:
    wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="showcase"]')))
except Exception as e:
    print(e)

caminho = nav.find_elements_by_xpath('//*[@id="showcase"]/ul[1]/a')
count_key = 0
while count_key < 8:
    nav.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN) 
    count_key += 1
    time.sleep(1)


try:

    for x in range(1, len(caminho)):
    
        h = nav.find_element_by_xpath(f'//*[@id="showcase"]/ul[1]/a[{x}]/div[3]/h3')
        preco = nav.find_element_by_xpath(f'//*[@id="showcase"]/ul[1]/a[{x}]/div[3]/div[2]/div[2]')
        preco = preco.text.split(' ', 2)
        print(preco[1])

        way = nav.find_element_by_xpath(f'//*[@id="showcase"]/ul[1]/a[{x}]')
        link = way.get_attribute('href')
        print(link)

        print(h.text)

        #imagem
        ft = nav.find_element_by_xpath(f'//*[@id="showcase"]/ul[1]/a[{x}]')
        pic = ft.find_element_by_xpath(f'//*[@id="showcase"]/ul[1]/a[{x}]/div[2]')
        picture = pic.find_element_by_tag_name('img')
        foto = picture.get_attribute('src')
        
        print(foto)
        print(20*'--'+str(x))
        


        select  = f"SELECT * FROM produtos WHERE nome = '{h.text}'"

        insert = "INSERT INTO `produtos` (`nome`, `valor`, `link`, `loja`,`img`) VALUES ('%s','%s','%s', 'magazine','%s')"%(h.text,preco[1],link,foto)
        
        try:
            cursor.execute(select)
            records = cursor.fetchall()

            if records[0][1] == h.text:
                cursor.execute(f"UPDATE `produtos` SET `valor` = '{preco[1]}' WHERE `produtos`.`id` = '{records[0][0]}';")
            else:
                cursor.execute(insert)
                db.commit()
        except Exception as e:
            print(e)
     
except Exception as e:
    print(e)

#db.close()







