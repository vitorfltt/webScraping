import requests
from bs4 import BeautifulSoup


Antivirus = []

pag = 1
while True:
    URL_Anti = f"https://www.baixaki.com.br/busca/?r={pag}&q=antivirus&so=&buscar=26"
    response = requests.get(URL_Anti)
    html_doc = response.text
    bs = BeautifulSoup(html_doc, 'html.parser')
    cod = None
    for tags in bs.find_all("a"):
        if tags.get("href") and "/download/" in tags["href"]:
            Antivirus.append(tags["href"])
            

        
         
            
            
    pag += 25
    if pag >= 250:
        break
    
    print(pag)
input(len(set(Antivirus)))

URL = "https://www.baixaki.com.br"


coment = []
for antiv in set(Antivirus):
    montar = f"{URL}{antiv}#comentarios"
    response = requests.get(montar)
    html_doc = response.text
    bs = BeautifulSoup(html_doc, 'html.parser')

    cod = None
    for tags in bs.find_all("a"):
        if tags.get("href") and "comentarios.asp?cod=" in tags["href"]:
            cod = tags["href"].split("cod=")[-1]     
            break

    pag = 1
    while True:
        link_json = f"https://www.baixaki.com.br/inc/asp/get-comentarios.asp?codprograma={cod}&pagina={pag}"
        response = requests.get(link_json)
        try:
            results = response.json()
        except:
            break
        if len(results) == 0:
            break
        for obj in results:
            new_obj = {
                "titulo": obj["titulo"],
                "comentario": obj["comentario"],
                "nota": obj["nota"]
            }
            coment.append(new_obj)
           
        print(f"MUDANDO DE PAGINA {pag} da pesquisa {antiv}")
        pag += 1



f = open("antivirus.csv","w")
f.write("titulo,nota,comentario\n")
for add in coment:
    linha=add["titulo"] + "," +add["nota"]+","+ add["comentario"]+"\n"
    f.write(linha)
f.close()

print(f"Comentario capturado {len(coment)}")
print(len(Antivirus))


