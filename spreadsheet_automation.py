import pandas as pd
import pandas_market_calendars as mcal

# 获取 NYSE 日历
nyse = mcal.get_calendar('NYSE')

# 获取 HKEX 日历
hkex = mcal.get_calendar('HKEX')
etfs_code_lst = ['513010', '513180', '513380', '159920', '513580']
etfs_remind_dict = {
    '513010': {'Fixing': 'Close_T+1', 'FX': 'Mostly Connect T0'},
    '513180': {'Fixing': '15:40-16:00_T+1', 'FX': '31% QDII, rest Connect'},
    '513380': {'Fixing': '15:45-15:55_T', 'FX': 'QDII mid'},
    '159920': {'Fixing': '15:45-15:55_T+1', 'FX': 'Mostly Connect T0'},
    '513580': {'Fixing': 'Close_T+1', 'FX': 'QDII mid'},
}

if __name__ == '__main__':
    # 载入策略
    etfs_remind_dataframe = pd.DataFrame(etfs_remind_dict).T
    etfs_holding_dataframe = pd.read_excel('spreadsheet_automation.xlsx', index_col=0)

    print(etfs_remind_dataframe)
    print(etfs_holding_dataframe)
