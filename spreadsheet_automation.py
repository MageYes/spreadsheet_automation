import pandas as pd
import pandas_market_calendars as mcal
from config import etfs_lst, etfs_hedge_date_dict, etfs_calendar_dict, hedge_info, start_date, end_date, excel_path
import datetime
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 15)
pd.set_option("display.width", 1000)


def get_calendar(mkt_name, start_date, end_date):
    mkt_ex = mcal.get_calendar(mkt_name)
    mkt_ex_schedule = mkt_ex.schedule(start_date=start_date, end_date=end_date)
    mkt_trading_days = mkt_ex_schedule.index.date
    return mkt_trading_days.tolist()


def get_hedge_dict(holding_date, reminder, trading_days):
    t, d = reminder.split('__')
    d0, drift = d.split('+')
    holding_date = datetime.datetime.date(holding_date)
    idx = trading_days.index(holding_date)
    hedge_date = trading_days[idx + int(drift)]
    return hedge_date, t


def match_trading_days_from_reminders(holding_date, Fixing_reminder, FX_reminder, trading_days):
    Fixing_hedge_dict = dict()
    FX_hedge_dict = dict()

    k1, v1 = get_hedge_dict(holding_date, Fixing_reminder, trading_days)
    Fixing_hedge_dict[k1] = v1

    if ',' in FX_reminder:
        qdii_connect_lst = FX_reminder.split(',')
        FX_qdii_reminder = [i for i in qdii_connect_lst if 'QDII' in i][0]
        k3, v3 = get_hedge_dict(holding_date, FX_qdii_reminder, trading_days)
        FX_hedge_dict[k3] = v3
        FX_connect_reminder = [i for i in qdii_connect_lst if 'Connect' in i][0]
        k4, v4 = get_hedge_dict(holding_date, FX_connect_reminder, trading_days)
        FX_hedge_dict[k4] = v4
    else:
        k2, v2 = get_hedge_dict(holding_date, FX_reminder, trading_days)
        FX_hedge_dict[k2] = v2

    return Fixing_hedge_dict, FX_hedge_dict


def get_etf_trading_days(etf_code, start_date, end_date, etfs_calendar_dict):
    opendate_mkt_lst = etfs_calendar_dict[str(etf_code)]
    if len(opendate_mkt_lst) == 1:
        trading_days = get_calendar(opendate_mkt_lst[0], start_date, end_date)
    if len(opendate_mkt_lst) > 1:
        trading_days = set()
        for i in opendate_mkt_lst:
            mkt_i_trading_days = get_calendar(i, start_date, end_date)
            trading_days = trading_days & set(mkt_i_trading_days) if len(trading_days) != 0 else set(mkt_i_trading_days)
        trading_days = sorted(list(trading_days))
    return trading_days


def update_hedge_info(date, etfs_lst, hedge_info):
    hedge_asset_info = None
    return hedge_asset_info


def match_Fixing_FX(etfs_lst, etfs_holding_dataframe, etfs_hedge_date_dataframe, start_date, end_date, etfs_calendar_dict, hedge_info):
    etfs_trading_days = set()
    for col in etfs_lst:
        etf_i_trading_days = get_etf_trading_days(col, start_date, end_date, etfs_calendar_dict)
        etfs_trading_days = etfs_trading_days | set(etf_i_trading_days)
    etfs_trading_days = sorted(list(etfs_trading_days))

    Fixing_hedge_df = pd.DataFrame(index=etfs_trading_days, columns=etfs_lst).notna()*1
    FX_hedge_df = pd.DataFrame(index=etfs_trading_days, columns=etfs_lst).notna()*1
    for i in etfs_holding_dataframe.index:  # i: datetime.date(2023, 5, 15)
        """此处hedge信息仅提示使用"""
        hedge_asset_info = update_hedge_info(i, etfs_lst, hedge_info)  # 从数据源，截面获取并更新数据到指定sheet中

        holding_temp = etfs_holding_dataframe.loc[i].dropna()
        for j in holding_temp.index:  # j: 513010 float
            Fixing_reminder = etfs_hedge_date_dataframe.loc[str(j), 'Fixing']
            FX_reminder = etfs_hedge_date_dataframe.loc[str(j), 'FX']
            trading_days = get_etf_trading_days(j, start_date, end_date, etfs_calendar_dict)
            Fixing_hedge_dict, FX_hedge_dict = match_trading_days_from_reminders(i, Fixing_reminder, FX_reminder, trading_days)
            for k in Fixing_hedge_dict:
                if Fixing_hedge_df.loc[k, str(j)] == 0:
                    Fixing_hedge_df.loc[k, str(j)] = Fixing_hedge_dict[k]
                else:
                    Fixing_hedge_df.loc[k, str(j)] += ',' + Fixing_hedge_dict[k]
            for k in FX_hedge_dict:
                if FX_hedge_df.loc[k, str(j)] == 0:
                    FX_hedge_df.loc[k, str(j)] = FX_hedge_dict[k]
                else:
                    FX_hedge_df.loc[k, str(j)] += ',' + FX_hedge_dict[k]
    return Fixing_hedge_df, FX_hedge_df


def automation(etfs_lst, etfs_hedge_date_dict, excel_path, start_date, end_date, etfs_calendar_dict, hedge_info):
    etfs_holding_dataframe = pd.read_excel(excel_path, index_col=0, sheet_name=0)
    etfs_hedge_date_dataframe = pd.DataFrame(etfs_hedge_date_dict).T
    Fixing_hedge_df, FX_hedge_df = match_Fixing_FX(etfs_lst, etfs_holding_dataframe, etfs_hedge_date_dataframe, start_date, end_date, etfs_calendar_dict, hedge_info)
    Fixing_hedge_df = Fixing_hedge_df.drop(Fixing_hedge_df.loc[(Fixing_hedge_df==0).all(axis=1)].index)
    FX_hedge_df = FX_hedge_df.drop(FX_hedge_df.loc[(FX_hedge_df==0).all(axis=1)].index)
    return Fixing_hedge_df, FX_hedge_df


if __name__ == '__main__':
    Fixing_hedge_df, FX_hedge_df = automation(etfs_lst, etfs_hedge_date_dict, excel_path, start_date, end_date, etfs_calendar_dict, hedge_info)
    print(Fixing_hedge_df)
    print(FX_hedge_df)


# 2023-5-18：config的hedge_info中是否应该放入pr
# 2023-5-18：match_trading_days_from_reminders函数中应该根据截面读取的数据去完善消息提醒