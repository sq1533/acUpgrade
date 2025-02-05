import os
import pandas as pd
midInfoPath = os.path.join(os.path.dirname(__file__),"DB","2midInfo.json")
mailACCPath = os.path.join(os.path.dirname(__file__),"DB","4-3mailAccess.json")
def cre(data):
    DF = pd.read_json(midInfoPath,orient='records',dtype={'mid':str,'info':str})
    new = {
        "mid":data['mid'],
        "info":data['info']
        }
    new_df = pd.DataFrame(new,index=[0])
    resurts = pd.concat([DF,new_df],ignore_index=True)
    return resurts.to_json(midInfoPath,orient='records',force_ascii=False,indent=4)

def put(data):
    DF = pd.read_json(midInfoPath,orient='records',dtype={'mid':str,'info':str})
    chn = {
        "mid":data['mid'],
        "info":data['info']
        }
    DF.loc[DF['mid']==chn['mid'],'info'] = chn['info']
    return DF.to_json(midInfoPath,orient='records',force_ascii=False,indent=4)

def delete(data):
    DF = pd.read_json(midInfoPath,orient='records',dtype={'mid':str,'info':str})
    d = {
        "mid":data['mid']
        }
    ind = DF[DF['mid']==d['mid']].index
    DF.drop(ind, inplace=True)
    return DF.to_json(midInfoPath,orient='records',force_ascii=False,indent=4)

def mail(data):
    email = {
        "passnumber":data["passnumber"],
        "addr":data["addr"],
        "subaddr":data["subaddr"],
        "title":data["title"],
        "main":data["main"]
        }
    PN = pd.DataFrame(email,index=[0])
    return PN.to_json(mailACCPath,orient='records',force_ascii=False,indent=4)