#© 2023 MaJunYoung akwns615@gmail.com v17
import requests, os, re, time, pyautogui
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
from urllib import parse
from requests_html import HTMLSession
from datetime import datetime
from tkinter import * 
copy = '© 2023 MaJunYoung akwns615@gmail.com v17'
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

#로그 작성함수
def printt(log):
    if not isinstance(log, str):
        log = str(log)
    print(log)
    with open('./log/'+firsttime+'.txt', "a", encoding='utf-8', errors='ignore') as file:
        file.write(str(datetime.now())+' : '+log+'\n')

try:
    printt(copy)
    mailid = pyautogui.prompt(title='ID', text='아이디를 입력하세요', default='2000414@partner.skcc.com')
    mailpw = pyautogui.password(title='PW', text='비밀번호를 입력하세요')

    # 세션 생성
    session = requests.Session()

    #Requests-HTML 세션 생성
    session = HTMLSession()
    session2 = HTMLSession()
    # 버프 프록시용 세팅
    # session.proxies = {'http': 'http://127.0.0.1:8088', 'https': 'http://127.0.0.1:8088'}
    # session2.proxies = {'http': 'http://127.0.0.1:8088', 'https': 'http://127.0.0.1:8088'}

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

    #1. 로그인해서 쿠키 가져오기 ------------------------------------------>최종
    whilelogin = 0
    while whilelogin < 3000:
        printt('세션 생성(1/2)')
        res = makesession()
        printt(len(str(res.text)))
        time.sleep(5)
        printt('세션 생성(2/2)')
        res100 = makesession2()
        printt(len(str(res100.text)))
        if len(str(res.text)) > 1500 and len(str(res100.text)) > 3000:
            whilelogin = len(str(res.text))
        else:
            printt("에러01: 세션 생성을 실패하였습니다 3분후 재시도합니다.")
            time.sleep(180)

    #2. 쿠키값으로 로그인하기 ------------------------------------------>최종
    whilelogin2 = 0
    while whilelogin2 < 13000:
        url2 = "https://mail.partner.skcc.com/owa/"
        res2 = session.get(url2, verify = False)
        printt(len(str(res2.text)))    
        if len(str(res2.text)) > 13000:
            whilelogin2 = len(str(res2.text))
        else:
            printt("에러02: 로그인에 실패하였습니다 3분후 재시도합니다.")
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
    while whilelogin3 < 13000:
        url3 = "https://mail.partner.skcc.com/owa/"+Noteid
        datas3 = {'hidpid':'MessageView','hidcanary':hidcanary, 'hidactbrfld':'1'}
        res3 = session.post(url3, data=datas3, cookies=cookies2, verify = False)
        printt(len(str(res3.text)))
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
        vari2.append(value)
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



    for i in soup2result:    
        foldername = re.sub(r'[\/:*?"<>|]', '', i['title']) # 특수문자 제거된 폴더명을 변수에 할당
        lb.insert(END, str(foldername))
        
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

    for i in soup2result :    
        foldername = re.sub(r'[\/:*?"<>|]', '', i['title']) # 특수문자 제거된 폴더명을 변수에 할당
        foldername = truncate_string(foldername)
        if foldername in vari2:  #--------------------------------------------------------------vari2로 선택한 폴더만 저장
            printt('-----------------'+i['title']) #폴더명 프린트찍기 12-13
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
            chkmsg = soup3.find_all('input',{'name':'chkmsg'}) #메일 RUL 파싱
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
                sub = soup4.find('td',{'class':'sub'}).get_text() # 제목 추출
                sub3 = ''.join(char for char in sub if char.isalnum() or char in (' ', '_', '-', '[', ']'))
                times = soup4.find('td',{'class':'hdtxnr'}).get_text() #시간 추출 ( 파일명 및 메일명에 사용 )
                time2 = ''.join(char for char in times if char.isalnum() or char in (' ', '_', '-'))
                htmlhtml = ''
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
                    htmlhtml += str(soup5)
                    with open('./'+foldername+'/['+time2+']__'+sub3+".html", "w", encoding='utf-8', errors='ignore') as file:
                        file.write(htmlhtml)
                except:
                    printt('에러발생'+url4)
                printt('저장완료:'+time2+'__'+sub3+".html")
    printt('백업완료')
    pyautogui.alert('백업이 완료되었습니다!')
except Exception as e:
    # 예외가 발생했을 때 처리
    error_message = f"Exception: {str(e)}"

    # 에러 메시지를 파일에 저장
    with open('./log/'+firsttime+'.txt', "a", encoding='utf-8', errors='ignore') as file:
        file.write(error_message + "\n") 

