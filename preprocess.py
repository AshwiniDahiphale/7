import pandas as pd


def preprocess(df,region_df):
    df=df[df['Season']=='Summer']  #filtering summer dataset
    df=df.merge(region_df,on='NOC',how='left')  #merge with region_df
    df.drop_duplicates(inplace=True)  # removing duplicates
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1) #one hot encoding
    return df