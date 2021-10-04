#import the library used to query a website
# start poing https://adataanalyst.com/data-analysis-resources/winning-numbers-irish-lotto/

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt


def get_data_from_internet():
#specify the url for 2017
    years = ["archive-2021","archive-2020","archive-2019","archive-2018","archive-2017","archive-2016","archive-2015",
              "archive-2013","archive-2012","archive-2011","archive-2010","archive-2009","archive-2008","archive-2007",
              "archive-2006","archive-2005","archive-2004","archive-2003","archive-2002","archive-2001","archive-2000",
              "archive-1999","archive-1998","archive-1997","archive-1996","archive-1995","archive-1994","archive-1993",
              "archive-1992","archive-1991","archive-1990","archive-1989","archive-1988"]

    yearlist = list()
    yearlistbonus = list()
    ano =1
    for year in years:
        lottery = "https://www.irishlottery.com/"+year
        #Query the website and return the html to the variable 'page'
        page = requests.get(lottery)
        soup = BeautifulSoup(page.content, 'html5lib')

        #print(soup)

        ball_class = soup.find_all(class_='ball')
        bonusball = soup.find_all(class_='bonus-ball')
        if not bonusball:
            bonusball = ['0']*(len(ball_class)//6)
        yearlistbonus.append(bonusball)
        #print(ano ,len(ball_class)//6, len(bonusball),bonusball)
        yearlist.append(ball_class)
        ano+=1
        if ano == 29:
            break
    return yearlist, yearlistbonus


def processa_dados(yearlist, yearlistbonus):

    mat = list()
    val = list()
    valbonus =list()
    str_remove = r'\W+\D+'

    #montagem do vetor de bolas bonus
    for y in yearlistbonus:
        for bn in y:
            valbonus.append(int(re.sub(str_remove, '', str(bn))))

    for y in yearlist:
        for b in y:
            val.append(re.sub(str_remove, '', str(b)))

    #montagem da matriz de dados das bolas de 1 a 6
    for b in range(0, len(val), 6):
        mat.append(val[b:b+6])

    return mat, valbonus


def createDataframe(mat,valbonus):
    vec = pd.Series(valbonus)
    df = pd.DataFrame(mat)
    columns = ["ball_one", "ball_two", "ball_three", "ball_four", "ball_five", "ball_six"]
    df.columns = columns
    df.insert(6, "bonusball", vec, True)
    return df


def readdataframe(filename):

    return pd.read_csv(filename, sep=';')


# yearlist, yearlistbonus = get_data_from_internet()
#
# mat, valbonus = processa_dados(yearlist, yearlistbonus)
#
# df = createDataframe(mat, valbonus)

df = readdataframe("loteryirelante.csv")

columns5 = ["ball_one", "ball_two", "ball_three", "ball_four", "ball_five", "ball_six"]
df["sum_six_ball"] = df[columns5].sum(axis=1)


columns6 = ["ball_one", "ball_two", "ball_three", "ball_four", "ball_five", "ball_six", "bonusball"]
df["sum_allballs"] = df[columns6].sum(axis=1)

print(df["sum_six_ball"].min(),df["sum_six_ball"].max())
print(df["sum_allballs"].min(),df["sum_allballs"].max())

hist = df["sum_six_ball"].tolist()
plt.hist(hist, bins=50)
plt.xlabel("bins")
plt.ylabel("contagem")






