import requests
from bs4 import BeautifulSoup
import os

if __name__ == "__main__":
    filePath = 'image_info.list'
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file ", filePath)
else:
    print ("Executed when imported")

class Main:
    def __init__(self):
        pass
    
    def fetch(self,url):
        page = requests.get(url)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        

    def func1(self):
        links = []
        results = self.soup.find_all('a', href=True)
        for anch in results:
            a = anch.get('href')
            if a.startswith('https'):
                links.append(a)
            elif a.startswith('#'):
                pass
            else:
                links.append('https://interface.ai' + a)
        return links

    def func2(self):
        assets = []
        results = self.soup.find_all('img', src=True)
        for img in results:
            a = img.get('src')
            end = ("jpg", "svg", "png")
            if a.endswith(end):
                if a.startswith('https'):
                    assets.append(a)
                else:
                    assets.append('https://interface.ai' + a)
            else:
                pass
        return assets

def getWebsiteAssets(url):
    obj = Main()
    obj.fetch(url)
    links = obj.func1()
    assets = obj.func2()
    myset = set(links)
    

    for i in myset:
        obj.fetch(i)
        assets = obj.func2()
        for i in assets:
            link = i.strip()
            try:
                r = requests.get(link, allow_redirects=True)
                name = link.rsplit('/', 1)[1]
                # print(name)
                open('images/' + name, 'wb').write(r.content)
                
            except Exception as inst:
                print(inst)
                print('  Encountered unknown error. Continuing.')
        file = open("image_info.list", "a")
        file.write(str(assets))
        file.close()
        

getWebsiteAssets('https://interface.ai')




