import pandas as pd
def midInfo():
    return pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})