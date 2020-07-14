from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql

try:
    db = pymysql.connect("localhost", "root", "", "crawler")
except:
    print("Erro na conexão") 

cursor = db.cursor()

url = "https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone/iphone?ordenacao=relevance&origem=omega"

net = webdriver.Firefox()
net.get(url)
wait = WebDriverWait(net,10)


for x in range (20):
    try:
        caminho = net.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{x}]')
        way = caminho.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{x}]/div/div[2]/a/section/div[2]/div[1]')
        name = way.find_element_by_tag_name('h3')
        #print(name.text)

        price = net.find_element_by_xpath(f'//*[@id="content-middle"]/div[4]/div/div/div/div[1]/div[{x}]/div/div[2]/a/section/div[2]/div[2]/div[2]/span')
        #print(price.text)
        try:
            cursor.execute("INSERT INTO `produtos` (`nome`, `valor`, `link`, `loja`) VALUES (", name ,", ", price ,",'link', 'pontoFrio');")
        except:
            print("Erro no Insert")

    except:                                    
        pass
                                         