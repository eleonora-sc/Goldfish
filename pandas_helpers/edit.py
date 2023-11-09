import pandas as pd

def remove_columns(dataframe, *args):
    for col_name in args:
        dataframe.drop(col_name,axis=1,inplace=True)

def change_column_position(dataframe, col, place:int):
    columns = list(dataframe.columns)
    try:
        if col in columns:
            columns.remove(col)
            columns.insert(1,col)
            dataframe = dataframe[columns]
    except:
        raise ValueError("Column did not exist")