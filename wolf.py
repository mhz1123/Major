# from urllib.request import Request, urlopen
# from bs4 import BeautifulSoup as soup

# url = 'https://www.sciencedaily.com/news/matter_energy/physics/'

# req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

# webpage = urlopen(req).read()

# page_soup = soup(webpage, "html.parser")

# containers = page_soup.findAll("h2","latest-head")
# for container in containers:
#     print(container)


import wolframalpha
client = wolframalpha.Client("R4U7JP-TEAKU27YYE")

def inp():
    testq = str(input())
    return testq

def search():
    testq=inp()
    res = client.query(testq)
    print(next(res.results).text)

# search(testq)