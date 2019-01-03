from selenium import webdriver      # pip install selenium
from bs4 import BeautifulSoup       # pip install bs4
import pymysql      # pip install pymysql
from datetime import datetime       # 현재 날짜 가져오기 위한 import
from tkinter import *
from tkinter import Tk
import viewtrend        # 시청자 꺾은선 그래프
import afreecaratio      # 시청자 비율 막대그래
import platformratio    # 플랫폼 별 시청자 수 

btn_text=[]
btn_tric=[]
afreeca_result = []
kakao_result = []
a_test = []
k_test = []
t_test = []

# 아프리카 모듈
def afreeca() :
    global afreeca_result
    # 리스트 초기화
    a_subject, a_bjname = [], []
    url= "http://www.afreecatv.com/"
    driver = webdriver.Chrome("./chromedriver.exe")      # chromedriver경로 입력

    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    subject = soup.find("div", {"class":"onAir"}).find_all("span", {"class":"subject"})     # 방송 제목
    totalviewer = soup.find("div", {"class":"onAir"}).find_all("span", {"class":"viewer"})      # 총 시청자 수
    bjname = soup.find("div", {"class":"onAir"}).find_all("a", {"class":"nick"})        # bj 이름
    temp = soup.find("div", {"class":"onAir"}).find_all("span", {"class":"count"})      # 임시 (pc/모바일 시청자수)

    for a in subject :
        a_subject.append(a.text)
    for a in bjname :
        a_bjname.append(a.text)

    a_totalviewer, a_pcviewer, a_mobileviewer  = [''] * len(a_subject), [''] * len(a_subject), [''] * len(a_subject)
  
    for i in range(len(a_subject)) :
        #  숫자 분리하는 더러운 방법
        tempstr = str(temp[i])      # pc와 모바일 시청자 수 분리 (0,000  / 0,000)
        a = tempstr.split("</em>")
        aa = a[1].split("<")
        bb = a[2].split("<")
        
        t = totalviewer[i].text.split(" 명")     # 총 시청자 수 (0,000)

        # 콤마(,) 분리
        temp1 = aa[0].split(",")    # pc 시청자 수
        temp2 = bb[0].split(",")    # 모바일 시청자 수
        temp3 = t[0].split(",")     # 총 시청자 

        for y in temp1 :
            a_pcviewer[i] = a_pcviewer[i] + y
        for y in temp2 :
            a_mobileviewer[i] = a_mobileviewer[i] + y
        for y in temp3 :
            a_totalviewer[i] = a_totalviewer[i] + y

        # 리스트에 추가 (방송이름, bj, 총시청자수, pc, 모바일)
        afreeca_result.append([subject[i].text,bjname[i].text,int(a_totalviewer[i]), int(a_pcviewer[i]), int(a_mobileviewer[i])])
    
def kakao() :
    global kakao_result
    
    url= "https://tv.kakao.com/live"
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    result_subject,result_pd,result_view = [] ,[], []

    subjects = soup.find("ul",{"class":"list_vertical view_all"}).find_all("strong",{"class":"tit_item"}) # 카카오 방송 제목
    pds = soup.find("ul",{"class":"list_vertical view_all"}).find_all("span",{"class":"txt_item"}) # 카카오 PD 목록
    view = soup.find("ul",{"class":"list_vertical view_all"}).find_all("span",{"class":"mark_play"}) # 작은 상자 시청자 수
    c_view = soup.find("ul",{"class":"list_vertical view_all"}).find_all("span",{"class":"info_append"}) # 큰 상자 2개 시청자 수

    # result_subject 배열에 방제목 추가
    for s in subjects:
         result_subject.append(s.text.strip())

    # result_pd 배열에 PD명 추가
    for p in pds:
         temp = p.text.split(':')
         result_pd.append(temp[1].strip())
         
    # 기존 view_list에 view 배열을 합친다.
    view_list = [ c_view[0],c_view[2] ]    
    view_list.extend(view) 

    # 숫자로만 필터링 
    for v in view_list:
         temp = v.text.split(':')
         temp1 = temp[1].strip()
         temp2 = temp1.split(',')
         temp3 = ''
         
         for i in temp2:
              temp3 = temp3 + i
              
         result_view.append(int(temp3))

    # 배열 정렬 (카카오tv홈페이지 배치때문에 배열0,1번째에 순위와 관련없이 추천방송2개가 들어있음)    
    a = result_view[0]
    b = result_view[1]

    # reverse=True 내림차순 정렬 ( 높은수부터 낮은수로 )
    result_view.sort(reverse=True)
    
    index_a = result_view.index(a)
    index_b = result_view.index(b)
    
    
    s_a = result_subject[0]
    s_b = result_subject[1]
    result_subject.remove(s_a)
    result_subject.remove(s_b) 
    
    p_a = result_pd[0]
    p_b = result_pd[1]
    result_pd.remove(p_a)
    result_pd.remove(p_b)

    # a,b 크기 비교에 따라 배열삽입에 영향이 있으므로 조건에 따라 바꿔서 배열 삽입
    if a > b:
         result_subject.insert(index_a,s_a)
         result_subject.insert(index_b,s_b)
         result_pd.insert(index_a,p_a)
         result_pd.insert(index_b,p_b)
    else:
         result_subject.insert(index_b,s_b)
         result_subject.insert(index_a,s_a)
         result_pd.insert(index_b,p_b)
         result_pd.insert(index_a,p_a)

    # 전역 배열변수 kakao_result에 배열을 추가
    for i in range(len(result_subject)):
        kakao_result.append( [result_subject[i],result_pd[i],result_view[i]] )

def insertDB(afreeca_result, kakao_result) :
    time = datetime.today().strftime("%Y-%m-%d-%H:%M")
    # MySQL Connection 연결
    conn = pymysql.connect(host='HOST', user= \
        'USER', password='PWD', db='DBNAME', \
                           charset='utf8')
    try :
        # Connection 으로부터 Cursor 생성
        curs = conn.cursor()
        # 쿼리문 작성
        sql1 = "insert into reportPython_afreeca (a_subject, a_bjname, a_totalViewer, a_pcViewer, a_mobileViewer, a_date) values (%s, %s, %s,%s, %s, %s)"    # 항상 %s 로
        for a in range(len(afreeca_result)) :
            curs.execute(sql1, (afreeca_result[a][0], afreeca_result[a][1], int(afreeca_result[a][2]), int(afreeca_result[a][3]), int(afreeca_result[a][4]), time))

        curs.execute("ALTER TABLE reportPython_afreeca AUTO_INCREMENT=1")
        curs.execute("SET @COUNT = 0")
        curs.execute("UPDATE reportPython_afreeca SET reportPython_afreeca.a_id = @COUNT:=@COUNT+1")

        # 쿼리문 작성
        sql2 = "insert into reportPython_kakao (k_subject, k_bjname, k_totalViewer, k_date) values (%s, %s, %s, %s)"     # 항상 %s 로
        for a in range(len(kakao_result)) :
            curs.execute(sql2, (kakao_result[a][0], kakao_result[a][1], int(kakao_result[a][2]), time))

        curs.execute("ALTER TABLE reportPython_kakao AUTO_INCREMENT=1")
        curs.execute("SET @COUNT = 0")
        curs.execute("UPDATE reportPython_kakao SET reportPython_kakao.k_id = @COUNT:=@COUNT+1")
            
        conn.commit()
        
    finally :
        conn.close()
    
def inputLabel(data, area, btn):
    for i in range (0, 12):
        Label(area).grid(row=2*i, column=1)
        Label(area).grid(row=2*i, column=2, columnspan=5)
        Label(area).grid(row=2*i+1, column=0)
        Label(area).grid(row=2*i+1, column=1)
        Label(area).grid(row=2*i+1, column=2, columnspan=3)
        Label(area).grid(row=2*i+1, column=5)
        Label(area).grid(row=2*i+1, column=6)
        Label(area).grid(row=2*i+1, column=7)
    temp_row = 0
    temp_var = 0
    for i in data:
        Label(area, text=str(temp_row+1)+"위", relief="groove").grid(row=2*temp_row, column=1, sticky='NSEW')
        Label(area, text=i[0], anchor="nw", width="1", relief="groove").grid(row=2*temp_row, column=2, columnspan=5, sticky='NSEW')
        Label(area, text="이름", relief="groove").grid(row=2*temp_row+1, column=1, sticky='NSEW')
        Label(area, text=i[1], anchor="nw", width="1", relief="groove").grid(row=2*temp_row+1, column=2, columnspan=3, sticky='NSEW')
        Label(area, text="시청자수", relief="groove").grid(row=2*temp_row+1, column=5, sticky='NSEW')
        if btn == 0:
            Button(area, text=i[2], width=3, relief="groove").grid(row=2*temp_row+1, column=6, sticky='NSEW')
        else:
            btn_text.append(StringVar())
            btn_text[temp_var].set(i[2])
            createRamdaButton(area, btn_text[temp_var], temp_var, i[2], i[3], i[4], temp_row)
            btn_tric.append(0)
            temp_var += 1
        temp_row += 1

def createRamdaButton(area, text, temp, i, j, k, temp_row):
    Button(area, textvariable=text, width=3, command=lambda:changeBtnText(temp,i,j,k)).grid(row=2*temp_row+1, column=6, sticky='NSEW')
        
def changeBtnText(var, i, j, k):
    if btn_tric[var] == 0:
        btn_text[var].set(j + ', ' + k)
        btn_tric[var] = 1
    else:
        btn_text[var].set(i)
        btn_tric[var] = 0
        
def click(x):
    messagebox.showinfo("EVENT",x)

def main():
    
    afreeca()
    for i in range(len(afreeca_result)):
        print(afreeca_result[i])
    
    kakao()
    for i in range(len(kakao_result)):
        print(kakao_result[i])

    insertDB(afreeca_result, kakao_result)
    
    root = Tk()
    root.title("viewer by platform")
    root.geometry("1200x800")

    for i in range(12) :
        a_test.append([afreeca_result[i][0], afreeca_result[i][1], str(afreeca_result[i][2]), str(afreeca_result[i][3]), str(afreeca_result[i][4])])
        k_test.append([kakao_result[i][0], kakao_result[i][1], str(kakao_result[i][2])])

    #show_area
    show_area = Frame(root)
    show_area.pack(fill = BOTH, expand = YES)
    
    wall_afreeca = PhotoImage(file="afreecatv.png")
    wall_kakao = PhotoImage(file="kakaotv.png")
    
    Label(show_area, image = wall_afreeca).grid(row=0, column=0, sticky='NSEW')
    Label(show_area, image = wall_kakao).grid(row=0, column=1, sticky='NSEW')
    
    show_area.grid_columnconfigure(0,weight=1)
    show_area.grid_columnconfigure(1,weight=1)
    show_area.grid_rowconfigure(0,weight=1)

    #print_area (a_area, t_area, k_area)
    print_area = Frame(root)
    print_area.pack(fill = BOTH, expand = YES)
    print_area.grid_columnconfigure(0,weight=1)
    print_area.grid_columnconfigure(1,weight=1)
    a_area = Frame(print_area)
    a_area.grid(row=0, column=0, sticky='NSEW')
    k_area = Frame(print_area)
    k_area.grid(row=0, column=1, sticky='NSEW')

    inputLabel(a_test,a_area,1)
    inputLabel(k_test,k_area,0)
    for i in [a_area,k_area]:
        for j in range(0,8):
            i.grid_columnconfigure(j,weight=1)
    #button_area
    button_area = Frame(root)
    button_area.pack(fill = BOTH, expand = YES)

    Button(button_area, text='시간별 플랫폼 시청자 비율', width=25, bg='#ffffff', command=platformratio.bar).grid(row=0, column=0)
    button_area.grid_columnconfigure(0,weight=1)
    Button(button_area, text='시간에 따른 시청자 추이', width=25, bg='#ffffff', command=viewtrend.trend).grid(row=0, column=1)
    button_area.grid_columnconfigure(1,weight=1)
    Button(button_area, text='Afreeca TV BJ 시청자 비율 ', width=25, bg='#ffffff', command=afreecaratio.ratio).grid(row=0, column=2)
    button_area.grid_columnconfigure(2,weight=1)
    
    root.mainloop()
    
if __name__=="__main__":
    main()
else:
    exit(0)
