#© 2023 MaJunYoung akwns615@gmail.com v10
import requests, json, os, re, time, pyautogui
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
from urllib import parse
from requests_html import HTMLSession
from datetime import datetime
#RequestsCookieJar는 dict 처럼 작동
#2000414@partner.skcc.com
#2300091
mailid = pyautogui.prompt(title='ID', text='아이디를 입력하세요', default='2000414@partner.skcc.com')
mailpw = pyautogui.password(title='PW', text='비밀번호를 입력하세요')

# 세션 생성
session = requests.Session()

#폴더 생성 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

#Requests-HTML 세션 생성
session = HTMLSession()

#세션 재 생성 함수
def makesession():
    url = "https://mail.partner.skcc.com/owa/auth.owa"
    datas = {'destination':'https://mail.partner.skcc.com/owa/','flags':'1','forcedownlevel':'0','trusted':'0','username':mailid,'password':mailpw,'isUtf8':'1'}
    cookies = {'OutlookSession':'b1a7d7bd6ef645549c4a633c2f0c3adb','PBack':'0'}
    res = session.post(url, data=datas, cookies=cookies, verify = False)
    return res

#1. 로그인해서 쿠키 가져오기 ------------------------------------------>최종
whilelogin = 0
while whilelogin < 20000:
    res = makesession()
    print(len(str(res.text)))
    if len(str(res.text)) > 20000:
        whilelogin = len(str(res.text))
    else:
        print("에러01: 로그인에 실패하였습니다 3분후 재시도합니다.")
        print(str(res.text))
        time.sleep(180)

#2. 쿠키값으로 로그인하기 ------------------------------------------>최종
whilelogin2 = 0
while whilelogin2 < 20000:
    url2 = "https://mail.partner.skcc.com/owa/"
    res2 = session.get(url2, verify = False)
    print(len(str(res2.text)))    
    if len(str(res2.text)) > 20000:
        whilelogin2 = len(str(res2.text))
    else:
        print("에러02: 로그인에 실패하였습니다 3분후 재시도합니다.")
        time.sleep(180)
        res = makesession()

#3. 로그인 후 나온 response에서 히든까나리 찾기
soup = BeautifulSoup(res2.content,"html.parser")
result = soup.find_all(attrs={'name':'hidcanary'})
hidcanary = result[0]['value'] # 히든 까나리 저장 ------------------------------> 로그인에 실패하였습니다. 잠시 후 다시 시도해주세요 (여기에서 오류가 자주 발생하니 try catch 하는게 좋을듯)
Noteid = soup.find(attrs={'name':'lnkFldr'})['href']

#4. 쿠키에 히든 까나리 추가
cookies2 = session.cookies.get_dict()
cookies2['UserContext'] = hidcanary

#4. post 히든까나리 추가해서 보내기 -> 메일 폴더 list 크롤링
whilelogin3 = 0
while whilelogin3 < 20000:
    url3 = "https://mail.partner.skcc.com/owa/"+Noteid
    datas3 = {'hidpid':'MessageView','hidcanary':hidcanary, 'hidactbrfld':'1'}
    res3 = session.post(url3, data=datas3, cookies=cookies2, verify = False)
    print(len(str(res3.text)))
    if len(str(res3.text)) > 20000:
        whilelogin3 = len(str(res3.text))
    else:
        print("에러03: 로그인에 실패하였습니다 3분후 재시도합니다.")
        time.sleep(180)
        res = makesession()
        
#5. res3에서 title 파싱
soup2 = BeautifulSoup(res3.content,"html.parser")
soup2result = soup2.select('select > option[title]')
errormemo = '에러 항목'+str(datetime.now())+'\n'
for i in soup2result :    
    foldername = re.sub(r'[\/:*?"<>|]', '', i['title']) # 특수문자 제거된 폴더명을 변수에 할당
    if foldername not in ('받은 편지함', '보낸 편지함', '보낼 편지함', '임시 보관함', '작업', '저널', '정크 메일', '지운 편지함', '메모'):  #--------------------------------저장이 필요없는 폴더는 제외 ( 특히 정크메일에서 오류가 발생, length 문제로 추정 )
        print('-----------------',i['title']) #폴더명 프린트찍기 12-13
        makedirs(foldername+'/img') # 특수문자 제거된 이름으로 폴더 생성
        makedirs(foldername+'/file') # 특수문자 제거된 이름으로 폴더 생성
        folderurl = 'https://mail.partner.skcc.com/owa/?ae=Folder&t='+i['value']+'&slUsng=1'
        #폴더 안에 들어가기 요청
        whileinfolder = 0
        while whileinfolder < 20000:
            folderres = session.get(folderurl, verify = False) #폴더 안에 들어가기 요청
            if len(str(folderres.text)) > 20000:
                whileinfolder = len(str(folderres.text))
            else:
                print("에러04: 로그인에 실패하였습니다 3분후 재시도합니다.")
                print(str(folderres.text))
                time.sleep(180)
                res = makesession()
        soup3 = BeautifulSoup(folderres.text,"html.parser")
        chkmsg = soup3.find_all('input',{'name':'chkmsg'}) #메일 RUL 파싱
        imgcount = 0 #이미지 저장할때 번호 할당용 변수
        for j in chkmsg:
            uri = parse.quote(j['value'])
            url4 = 'https://mail.partner.skcc.com/owa/?ae=Item&t=IPM.Note&id='+uri
            whileemail = 0
            while whileemail < 20000: #------------------------------------------------------------------------------->메일 들어가는 req까지 length 처리 완료
                res4 = session.get(url4, verify = False)
                if len(str(res4.text)) > 20000:
                    whileemail = len(str(res4.text))
                else:
                    print("에러04: 로그인에 실패하였습니다 3분후 재시도합니다.")
                    print(len(str(res4.text)))
                    time.sleep(180)
                    res = makesession()
            soup4 = BeautifulSoup(res4.content,"html.parser")
            img = soup4.find('td',{'class':'cntnttp'}).select('table > tr')[2].select('img')
            file = soup4.find_all('a',{'id':'lnkAtmt'})
            html = '© 2023 MaJunYoung akwns615@gmail.com v10<hr><br>'
            if file:
                for f in file:
                    filename = f['title']
                    filename = ''.join(char for char in filename if char.isalnum() or char in (' ', '_', '-', '.'))
                    fileurl = 'https://mail.partner.skcc.com/owa/'+f['href']
                    resfile = session.get(fileurl, verify = False)
                    html += '첨부파일 : '+'<a href="file/'+filename+'">'+filename+'</a><br>'
                    with open('./'+foldername+'/file/'+filename, "wb") as file:
                        file.write(resfile.content)     
            #이미지 저장 및 경로 수정
            for k in img:
                imgcount += 1
                if 'src' in k.attrs:
                    imgurl = 'https://mail.partner.skcc.com/owa/'+k['src']
                    resimg = session.get(imgurl, verify = False)
                    with open('./'+foldername+'/'+'img/'+foldername+str(imgcount)+".png", "wb") as file:
                        file.write(resimg.content)
                    #print('     사진저장:'+k['src']) #---------------------------------------23년12월11일 주석
                    k['src'] = 'img/'+foldername+str(imgcount)+".png"
                    #sub = soup4.find('td',{'class':'sub'}).get_text() # 사진 제목 설정을 위한 메일 제목 파싱 -----------------------------없어도 될꺼같은데 12-13
                    
            # 메일 내용 저장 시작
            content_td = soup4.find('td', {'class': 'cntnttp'})
            if content_td:
                tr_elements = content_td.select('table > tr')
                
                # 필요한 데이터 추출
                if len(tr_elements) > 2:
                    try:
                        html += str(tr_elements[2])
                    except:
                        print(url4)
                        errormemo += url4+'\n' #-------------------------------------------------->에러항목 저장
                    sub = soup4.find('td',{'class':'sub'}).get_text() # 제목 추출
                    sub3 = ''.join(char for char in sub if char.isalnum() or char in (' ', '_', '-'))
                    times = soup4.find('td',{'class':'hdtxnr'}).get_text() #시간 추출
                    time2 = ''.join(char for char in times if char.isalnum() or char in (' ', '_', '-'))
                    with open('./'+foldername+'/'+time2+'__'+sub3+".html", "w", encoding='utf-8', errors='ignore') as file:
                        file.write(html)
                    
                    print('저장완료:',time2+'__'+sub3+".html")
                else:
                    print("데이터가 충분하지 않습니다.")
            else:
                print("요소를 찾을 수 없습니다.")
session.close()
with open('./error.txt', "a", encoding='utf-8', errors='ignore') as file:
    file.write(errormemo)
print('백업완료')
pyautogui.alert('백업이 완료되었습니다!')
 

