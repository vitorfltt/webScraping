from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pymysql
import time
from difflib import SequenceMatcher

try:
    db = pymysql.connect("localhost", "root", "", "crawler")
    cursor = db.cursor()
except:
    print("Erro na conexão") 


url = "https://www.americanas.com.br/busca/iphone"

net = webdriver.Firefox()
net.get(url)
wait = WebDriverWait(net,10)

try:
    wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class=""]/div[6]/div/div/div/div[1]')))
except Exception as e:                                        
    print(e)

count_key = 0
while count_key < 7:
    net.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN) 
    count_key += 1
    time.sleep(1)

whole = net.find_elements_by_xpath('//*[@id="content-middle"]/div[6]/div/div/div/div[1]/div')
#print(len(whole))
#print(whole)
try:

    for x in range(1, len(whole)):
        caminho = net.find_element_by_xpath(f"//*[@id='content-middle']/div[6]/div/div/div/div[1]/div[{x}]/div/div[2]")
        link = caminho.find_element_by_xpath(f'//*[@id="content-middle"]/div[6]/div/div/div/div[1]/div[{x}]/div/div[2]/a')
        href = link.get_attribute('href')     
        print(href)

        # nome
        n = net.find_element_by_xpath(f'//*[@id="content-middle"]/div[6]/div/div/div/div[1]/div[{x}]/div/div[2]/a/section/div[2]')
        name = n.find_element_by_xpath(f'//*[@id="content-middle"]/div[6]/div/div/div/div[1]/div[{x}]/div/div[2]/a/section/div[2]/div[1]')
        nome = name.find_element_by_tag_name('h2')
        print(nome.text)

        #preco
        p = n.find_element_by_xpath(f'//*[@id="content-middle"]/div[6]/div/div/div/div[1]/div[{x}]/div/div[2]/a/section/div[2]/div[2]/div[2]')
        preco = p.find_element_by_tag_name('span')
        preco = preco.text.split(' ', 2)
        print(preco[1])

        #imagem
        img = net.find_element_by_xpath(f'//*[@id="content-middle"]/div[6]/div/div/div/div[1]/div[{x}]/div/div[2]/a/section/div[1]/div/div/picture/img')
        foto = img.get_attribute('src')
        print(foto)
        print(20*'-'+str(x))
        
        
        #seq = SequenceMatcher(None,'iphone 7 128gb preto', ' '.join(nome.text.split()[:6]) )
        #if seq.ratio() >= 0.70:
        #    print(nome.text)
        





        

        select  = f"SELECT * FROM produtos WHERE nome = '{nome.text}'"

        insert = "INSERT INTO `produtos` (`nome`, `valor`, `link`, `loja`, `img`) VALUES ('%s','%s','%s','americanas','%s')"%(nome.text,preco[1],href,foto)

        try:
            cursor.execute(select)
            records = cursor.fetchall()

            if records[0][1] == nome.text:
                cursor.execute(f"UPDATE `produtos` SET `valor` = '{preco[1]}' WHERE `produtos`.`id` = '{records[0][0]}';")
            else:
                cursor.execute(insert)
                db.commit()
        except Exception as e:
            print(e)




except Exception as a:
    print(a)




                                    








