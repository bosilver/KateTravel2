# -*- coding: utf-8 -*-
import xlrd
import re
import uniout
from datetime import datetime


bookings = list()

def open_excel(file= 'tmp.xlsx'):
    data = xlrd.open_workbook(file)
    return data


def excel_table_byindex(file= 'tmp.xlsx',colnameindex=0,by_index=0):

    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
                list.append(app)
    return list

subject = dict(activity='',
               time='',
               web_adult='',
               web_child='',
               KTL_adult='',
               KTL_child='',
               pay_deposit='',
               pay_all='')

location_id = {
    u'皇后鎮': 'QT',
    u'瓦納卡': 'WANAKA',
    u'西海岸': 'WC',
    u'庫克山和蒂卡普': 'CT',
    u'基督城': 'CHC',
    u'凱庫拉': 'KAI',
    u'但尼丁': 'DUN',
    u'南島北部': 'SN',
    u'斯圖爾特島': 'ST',
    u'奧克蘭': 'AKL',
    u'羅托魯阿': 'RO'
}

def excel_table_byname(file= 'tmp.xlsx', data=None,colnameindex=0,by_name=u'Sheet1'):

    if not data:
        data = open_excel(file)
    table = data.sheet_by_name(by_name)
    name_id = location_id[by_name]
    nrows = table.nrows
    colnames =  table.row_values(colnameindex)
    list =[]
    company = None
    activity = None
    parse_float = lambda x: x.split('-')[0].strip('$') if type(x) != float else ("%.2f" % x)
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            if u'活動/項目/景點' in row[0]: #title column
                continue

            if row[2] == '' or u'http' in row[0]:  #company column
                company = row[0]
                continue

            if row[0] == '': #empty column
                try:
                    float(row[2])
                except:
                    continue
                else:
                    row[0] = activity
                #if re.match(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', row[2]):

            act = dict()
            act['id'] = '%s%d' % (name_id, rownum)
            act['activity'] = activity = row[0]
            act['time'] = row[1]
            act['web_adult'] = parse_float(row[2])
            act['web_child'] = parse_float(row[3])
            act['KTL_adult'] = parse_float(row[4])
            act['KTL_child'] = parse_float(row[5])
            act['pay_deposit_ad'] = parse_float(row[6])
            act['pay_deposit_ch'] = parse_float(row[7])
            act['company'] = company
            list.append(act)
    return list

def get_excel_data(file='tmp.xlsx'):

    tables = []
    data = open_excel(file)
    for sheet in data.sheet_names():
        if u'租車' in sheet:
            continue
        table = list()
        table = excel_table_byname(data=data, by_name=sheet)
        if table:
            tables.append(dict(location=sheet, act_list=table))
    return tables

def get_location(all_data):

    for i in range(len(all_data)):
        print(i, all_data[i]['location'])
    location = input("Choose a location: ")
    return location

def get_activity(data):

    global bookings
    while True:
        for i in range(len(data)):
            comment = '(%s)' % data[i]['time'] if data[i]['time'] else ''
            print('%d. %s%s' % (i, data[i]['activity'], comment))
        act = input("Choose a activity: ")
        adult = input("Input Adult number: ")
        child = input("Input Clild number:")
        date = raw_input("Input date(YYYY/MM/DD HH:MM): ")
        dt = datetime.strptime(date, "%Y/%m/%d %H:%M")
        data[act].update(dict(ad=adult, ch=child, time=dt))
        bookings.append(data[act])
        output_booking()

        a = input('continue booking?: ')
        while a != 'yes' and a != 'no':
            a = input('please enter yes or no to continue booking(y/n): ')
        if a == 'no':
            print('booking finish')
            break

def output_booking():
    """
    """
    i = 1
    print ('')
    print ("   %17s\t%30s\tAD\tCH  " % ('Date & time', 'activity name'))
    for booking in bookings:
        print ("%2d %17s\t%30s\t%2d\t%2d" % (i,
            booking['time'].strftime("%d %b %Y %H:%M"),
            booking['activity'][:30],
            booking['ad'], booking['ch']))
        i += 1
    print ('')
    print ('')

def test_list(data):
    act_table = dict()
    act_list_option = list()
    for i in range(len(data)):
        act_list = data[i]['act_list']
        for j in range(len(act_list)):
            act_list_option.append((act_list[j]['id'], act_list[j]['activity']))
            act_table[act_list[j]['id']] = act_list[j]

    print (act_list_option)
    print ('')
    print (act_table)

def main():


    all_data = get_excel_data()
    test_list(all_data)
    location = get_location(all_data)
    get_activity(all_data[location]['act_list'])
    #tables = excel_table_byindex()
#    for row in tables:
#        print row

    #tables = excel_table_byname()
    #for row in tables:
    #    print row

if __name__=="__main__":
    main()
