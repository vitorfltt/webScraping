from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
url = "https://www.jcnet.com.br/Politica"


# Abre firefox
driver = webdriver.Firefox()
#navega para uma URL
driver.get(url)

#Aguarda o elemento
wait = WebDriverWait(driver, 10)
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[1]/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody")))
except:
    print("nao encontrou o elemento")

#pega um elemento
tag_tds = driver.find_elements_by_xpath("/html/body/table/tbody/tr[1]/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td")
noticias = {}
acho_data = False
for td in tag_tds:
    try:
        data = td.find_element_by_tag_name("div")
        print(data.text)
        if not acho_data:
            acho_data = data.text
            noticias[acho_data] = []
        else:
            break
    except:
        pass
    try:
        link = td.find_element_by_tag_name("a")
        span = link.find_element_by_tag_name("span")
        print(link.get_attribute("href"))
        print(span.text)
        obj = {
            "link": link.get_attribute("href"),
            "titulo": span.text,
            "sub_titulo": None         
            }

        noticias[acho_data].append(obj)
    except:
        pass

for x in range(len(noticias[acho_data])):
    link = noticias[acho_data][x]["link"]

    #navega para uma URL
    driver.get(link)

    #Aguada o elemento
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[1]/td[2]/main/div/h2/em")))
    except:
        print("nao encontrou o elemento")
    tag_em = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[2]/main/div/h2/em")
    noticias[acho_data][x]["sub_titulo"] = tag_em.text
print(noticias)



