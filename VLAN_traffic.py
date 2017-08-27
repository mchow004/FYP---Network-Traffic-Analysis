'''
Created on May 18, 2017

@author: user
'''
import csv
import operator
import datetime
if __name__ == '__main__':
    start_date = '120617'
    start_hour = '09'
    start_minute = '27'
    start_time = datetime.datetime(2017,6,12,int(start_hour), int(start_minute))
    end_date_str = '190617-0912'
    current_time = start_time
    while True:
        current_date = '{8}{9}/{5}{6}/{2}{3}'.format(*str(current_time))
        current_hour_minute = '{11}{12}:{14}{15}'.format(*str(current_time))
        curr_time_Str ='{8}{9}{5}{6}{2}{3}-{11}{12}{14}{15}'.format(*str(current_time))
        filename = 'singarenSFlow-' + curr_time_Str + '_output.csv'
        with open(filename, newline = '') as csvfile:
            spamreader = csv.reader(csvfile)
            sortedlist = sorted(spamreader, key=operator.itemgetter(0))
            sortedlist1 = sorted(sortedlist, key=operator.itemgetter(1))
            newList = []
            total_size = 0
            vlan_set = set()
            for i in range(0, len(sortedlist1)): #outgoing/From
                smallList = []
                if i == (len(sortedlist1) - 1): #break out of last row
                    break
                elif sortedlist[i][0] == sortedlist[i+1][0]:
                    total_size += int(sortedlist[i][3])
                else:
                    if total_size == 0:
                        total_size = int(sortedlist[i][3])
                    else:
                        total_size += int(sortedlist[i][3])
                    smallList.append(sortedlist[i][0])
                    smallList.append(total_size)
                    newList.append(smallList)
                    total_size = 0
            for i in range(0, len(sortedlist1)): #incoming/To
                smallList = []
                if i == (len(sortedlist1) - 1): #break out of last row
                    break
                elif sortedlist1[i][1] == sortedlist1[i+1][1]:
                    total_size += int(sortedlist1[i][3])
                else:
                    if total_size == 0:
                        total_size = int(sortedlist1[i][3])
                    else:
                        total_size += int(sortedlist1[i][3])
                    for j in range(0, len(newList)):
                        if int(newList[j][0]) == int(sortedlist1[i][1]):
                            newList[j].append(total_size)
                            total_size = 0
            for i in range(0, len(newList)):
                if len(newList[i]) < 3:
                    newList[i].append(0)
                        
            index = filename.find('output.csv')
            filename = filename[:index] + 'vlantraffic.csv'                   
            with open(filename, 'w', newline = '') as csvfile2:
                spamwriter = csv.writer(csvfile2)
                headerRow = ['VLAN', 'Outgoing', 'Incoming']
                spamwriter.writerow(headerRow)
                for i in range(0, len(newList)):
                    spamwriter.writerow(newList[i])
        if (curr_time_Str == end_date_str):
            break
        current_time = current_time + datetime.timedelta(minutes = 15)