import requests, json, os, re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
from urllib import parse
from requests_html import HTMLSession
#RequestsCookieJar는 dict 처럼 작동

#global 변수들

#폴더 생성 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

#Requests-HTML 세션 생성
session = HTMLSession()

#for문 함수화
def forfor(j,imgcount,cookies2):
    uri = parse.quote(j['value'])
    url4 = 'https://mail.partner.skcc.com/owa/?ae=Item&t=IPM.Note&id='+uri
    res4 = requests.get(url4, cookies=cookies2, verify = False)
    soup4 = BeautifulSoup(res4.content,"html.parser")
    def errcon1():
        global img
        try:
            img = soup4.find('td',{'class':'cntnttp'}).select('table > tr')[2].select('img')
        except:
            cookies2, soup2result = login()
            errcon1()
    errcon1()
    
    
    #이미지 저장 및 경로 수정
    for k in img:
        imgcount += 1
        if 'src' in k.attrs:
            imgurl = 'https://mail.partner.skcc.com/owa/'+k['src']
            resimg = requests.get(imgurl, cookies=cookies2, verify = False)
            with open('./'+foldername+'/'+'img/'+foldername+str(imgcount)+".png", "wb") as file:
                file.write(resimg.content)
            print('     사진저장:'+k['src'])
            k['src'] = 'img/'+foldername+str(imgcount)+".png"
            sub = soup4.find('td',{'class':'sub'}).get_text() # 사진 제목 설정을 위한 메일 제목 파싱
    html = str(soup4.find('td',{'class':'cntnttp'}).select('table > tr')[2])
    #html = str(soup4.select('table>tbody>tbody'))
    sub = soup4.find('td',{'class':'sub'}).get_text() # 제목 추출 에러처리 필요
    sub3 = ''.join(char for char in sub if char.isalnum() or char in (' ', '_', '-'))
    time = soup4.find('td',{'class':'hdtxnr'}).get_text() #시간 추출 에러처리 필요
    time2 = ''.join(char for char in time if char.isalnum() or char in (' ', '_', '-'))
    with open('./'+foldername+'/'+time2+'__'+sub3+".html", "w", encoding='utf-8') as file:
        file.write(html)
    print(time2,sub3) #시간 제목출력
    

#1. 로그인해서 쿠키 가져오기
def login():
    url = "https://mail.partner.skcc.com/owa/auth.owa"
    datas = {'destination':'https://mail.partner.skcc.com/owa/','flags':'1','forcedownlevel':'0','trusted':'0','username':'2300091@partner.skcc.com','password':'Akwnsdud1!','isUtf8':'1'}
    cookies = {'OutlookSession':'b1a7d7bd6ef645549c4a633c2f0c3adb','PBack':'0'}
    res = requests.post(url, data=datas, cookies=cookies, verify = False, allow_redirects=False)
    #쿠키 저장
    logcookie = res.cookies
    
        #2. 쿠키값으로 로그인하기 
    url2 = "https://mail.partner.skcc.com/owa/"
    cookies2 = res.cookies
    res2 = requests.get(url2, cookies=cookies2, verify = False)
    #print(res2.text) #-------------------------------------------------> 일단 오류뜨면 여기서부터 오류페이지로뜸

    #BeautifulSoup으로 input태그중 name=hidcanary값 가져오기
    soup = BeautifulSoup(res2.content,"html.parser")
    result = soup.find_all(attrs={'name':'hidcanary'})
    try:
        hidcanary = result[0]['value'] # 히든 까나리 저장 ------------------------------> 로그인에 실패하였습니다. 잠시 후 다시 시도해주세요 (여기에서 오류가 자주 발생하니 try catch 하는게 좋을듯)
    except:
        login()

    #쿠키에 히든 까나리 추가
    cookies2['UserContext'] = hidcanary
    #쿠키에 잡다한 내용들 추가 ( 식제해도 작동 할거같음 )
    cookies2['OutlookSession'] = 'c24f51d13b194a28a85b268691ea9fc1'
    cookies2['PBack'] = '0' 
    cookies2['tzid'] = 'Korea Standard Time' 
    cookies2['owacsdc'] = '1'
    
    #3. post로 보내기
    url3 = "https://mail.partner.skcc.com/owa/?ae=StartPage&id=LgAAAADt174hy3kJR6AvN63aPJFKAQDbaie4P2xxSKlViirAstGGAAAARAmCAAAB&slUsng=0&pg=1"
    datas3 = {'hidpid':'MessageView','hidcanary':hidcanary, 'hidactbrfld':'1'}
    res3 = requests.post(url3, data=datas3, cookies=cookies2, verify = False)
    
    #4. soup
    soup2 = BeautifulSoup(res3.content,"html.parser")
    soup2result = soup2.select('select > option[title]')
    return cookies2, soup2result

cookies2, soup2result = login()
for i in soup2result :
    print('-----------------',i['title'])
    foldername = re.sub(r'[\/:*?"<>|]', '', i['title'])
    makedirs(foldername+'/img')
    folderurl = 'https://mail.partner.skcc.com/owa/?ae=Folder&t='+i['value']+'&slUsng=1'
    folderres = requests.get(folderurl, cookies=cookies2, verify = False)
    soup3 = BeautifulSoup(folderres.text,"html.parser")
    chkmsg = soup3.find_all('input',{'name':'chkmsg'})
    imgcount = 0
    for list in chkmsg:
        forfor(list,imgcount,cookies2)

        
 

