from dbconnection import *


workorder_input = "31170167"



if not df.empty:
    
    print(df)
    df['WORKORDER_N'] = df['WORKORDER_N'].fillna(0).astype(int)
    print("#######################################################################")

    #mydf = df[df["WORKORDER_N"].notnull() & (df["WORKORDER_N"].astype(str) == workorder_input)]
    mydf= df


print()
print(mydf)