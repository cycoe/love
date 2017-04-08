import requests
import os

class Fetcher(object):

    def __init__(self):
        self.APIUrl = 'http://open.lovebizhi.com/baidu_rom.php'
        self.pathDict = {
            0: '.cache/samll/',
            1: '.cache/big/',
            2: '.cache/cover/',
            3: os.path.expanduser('~') + '/Wallpaper'
        }

    def formatParams(self, setType=1):
        params = {
            'width': self.width,
            'height': self.height,
            'type': setType,
        }
        return params

    def setImgSize(self, width, height):
        self.width = width
        self.height = height

    def getCateLib(self):
        response = requests.get(self.APIUrl, params=self.formatParams()).json()
        self.rankUrl = response['ranking']
        self.bannerUrl = response['banner']
        self.wallpaperUrl = response['wallpaper']
        self.recommendUrl = response['recommend']
        self.cateLib = response['category']
        return self.cateLib

    def fetchImgList(self, selectedCate):
        cateName = self.cateLib[selectedCate]['name']
        coverUrl = self.cateLib[selectedCate]['cover']
        cateUrl = self.cateLib[selectedCate]['url']
        response = requests.get(cateUrl).json()
        self.picList = response['data']

    def fetchImgCache(self, cateName, imgUrl, imgName, imgSize):
        catePath = self.pathDict[imgSize] + cateName
        imgPath = '/'.join([catePath, imgName]) + '.jpg'
        os.system('mkdir -p ' + catePath)
        imagebody = requests.get(imgUrl)
        with open(imgPath, 'wb') as fr:
            for chunk in imagebody:
                fr.write(chunk)
        return  imgPath

    def fetchRankImgList(self):
        response = requests.get(self.rankUrl).json()
        return response['data']


def main():
    fetcher = Fetcher()
    print(fetcher.getCateLib())


if __name__ == '__main__':
    main()
