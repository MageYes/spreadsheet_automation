import pandas as pd
etfs_lst = ['513010', '513180', '513380', '159920', '513580']
etfs_hedge_date_dict = {
    '513010': {
        'Fixing': 'Close__T+1',
        'FX': 'Mostly_Connect_20:25-20:35__T+0'
    },
    '513180': {
        'Fixing': '15:40-16:00__T+1',
        'FX': '31%_QDII_random__T+1,69%_Connect_20:25-20:35__T+0'
    },
    '513380': {
        'Fixing': '15:45-15:55__T+0',
        'FX': 'QDIImid_random__T+1'
    },
    '159920': {
        'Fixing': '15:45-15:55__T+1',
        'FX': 'Mostly_Connect_20:25-20:35__T+0'
    },
    '513580': {
        'Fixing': 'Close__T+1',
        'FX': 'QDIImid_random__T+1'
    },
}
start_date = pd.Timestamp('2023-05-01')
end_date = pd.Timestamp('2028-12-31')
#excel_path = 'shared_folder/spreadsheet_automation.xlsx'
excel_path = 'spreadsheet_automation.xlsx'