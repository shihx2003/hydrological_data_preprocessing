# encoding: utf-8
"""
author: @shihx2003
created: 2024-12-24
"""
# %% 读取数据
import os
import pandas as pd
import numpy as np
def generate_date_strings(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date)
    date_strings = date_range.strftime('%Y%m%d').tolist()
    date_df = pd.DataFrame(date_strings, columns=['dt'])
    return date_df

def split_data(input_df):
    df = input_df.copy()
    
    result = {}
    num_rows = 34
    for i in range(16):
        temp1 = df.iloc[i*num_rows:(i+1)*num_rows, :]
        station = temp1.iloc[0, 0].split("-")[1][:-1]
        temp = temp1.iloc[2:-1, :]
        temp.reset_index(drop=True, inplace=True)
        temp.fillna(0, inplace=True)
        result[station] = temp
        del temp
        del temp1
    return result

def reshape_data(input_df, station_name):
    df = input_df.copy()
    

    result = []
    for i in df.columns[1:]:
        df_select = pd.DataFrame()
        day_num = mouth_days[i]
        df_select[i] = df[i]
        temp = df_select.iloc[:day_num, 0]
        result.append(temp)
        del temp
        del df_select

    reshaped = pd.concat(result, ignore_index=True)
    reshaped_df = pd.DataFrame(reshaped)
    reshaped_df.columns = [station_name]
    # print(reshaped_df)
    return reshaped_df

excel_path = r"F:\水文年鉴\紫金关整理.xlsx"
data = pd.read_excel(excel_path, sheet_name="逐日降雨量")
mouth_days = {'一月': 31, '二月': 28, '三月': 31, '四月': 30, '五月': 31, '六月': 30, 
              '七月': 31, '八月': 31, '九月': 30, '十月': 31, '十一月': 30, '十二月': 31}
rain_day = split_data(data)

# reshape_data(rain_day['紫金关站'], '紫金关站')
final_out = generate_date_strings('2022-01-01', '2022-12-31')
for key in rain_day.keys():
    station_data = reshape_data(rain_day[key], key)
    # print(station_data)
    final_out[key] = station_data[key]
final_out.to_excel(r"F:\水文年鉴\紫金关整理_reshape.xlsx", index=False)