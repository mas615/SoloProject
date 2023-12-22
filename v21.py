#© 2023 MaJunYoung akwns615@gmail.com v21
import requests, os, re, time, pyautogui
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
from urllib import parse
from requests_html import HTMLSession
from datetime import datetime
from tkinter import * 
from datetime import datetime
copy = '© 2023 MaJunYoung akwns615@gmail.com v21'
#RequestsCookieJar는 dict 처럼 작동
#2000414@partner.skcc.com
#2300091@partner.skcc.com

#폴더 생성 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
#로그폴더 생성
makedirs('log')
firsttime = str(datetime.now())
firsttime = ''.join(char for char in firsttime if char.isalnum() or char in (' ', '_', '-', '.'))
with open('./log/'+firsttime+'.txt', "a", encoding='utf-8', errors='ignore') as file:
        file.write(firsttime+'\n')
        
#Backup폴더 생성
makedirs('backup')

#시간변환함수
def convert_date_string(input_string):
    # 한글을 제거하고 시간 문자열을 datetime 객체로 파싱
    cleaned_string = input_string.replace("년 ", "-").replace("월 ", "-").replace("일 ", "").replace("오전", "AM").replace("오후", "PM")

    # 요일 한글을 영문으로 변환
    for day_kor, day_eng in [("월요", "Monday"), ("화요", "Tuesday"), ("수요", "Wednesday"), ("목요", "Thursday"), ("금요", "Friday"), ("토요", "Saturday"), ("일요", "Sunday")]:
        cleaned_string = cleaned_string.replace(day_kor, day_eng)

    dt = datetime.strptime(cleaned_string, "%Y-%m-%d%A%p %I:%M")

    # 출력 형식으로 포맷팅
    output_string = dt.strftime("%y%m%d_%H%M")

    return output_string

#로그 작성함수
def printt(log):
    if not isinstance(log, str):
        log = str(log)
    print(log)
    with open('./log/'+firsttime+'.txt', "a", encoding='utf-8', errors='ignore') as file:
        file.write(str(datetime.now())+' : '+log+'\n')
        
#전체 에러 처리
try:
    printt(copy)
    #자동로그인 시작
    if not os.path.exists('./loginid.js'):
        mailid = pyautogui.prompt(title='ID', text='아이디를 입력하세요')        
    else:
        with open('./loginid.js', "r", encoding='utf-8', errors='ignore') as file:
            loginid = file.readlines()
        mailid = pyautogui.prompt(title='ID', text='아이디를 입력하세요', default=loginid)
        if mailid is not None:
            with open('./loginid.js', "w", encoding='utf-8', errors='ignore') as file:
                file.write(mailid)
        else:
            printt('ID입력 취소')
            sys.exit()
    mailpw = pyautogui.password(title='PW', text='비밀번호를 입력하세요')
    if mailpw is None:
        printt('PW입력 취소')
        sys.exit()

    # 세션 생성
    session = requests.Session()

    #Requests-HTML 세션 생성
    session = HTMLSession()
    session2 = HTMLSession()
    # 버프 프록시용 세팅
    # session.proxies = {'http': 'http://127.0.0.1:8088', 'https': 'http://127.0.0.1:8088'}
    # session2.proxies = {'http': 'http://127.0.0.1:8088', 'https': 'http://127.0.0.1:8088'}
    errors1 = ''
    #세션 생성 함수
    def makesession():
        url = "https://mail.partner.skcc.com/owa/auth.owa"
        datas = {'destination':'https://mail.partner.skcc.com/owa/','flags':'1','forcedownlevel':'0','trusted':'0','username':mailid,'password':mailpw,'isUtf8':'1'}
        cookies = {'OutlookSession':'b1a7d7bd6ef645549c4a633c2f0c3adb','PBack':'0'}
        res = session.post(url, data=datas, cookies=cookies, verify = False)
        return res
    def makesession2():
        url = "https://mail.partner.skcc.com/owa/auth.owa"
        datas = {'destination':'https://mail.partner.skcc.com/owa/','flags':'0','forcedownlevel':'0','trusted':'0','username':mailid,'password':mailpw,'isUtf8':'1'}
        cookies = {'OutlookSession':'b1a7d7bd6ef645549c4a633c2f0c3adb','PBack':'0'}
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36'}
        res = session2.post(url, data=datas, cookies=cookies, headers=headers, verify = False)
        return res
        
    #100자 이후로는 자르는 함수
    def truncate_string(input_string, max_length=100):
        if len(input_string) > max_length:
            truncated_string = input_string[:max_length]
            return truncated_string
        else:
            return input_string
    
    def truncate_string200(input_string, max_length=200):
        if len(input_string) > max_length:
            truncated_string = input_string[:max_length]
            return truncated_string
        else:
            return input_string

    #1. 로그인해서 쿠키 가져오기 ------------------------------------------>최종
    whilelogin = 0
    while whilelogin < 3000:
        printt('☆세션 생성(1/3)')
        res = makesession()
        printt('    packet length : '+str(len(res.text)))
        time.sleep(5)
        printt('☆세션 생성(2/3)')
        res100 = makesession2()
        printt('    packet length : '+str(len(res100.text)))
        if len(str(res.text)) > 1500 and len(str(res100.text)) > 3000:
            whilelogin = len(str(res.text))
        else:
            printt("에러01: 세션 생성을 실패하였습니다 3분후 재시도합니다.")
            time.sleep(180)

    
    #로그인 성공했으니 성공한 아이디 저장
    with open('./loginid.js', "w", encoding='utf-8', errors='ignore') as file:
            file.write(mailid)
            
    #2. 쿠키값으로 로그인하기 (session 사용으로 폐기)
    # whilelogin2 = 0
    # while whilelogin2 < 13000:
        # url2 = "https://mail.partner.skcc.com/owa/"
        # res2 = session.get(url2, verify = False)
        # printt(len(str(res2.text)))    
        # if len(str(res2.text)) > 13000:
            # whilelogin2 = len(str(res2.text))
        # else:
            # printt("에러02: 로그인에 실패하였습니다 3분후 재시도합니다.")
            # time.sleep(180)
            # res = makesession()

    #3. 로그인 후 나온 response에서 히든까나리 찾기
    soup = BeautifulSoup(res.content,"html.parser")
    result = soup.find_all(attrs={'name':'hidcanary'})
    hidcanary = result[0]['value'] # 히든 까나리 저장 ------------------------------> 로그인에 실패하였습니다. 잠시 후 다시 시도해주세요 (여기에서 오류가 자주 발생하니 try catch 하는게 좋을듯)
    Noteid = soup.find(attrs={'name':'lnkFldr'})['href']

    #4. 쿠키에 히든 까나리 추가
    cookies2 = session.cookies.get_dict()
    cookies2['UserContext'] = hidcanary

    #4. post 히든까나리 추가해서 보내기 -> 메일 폴더 list 크롤링
    whilelogin3 = 0
    while whilelogin3 < 13000:
        url3 = "https://mail.partner.skcc.com/owa/"+Noteid
        datas3 = {'hidpid':'MessageView','hidcanary':hidcanary, 'hidactbrfld':'1'}
        res3 = session.post(url3, data=datas3, cookies=cookies2, verify = False)
        printt('☆메일 폴더 리스트 추출(3/3)')
        printt('    packet length : '+str(len(res3.text)))
        if len(str(res3.text)) > 13000:
            whilelogin3 = len(str(res3.text))
        else:
            printt("에러03: 로그인에 실패하였습니다 3분후 재시도합니다.")
            time.sleep(180)
            res = makesession()
            
    #5. res3에서 title 파싱
    soup2 = BeautifulSoup(res3.content,"html.parser")
    soup2result = soup2.select('select > option[title]')


    #----------------------------------------------------------------------------------------GUI 선택창 시작
    vari2 = []
    def btnpress():
        global vari2
        value = lb.get(lb.curselection())
        vari2.append(items[value])
        text_widget.insert(END, value+'\n')
        printt(vari2)    

    #-------------------윈도우
    root = Tk()
    root.geometry("600x400")
    root.title("폴더선택")
    root.option_add("*Font", "맑은고딕 10")
    root.resizable(False, False)

    #카피라이트
    label = Label(root, text=copy)
    label.pack()

    #-------------프레임창
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=YES)

    lb = Listbox(frame, selectmode="browse", height=20)
    sb = Scrollbar(frame, orient=VERTICAL, command=lb.yview)
    lb.config(yscrollcommand=sb.set)

    items = {}

    for i in soup2result:    
        foldername1 = re.sub(r'[\/:*?"<>|]', '', i.get_text()) # 특수문자 제거된 폴더명을 변수에 할당
        foldername2 = re.sub(r'[\/:*?"<>|]', '', i['title'])
        items[foldername1] = foldername2
        lb.insert(END, str(foldername1))
        
    # Scrollbar를 Listbox에 붙이기
    lb.pack(side=LEFT, fill=BOTH, expand=YES)
    sb.pack(side=RIGHT, fill=Y)

    # 하위 프레임
    frame_bottom = Frame(root)
    frame_bottom.pack(fill=BOTH, expand=YES)

    #버튼
    btn = Button(frame_bottom, text="추가", width=10, command=lambda: btnpress())
    btn.pack(side=LEFT)
    btn2 = Button(frame_bottom, text="완료", width=10, command=lambda: root.destroy())
    btn2.pack(side=RIGHT)

    #텍스트창
    text_widget = Text(root, wrap=WORD, height=10)
    text_widget.pack()

    #엔터 눌러서 추가되게
    lb.bind("<Return>", lambda event: btnpress())


    root.mainloop()
    #-------------------------------------------------------------------------------------------------선택창 끝
    errorcount = 1
    lastname = ''
    lastnamecount = 1
    for i in soup2result :    
        foldername = re.sub(r'[\/:*?"<>|]', '', i['title']) # 특수문자 제거된 폴더명을 변수에 할당
        foldername = truncate_string(foldername)
        if foldername in vari2:  #--------------------------------------------------------------vari2로 선택한 폴더만 저장
            printt('-----------------'+i['title']) #폴더명 프린트찍기 12-13
            foldername = 'backup/'+foldername
            makedirs(foldername+'/img') # 특수문자 제거된 이름으로 폴더 생성
            makedirs(foldername+'/file') # 특수문자 제거된 이름으로 폴더 생성
            #lnkLstPg 폴더 페이지 최대수
            folderurl = 'https://mail.partner.skcc.com/owa/?ae=Folder&t='+i['value']+'&slUsng=1'
            #폴더 안에 들어가기 요청
            whileinfolder = 0
            while whileinfolder < 13000:
                folderres = session.get(folderurl, verify = False) #폴더 안에 들어가기 요청
                if len(str(folderres.text)) > 13000:
                    whileinfolder = len(str(folderres.text))
                else:
                    printt("에러04: 로그인에 실패하였습니다 3분후 재시도합니다.")
                    #print(str(folderres.text))
                    time.sleep(180)
                    res = makesession()
            soup3 = BeautifulSoup(folderres.text,"html.parser")
            maxpage = soup3.find('a',{'id':'lnkLstPg'})
            chkmsg = soup3.find_all('input',{'name':'chkmsg'}) #메일 RUL 파싱
            if maxpage is not None:
                maxpage = soup3.find('a',{'id':'lnkLstPg'})['onclick']
                maxpage = re.search(r'\d+', maxpage).group()
                maxpage = int(maxpage)
                printt("총 페이지 : "+str(maxpage))
                nowpage = int(2)
                while nowpage <= maxpage:
                    maxurl = folderurl+'&pg='+str(nowpage)
                    maxres = session.get(maxurl, verify = False)
                    maxsoup = BeautifulSoup(maxres.text,"html.parser")
                    chkmsg.extend(maxsoup.find_all('input',{'name':'chkmsg'})) #메일 RUL 파싱
                    nowpage += 1
            mailcount = 1
            for j in chkmsg:
                #이미지 및 파일용
                uri = parse.quote(j['value'])
                url4 = 'https://mail.partner.skcc.com/owa/?ae=Item&t=IPM.Note&id='+uri
                whileemail = 0
                while whileemail < 13000: #------------------------------------------------------------------------------->메일 들어가는 req까지 length 처리 완료
                    res4 = session.get(url4, verify = False)
                    if len(str(res4.text)) > 13000:
                        whileemail = len(str(res4.text))
                    else:
                        printt("에러04: 로그인에 실패하였습니다 3분후 재시도합니다.")
                        printt(len(str(res4.text)))
                        time.sleep(180)
                        res = makesession()
                #html 및 pdf용        
                urihtml = parse.quote(j['value'])
                urihtml2 = 'https://mail.partner.skcc.com/owa/?ae=Item&t=IPM.Note&a=Print&id='+urihtml
                whileemailhtml = 0
                reshtml = session2.get(urihtml2, verify = False)
                soup4 = BeautifulSoup(res4.content,"html.parser")
                soup5 = BeautifulSoup(reshtml.content,"html.parser")
                img = soup5.select('img')
                file = soup4.find_all('a',{'id':'lnkAtmt'})
                sub = soup5.find(class_='sub').get_text() # 제목 추출
                times = soup5.find(class_='hdtxnr').get_text() #시간 추출 ( 파일명 및 메일명에 사용 )
                sender = soup5.find(class_='frm').get_text() #보낸사람 추출 rwRRO
                sub3 = ''.join(char for char in sub if char.isalnum() or char in (' ', '_', '-', '[', ']'))
                time2 = ''.join(char for char in times if char.isalnum() or char in (' ', '_', '-', '[', ']', ':'))
                time2 = convert_date_string(time2)
                sender2 = ''.join(char for char in sender if char.isalnum() or char in (' ', '_', '-'))
                #htmlhtml = ''
                if file:
                    for f in file:
                        filename = f['title']
                        filename = ''.join(char for char in filename if char.isalnum() or char in (' ', '_', '-', '.', '[', ']'))
                        fileurl = 'https://mail.partner.skcc.com/owa/'+f['href']
                        resfile = session.get(fileurl, verify = False)
                        #htmlhtml = '첨부파일 : '+'<a href="file/'+filename+'">'+filename+'</a><br>'
                        with open('./'+foldername+'/file/'+'['+time2+']__'+filename, "wb") as file:
                            file.write(resfile.content)     
                #이미지 저장 및 경로 수정
                for k in img:
                    if 'src' in k.attrs:                    
                        imgurl = 'https://mail.partner.skcc.com/owa/'+k['src']
                        imgname = k['src']
                        imgname = ''.join(char for char in imgname if char.isalnum() or char in (' ', '_', '-', '.'))
                        imgname = imgname[-50:]
                        resimg = session.get(imgurl, verify = False)
                        with open('./'+foldername+'/'+'img/'+imgname+".png", "wb") as file:
                            file.write(resimg.content)
                        #print('     사진저장:'+k['src']) #---------------------------------------23년12월11일 주석
                        k['src'] = 'img/'+imgname+".png"
                        
                # 메일 내용 저장 시작
                try:
                    #진짜 메일 내용 저장
                    htmlhtml = str(soup5)
                    htmlpath = './'+foldername+'/['+time2+']_['+sender2+']_'+sub3
                    htmlpath = truncate_string200(htmlpath)
                    #이름 중복 체크
                    if lastname != htmlpath:                        
                        lastname = htmlpath
                    else:
                        htmlpath = htmlpath+'_중'+str(lastnamecount)
                        lastnamecount += 1
                    #저장
                    with open(htmlpath+".html", "w", encoding='utf-8', errors='ignore') as file:
                            file.write(htmlhtml)
                except Exception as e:
                    errors1 += str(errorcount)+'['+time2+']__['+sub3+'] : '+url4+'\n'
                    printt('    에러발생 url : '+url4)
                    printt('    에러내용 : '+str(e))
                    htmlpath = './'+foldername+'/[에러]_['+time2+']_['+sender2+']_'+sub3
                    htmlpath = truncate_string200(htmlpath)
                    #이름 중복 체크
                    if lastname != htmlpath:                        
                        lastname = htmlpath
                    else:
                        htmlpath = htmlpath+'_중'+str(lastnamecount)
                        lastnamecount += 1
                    errorhtml = reshtml.text
                    with open(htmlpath+".html", "w", encoding='utf-8', errors='ignore') as file:
                        file.write(errorhtml)
                    errorcount += 1
                printt('저장완료'+str(mailcount)+':'+time2+'__'+sub3+".html")
                mailcount += 1
    if errors1:
        printt('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼에러발생 모음( 파일,사진,메일 수동 저장 필요 )▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
        printt(errors1)
        pyautogui.alert('에러발생 항목이 있습니다 log파일 확인 후 수동 백업 필요')
    printt('백업완료')
    pyautogui.alert('백업이 완료되었습니다!')
except Exception as e:
    # 예외가 발생했을 때 처리
    error_message = f"Exception: {str(e)}"

    # 에러 메시지를 파일에 저장
    with open('./log/'+firsttime+'.txt', "a", encoding='utf-8', errors='ignore') as file:
        file.write(error_message + "\n") 

