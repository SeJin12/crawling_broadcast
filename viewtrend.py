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

def trend():
     # 폰트 설정
     font_location = 'C:/WINDOWS/FONTS/NANUMGOTHIC.TTF'  
     font_manager.FontProperties(fname = font_location)
     rc('font', family = "NanumGothic")

     # DB에서 가져온 결과 리스트에 저장
     a_data = get('select a_date,sum(a_totalViewer) from reportPython_afreeca group by a_date')
     k_data = get('select k_date,sum(k_totalViewer) from reportPython_kakao group by k_date')

     temp = [ a_data[i][0][5:] for i in range(len(a_data)) ] # x축 값 ( 년도를 뺀 )
     datax = []
     for i in temp:
          datax.append((i[:5]+'\n'+ i[6:]))
     
     a_datay = [ int(a_data[i][1]) for i in range(len(a_data)) ]
     k_datay = [ int(k_data[i][1]) for i in range(len(k_data)) ]
     t_datay = [] # total
     for i in range(len(k_datay)):
          t_datay.append(a_datay[i] + k_datay[i])

     plt.figure(figsize=(12,6))
     ax = plt.axes()
     plt.plot(datax,t_datay,color='#000000',label = 'total_viewer') # 총 합계
     plt.plot(datax,a_datay,color='#0054FF',label = 'afreeca') # 아프리카 
     plt.plot(datax,k_datay,color='#FFFF36',label = 'kakao') # 카카오
     
     ax.set_ylim([0,max(t_datay)*3/2])
     
     ax.yaxis.set_major_locator(ticker.MultipleLocator(10000))
     ax.yaxis.set_minor_locator(ticker.MultipleLocator(5000))
     
     plt.grid(which='major',ls='-',linewidth='0.5',axis='x')
     plt.grid(which='major',ls=':',linewidth='0.5',axis='y')
     plt.grid(which='minor',linewidth='0.5',axis='y')

     plt.xlabel('Date')
     plt.ylabel('Viewer')
     plt.legend(loc='upper right')
     plt.title('Viewer trend by time',fontsize=20,color='#000000')
     plt.savefig('viewtrend.png',format='png',dpi=300)
     plt.show()