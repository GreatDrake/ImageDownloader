from PyQt5.QtCore import QThread, pyqtSignal
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin
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
        
        path = self.text
       
        try:
            parsed_uri = urlparse(path)
            self.protocol = parsed_uri.scheme
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        except Exception:
            self.error.emit()
            return
        try:
            html = urlopen(path)
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

        i = 0
        for image in images:
            try:
                pth = self.getCorrectPath(image, path, domain)
            except Exception:
                self.error.emit()
                return
            try:
                i += 1
                with urlopen(pth) as f:
                    im = f.read()
                    if im:
                        with open(os.path.join('images', str(i))+ '.png', 'wb') as img:
                            img.write(im)
                    else:
                        i -= 1
            except Exception:
                i -= 1
        self.finished.emit(i)
            
    def getCorrectPath(self, image, path, domain):
        if '..' in image['src']:
            path2 = os.path.dirname(path) + image['src']
            i2 = path2.find('..')
            i1 = path2.rindex('/', 0, i2)
            return path2[0:i1] + path2[i2+2:]
        elif 'http' in image['src']:
            return image.attrs['src']
        else:
            return (domain + image.attrs['src'] if not image.attrs['src'][0:2] == '//' else self.protocol + ':' + image['src'])
