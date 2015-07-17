import numpy as np
import os, urllib, csv,time

class DataReader:
    
    def __init__(self,csvfile):
        
        self.csvfile = csvfile
        self.regressionscore=[]
        self.image_url=[]
        self.downloadfolder='datasets'
        self.labelstxt='labels.txt'

        if not os.path.exists(os.path.join(os.getcwd(), self.downloadfolder)):
            os.mkdir(os.path.join(os.getcwd(), self.downloadfolder))
             
    def csvReader(self):
        with open(self.csvfile, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for r in reader:
                imageurl = r[0]
                imagename = r[0].split('/')[-1]
                score = r[1]
                self.regressionscore.append(score)
                self.labelsTxtCreator(imagename,score)
                self.image_url.append(imageurl)
                
    def labelsTxtCreator(self,img_name,img_label):
        f=open(self.labelstxt,'a')
        txttowrite=img_name+','+img_label+'\n'
        f.write(txttowrite)
        f.close()
        
    def imgDownloader(self):
        img_count = len(self.image_url) 
        i=0
        while i < img_count:
            try:
                img_name = self.image_url[i].split('/')[-1]
                urllib.urlretrieve (self.image_url[i], os.path.join(os.getcwd(),self.downloadfolder,img_name))
                print i,' th image downloaded'
                i+=1
            except IOError:
                print 'error on' + i + 'th image'
        
    def calculateAverageScore(self):
        np_array = np.array(self.regressionscore).astype('float')
        return np.mean(np_array)
        