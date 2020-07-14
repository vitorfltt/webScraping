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

url = "https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone/iphone?ordenacao=relevance&origem=omega"


net = webdriver.Firefox()
net.get(url)
wait = WebDriverWait(net,10)

try:
    wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="content-middle"]/div[4]/div/div/div/div[1]')))
except Exception as e:                                        
    print(e)


count_key = 0
while count_key < 10:
    net.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN) 
    count_key += 1
    time.sleep(1)
       
whole = net.find_elements_by_xpath('//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div')


#for x in range(len(whole)): 
#    print (whole[x].text)

v = 0

try:
    for y in range(1, len(whole)):

        v += 1

        #link
        father = net.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]')
        time = father.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]/div')
        son = time.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]/div/div[1]')
        d = son.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]/div/div[2]')
        a = d.find_element_by_tag_name('a')
        href = a.get_attribute('href')
        print(href)

        #nome
        n = d.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]/div/div[2]/a/section')
        proc = n.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]/div/div[2]/a/section/div[2]')
        find = proc.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]/div/div[2]/a/section/div[2]/div[1]')
        name = find.find_element_by_tag_name('h2')
        print(name.text)

        #preco
        p = n.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]/div/div[2]/a/section/div[2]/div[2]')
        price = p.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{y}]/div/div[2]/a/section/div[2]/div[2]/div[2]')
        preco = price.find_element_by_tag_name('span')
        preco = preco.text.split(' ', 2)
        print(preco[1])
        #print(preco.text)

        #imagem
        pic = net.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[1]/div/div[2]/a/section/div[1]/div/div/picture/img')
        photo = pic.get_attribute('src')
        print(photo)

        select  = f"SELECT * FROM produtos WHERE nome = '{name.text}'"

        insert = "INSERT INTO `produtos` (`nome`, `valor`, `link`, `loja`,`img`) VALUES ('%s','%s','%s', 'submarino','%s')"%(name.text,preco[1],href,photo)

        try:
            cursor.execute(select)
            records = cursor.fetchall()

            if records[0][1] == name.text:
                cursor.execute(f"UPDATE `produtos` SET `valor` = '{preco[1]}' WHERE `produtos`.`id` = '{records[0][0]}';")
                
            else:
                cursor.execute(insert)
                db.commit()

        except Exception as e:
            print(e)

except Exception as e:
    print(e)


    

                                         