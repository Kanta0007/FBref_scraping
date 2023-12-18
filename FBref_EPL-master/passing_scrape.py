import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys, getopt
import csv

def scrapeURL(url):
    res = requests.get(url)
    ## The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("",res.text),'lxml')
    all_tables = soup.findAll("tbody")
    team_table = all_tables[0]
    #Parse team_table
    pre_df_squad = dict()
    #Note: features does not contain squad name, it requires special treatment
    features_wanted_squad = {"stat_time","round","dayofweek","venue","result","goals_for","goals_against","opponent","xg_for","xg_against","possession","attendance","captain","formation","referee","match_report"}
    rows_squad = team_table.find_all('tr')
    for row in rows_squad:
        if(row.find('th',{"scope":"row"}) != None):
            name = row.find('th',{"data-stat":"date"}).text.strip().encode().decode("utf-8")
            if 'date' in pre_df_squad:
                pre_df_squad['date'].append(name)
            else:
                pre_df_squad['date'] = [name]
            for f in features_wanted_squad:
                cell = row.find("td",{"data-stat": f})
                if cell is not None:
                    a = cell.text.strip().encode()
                    text = a.decode("utf-8")
                    if f in pre_df_squad:
                        pre_df_squad[f].append(text)
                    else:
                        pre_df_squad[f] = [text]
    df_squad = pd.DataFrame.from_dict(pre_df_squad)
    
    return df_squad
    
    
def main(argv):
    urls = pd.DataFrame()
    df_squad = pd.DataFrame()



    #指定されたコマンドライン引数を処理
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        print('FBref_scrape.py -f <url_csv_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('america_scrape.py -f <url_csv_file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            urls = pd.read_csv(arg,delimiter=',')


    
    #指定したファイルのURL群からそれぞれのURLのデータを取り出す。
    for url in urls:
        print(url)
        df_squad =pd.concat([df_squad, scrapeURL(url)], ignore_index = True)

    df_squad.to_csv('athletic/' + "Almeria_"+ "_squad.csv")

if __name__ == "__main__":
   main(sys.argv[1:])
   