import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pymysql
from matplotlib import font_manager, rc

def get(query) :
    conn = pymysql.connect(host='HOST', user= \
        'USER', password='PWD', db='DBNAME', \
                           charset='utf8')
    curs = conn.cursor() # 커서 생성
    sql = query # SQL문 작성
    curs.execute(sql) # SQL문 실행
    rows = curs.fetchall() # 데이터 불러온다
    conn.close()

    return rows

def ratio() :
    # 폰트 설정
    font_location = 'C:/WINDOWS/FONTS/NANUMGOTHIC.TTF'  
    font_manager.FontProperties(fname = font_location)
    rc('font', family = "NanumGothic")

    width = 0.2
    temp,pc, mobile, ratio = [], [], [], []
    # DB에서 가져온 결과 리스트에 저장
    a_data = get('select a_bjname, sum(a_mobileViewer), sum(a_pcViewer),'\
                 +'sum(a_mobileViewer)+sum(a_pcViewer) as a from reportPython_afreeca '\
                 +'group by a_bjname order by sum(a_totalViewer) desc limit 0,12')
    for i in a_data :   # 비율 계산 후 리스트에 추가
        temp.append(i[0])
        pc.append( round((float(i[1]) / float(i[3])*100),1) )
        mobile.append( round((float(i[2]) / float(i[3])*100),1) )

    plt.figure(figsize=(12,6))
    stand = np.arange(12)
    xyax = plt.axes()
    xyax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    xyax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    xyax.set_ylim(0,100)

    plt.grid(which='major', ls=':', linewidth='1', axis='y')
    plt.grid(which='minor', linewidth='0.5', axis='y')

    plt.ylabel("Rate", fontsize=12)

    plt.title("Afreeca TV Viewer Rate", fontsize=20, color="black")

    plt.bar(stand-0.1, pc, width, color="r", label="pc")
    plt.bar(stand+0.1, mobile, width, color="b", label="mobile")

    plt.xticks(stand, temp, fontsize=8, rotation=30)

    plt.legend(loc="upper right")
    plt.savefig("Ratio.png", format="png", dpi=300)
    plt.show()