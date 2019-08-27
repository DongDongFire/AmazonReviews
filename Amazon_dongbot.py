from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import re
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

__all__=['Amazon_dongbot']


options = Options()
os.chdir('D:/download')


options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
options.add_argument("disable-gpu")
driver=wd.Chrome(executable_path = 'C:/chromedriver.exe',options=options)

class Amazon_dongbot:
    
    options = Options()
    os.chdir('D:/download')


    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("disable-gpu")
    driver=wd.Chrome(executable_path = 'C:/chromedriver.exe',options=options)
    
    def dongbot(asin):
        url='https://www.amazon.com/LG-Electronics-SIGNATURE-OLED77G7P-77-Inch/product-reviews/{}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'.format(asin)

        
        driver.get(url)
        driver.implicitly_wait(10)
        res=driver.page_source
        html=BeautifulSoup(res,'html.parser')
        total_reviews=int(html.find('span',{'class':'a-size-medium totalReviewCount'}).text)
        names=html.find('a',{'data-hook':'product-link'}).text

        date=[]
        model=[]
        rating=[]
        title=[]
        body=[]

        while len(date) < total_reviews:

            source=driver.page_source
            bs_obj=BeautifulSoup(source,"html.parser")


            date_list=bs_obj.findAll('span',{'data-hook':'review-date'})
            for i in date_list:
                date.append(i.text)

            model_list=bs_obj.findAll('a',{'data-hook':'format-strip'})
            for o in model_list:
                model.append(o.text)

            rating_list=bs_obj.findAll('i',{'data-hook':'review-star-rating'})
            for k in rating_list:
                rating.append(int(k.text.split(' ')[0][0]))

            title_list=bs_obj.findAll("a",{'data-hook':'review-title'})
            for m in title_list:
                title.append(m.text)

            body_list=bs_obj.findAll('span',{'data-hook':'review-body'})
            for n in body_list:
                body.append(n.text)

            
            if 'a-disabled a-last' in bs_obj:
                driver.quit()
                driver.close()
                break;
            else:
                driver.find_element_by_class_name('a-last').click()
            
                WebDriverWait(driver, 35).until(
                        # 지정한 한개 요소가 올라면 웨이트 종료
                    EC.presence_of_element_located( (By.CLASS_NAME, 'a-last'))
                )
                time.sleep(3)
            

     
            

        df=pd.DataFrame({'Date':date,'Rating':rating,"Model":model,"TItle":title,"Body":body})
        df['Int_date']=pd.to_datetime(df['Date'],format='%B %d, %Y')
        df['Month']=df['Int_date'].dt.month
        df['Year']=df['Int_date'].dt.year

        
        #파일 이름 설정
        #writer=pd.ExcelWriter('Amazon %s test.xlsx'%names[:10],engine='xlsxwriter')
        #df.to_excel(writer, sheet_name='Raw')

        #writer.save()

        return df
