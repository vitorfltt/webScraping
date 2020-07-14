from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.jcnet.com.br"

navega = webdriver.Firefox()
navega.get(URL)
wait = WebDriverWait(navega,10)

try:
    wait.until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/div[1]/table/tbody")))
except:
    print("nao encontrou o elemento")

lis = navega.find_elements_by_xpath("/html/body/div[1]/table/tbody/tr[2]/td[1]/div/div/li")
links = []

v = 0
for x in lis:
    try:
        a = x.find_element_by_tag_name("a")
        h = a.get_attribute("href")
        links.append(h)
    except:
        pass
    v += 1
    if v >= 10:
        break
    else:
        pass
f = open("noticias.csv","w")
f.write("data|link|titulo\n")
print(links)

for link in links:
    navega.get(link)
    caminho = navega.find_elements_by_xpath("/html/body/table/tbody/tr[1]/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td")
    for td in caminho:
        try:
            data = td.find_element_by_tag_name("div") 
            date = data.text
            print(date) 
            f.write(date)
        except:
            pass
        
        try:
            tag_a = td.find_element_by_tag_name("a")
            href = tag_a.get_attribute("href")
            print(href)
            span = tag_a.find_element_by_tag_name("span")
            print(span.text)
            f.write(f"|{href}|{span.text}\n")
        except:
            pass

f.close()        

        








