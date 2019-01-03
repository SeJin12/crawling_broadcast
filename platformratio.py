import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pymysql
from matplotlib import font_manager, rc

def get(query):
     conn = pymysql.connect(host='HOST',user=\
                            'USER',password='PWD',db='DBNAME',\
                            charset='utf8')
     curs = conn.cursor() # 커서 생성
     sql = query # SQL문 작성
     curs.execute(sql) # SQL문 실행
     rows = curs.fetchall() # 데이터 불러온다
     conn.close()
     return rows


def bar():
     # 폰트 설정
     font_location = 'C:/WINDOWS/FONTS/NANUMGOTHIC.TTF'  
     font_manager.FontProperties(fname = font_location)
     rc('font', family = "NanumGothic")

     # DB에서 가져온 결과 리스트에 저장
     a_data = get('select a_date,sum(a_totalViewer) from reportPython_afreeca  group by a_date order by a_date desc limit 0,12')
     k_data = get('select k_date,sum(k_totalViewer) from reportPython_kakao group by k_date order by k_date desc limit 0,12')
     width = 0.4
     temp = [ a_data[i][0][5:] for i in range(len(a_data)) ] # x축 값 ( 년도를 뺀 )
     x = []
     for i in temp:
          x.append((i[:5]+'\n'+ i[6:]))

     total, afreeca, kakao = [], [], []
     for i in range(len(a_data)) :
          total.append(int(a_data[i][1]) +  int(k_data[i][1]))
          afreeca.append(  (int(a_data[i][1])/total[i])*100)
          kakao.append(  (int(k_data[i][1])/total[i])*100)


     print(str(afreeca[0]),' ',str(kakao[0]),' ' ,str(total[0]))
     stand = np.arange(len(x))

     plt.figure(figsize=(12,6))
     xyax = plt.axes()
     xyax.yaxis.set_major_locator(ticker.MultipleLocator(20))
     xyax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
     xyax.set_ylim(0,100)

     plt.grid(which='major',ls=':',linewidth='1',axis='y')
     plt.grid(which='minor',linewidth='0.5',axis='y')
     plt.ylabel('Viewer ( % )')
     plt.xlabel('Broadcasted Time')
     plt.title("Platform Viewer Rate by time",fontsize=20,color="#000000")
     
     plt.bar(stand-0.2,afreeca,width,color='#0054FF',label='afreeca')
     plt.bar(stand+0.2,kakao,width,color='#FFFF36',label='kakao')
     plt.xticks(stand,x)
     plt.legend(loc='upper right')
     plt.savefig('platformratio.png',format='png',dpi=300)
     plt.show()

