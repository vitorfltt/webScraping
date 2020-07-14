from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/"
caminho = []
f = open("cel.csv","w")
f.write("titulo|comentarios|nota\n")


net = webdriver.Firefox()
net.get(url)
wait = WebDriverWait(net,10)

try:
    wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="__next"]/div[4]/div/div')))
except:
    print("nao encontrou o elemento")

try:
    #pegando links
    divs = net.find_elements_by_xpath('//*[@id="showcase"]/ul[1]/div')
    v = 0
    for x in divs:
        v += 1
        link = x.find_element_by_tag_name("a")
        h = link.get_attribute("href")
        print(h)
        caminho.append(h)
        #print(len(caminho))
        if v >= 2:
            break
        else:
            pass

except:
    print("nao")

#pegando comentarios
for w in caminho:
    net.get(w)
    try:
        comments = net.find_elements_by_class_name("wrapper-review__comment")
        for comment in comments:
            post = comment.find_element_by_class_name("product-review__post")
            titulo = post.find_element_by_tag_name("span")
            texto = post.find_element_by_tag_name("p")
            print("TITULO:", titulo.text)
            print("DESCRICAO:", texto.text)
            f.write(f"{titulo.text}|{texto.text}|")
            print("-"*30)

            star = comment.find_element_by_class_name("rating-percent__full")
            print(star.text)
            nota = len(star.text)
            print(nota)
            if nota <= 3:
                nota = 0
                f.write(f"{nota}\n")
            elif nota > 3 and nota < 7:
                nota = 1
                f.write(f"{nota}\n")
            elif nota >= 7:
                nota = 2
                f.write(f"{nota}\n")
            #qtd = principal.find_element_by_tag_name("span")
            #print(qtd.text)
            #class_star = qtd.find_element_by_class_name("rating-percent__numbers")
            #print(class_star.text)
    except:
        print("nao foi")
f.close()






 



