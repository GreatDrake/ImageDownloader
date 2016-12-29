from PyQt5.QtCore import QThread, pyqtSignal
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import shutil

class Downloader(QThread):
    finished = pyqtSignal(int)
    error = pyqtSignal()
    
    def __init__(self, text):
        super().__init__()
        self.text = text
    
    def run(self):
        url = self.text
       
        try:
            html = urlopen(url)
            bsObj = BeautifulSoup(html, 'html.parser')
            images = bsObj.findAll("img") 
        except Exception:
            self.error.emit()
            return
        
        if not ('images' in os.listdir(os.getcwd())):
            os.mkdir('images')
        else:
            shutil.rmtree('images')
            os.mkdir('images')

        c = 0
        for image in images:
            pth = self.getCorrectPath(image, url)
            c += 1
            try:
                with urlopen(pth) as f:
                    im = f.read()
                    if im:
                        with open(os.path.join('images', str(c))+ '.png', 'wb') as img:
                            img.write(im)
                    else:
                        c -= 1
            except Exception:
                c -= 1
                
        self.finished.emit(c)
            
    def getCorrectPath(self, image, url):
        if 'http' in image.attrs['src']:
            return image.attrs['src']
        else:
            return urljoin(url, image.attrs['src'])
        
        
        
        
