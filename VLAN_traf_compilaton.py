'''
Created on Jun 8, 2017

@author: user
'''
import csv
import operator
import datetime
if __name__ == '__main__':
    overall_traffic = []
    start_date = '120617'
    start_hour = '09'
    start_minute = '27'
    start_time = datetime.datetime(2017,6,12,int(start_hour), int(start_minute))
    end_date_str = '190617-0912'
    current_time = start_time
    end_of_file_ptr = 0
    while True:
        current_date = '{8}{9}/{5}{6}/{2}{3}'.format(*str(current_time))
        current_hour_minute = '{11}{12}:{14}{15}'.format(*str(current_time))
        curr_time_Str ='{8}{9}{5}{6}{2}{3}-{11}{12}{14}{15}'.format(*str(current_time))
        filename = 'singarenSFlow-' + curr_time_Str + '_vlantraffic.csv'
        with open(filename, newline = '') as csvfile:
            spamreader = csv.reader(csvfile)
            sortedlist = sorted(spamreader, key=operator.itemgetter(0))
            for i in range(0, len(sortedlist) - 1):
                overall_traffic.append(sortedlist[i])
                overall_traffic[end_of_file_ptr].insert(0, current_date)
                overall_traffic[end_of_file_ptr].insert(1, current_hour_minute)
                end_of_file_ptr += 1                     
        if (curr_time_Str == end_date_str):
            break
        current_time = current_time + datetime.timedelta(minutes = 15)
        
    with open('Overall_traffic_compilation.csv', 'w', newline = '') as csvfile2:
            spamwriter = csv.writer(csvfile2)
            headerRow = ['Date', 'Time', 'VLAN', 'Outgoing', 'Incoming']
            spamwriter.writerow(headerRow)
            for i in range(0, len(overall_traffic)):
                spamwriter.writerow(overall_traffic[i])