from datetime import datetime
import pandas as pd
import matplotlib

matplotlib.use('Agg') 
matplotlib.rcParams['font.sans-serif'] = 'NanumGothic,AppleGothic' 
import matplotlib.pyplot as plt

def main():
    # 1981년과 2014년 사이의 환율과 고용률을 출력해 봅니다. 
    # 조금 이해하기 쉽게 Pandas 대신 기본 숫자 비교와 문자열 비교를 사용해 봤습니다.
    # 환율 정보 읽어 들이기
    df_exchange = pd.read_csv('DEXKOUS.csv', header=1, 
        names=['DATE', 'DEXKOUS'], skipinitialspace=True, index_col=0)
    years = {}
    output = []
    for index in df_exchange.index:
        year = int(index.split('-')[0])
        if (year not in years) and (1981 < year < 2014):
            if df_exchange.DEXKOUS[index] != ".":
                years[year] = True
                output.append([year, float(df_exchange.DEXKOUS[index])])
    df_exchange = pd.DataFrame(output)

    # 고용률 통계를 구합니다.
    df_jobs = pd.read_excel('gugik.xlsx') 
    output = []
    stacked = df_jobs.stack()[7]
    for index in stacked.index:
        try:
            if 1981 <= int(index) <= 2014:
                output.append([int(index), float(stacked[index])])
        except:
            pass
    s_jobs = pd.DataFrame(output)

    # 첫 번째 그래프 그리기
    plt.subplot(2, 1, 1)
    plt.plot(df_exchange[0], df_exchange[1], label='원/달러') 
    plt.xlim(1981, 2014) # X축의 범위를 설정합니다.
    plt.ylim(500, 2500)
    plt.legend(loc='best')
    
    # 두 번째 그래프 그리기
    print(s_jobs)
    plt.subplot(2, 1, 2) # 3 1 の3 のサブプロットを作成。 
    plt.plot(s_jobs[0], s_jobs[1], label='고용률(%)') 
    plt.xlim(1981, 2014) # X축의 범위를 설정합니다.
    plt.ylim(0, 100) # Y축의 범위를 설정합니다.
    plt.legend(loc='best')
    plt.savefig('historical_data.png', dpi=300) # 이미지를 저장합니다.

if __name__ == '__main__': 
    main()