'''
Created on Feb 18, 2017

@author: user
'''
import csv
import operator
import datetime
if __name__ == "__main__":
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
        filename = 'singarenSFlow-' + curr_time_Str + '.csv'
        with open(filename, newline = '') as csvfile:
            spamreader = csv.reader(csvfile)
            sortedlist = sorted(spamreader, key=operator.itemgetter(8)) #sort by VLAN_out
            sortedlist1 = sorted(sortedlist, key=operator.itemgetter(7)) #sort by VLAN_in
            newList = []
            for i in range(0, len(sortedlist1)):
                if (sortedlist1[i][0] == 'FLOW'):
                    smallList = []
                    smallList.append(sortedlist1[i][7]) #in_vlan
                    smallList.append(sortedlist1[i][8]) #out_vlan
                    smallList.append(sortedlist1[i][4]) #src_MAC
                    smallList.append(sortedlist1[i][5]) #dst_MAC
                    smallList.append(sortedlist1[i][17]) #packet_size
                    newList.append(smallList) #List of smallLists
            sum = 0
            count = 1
            mac_add_sets = set() #used for distinct src-dst pairs
                
            for i in range(0, len(newList)):
                current_mac_pair = (newList[i][2], newList[i][3]) #(src_MAC, dst_MAC)
                mac_add_sets.add(current_mac_pair)
                if i == (len(newList) - 1): #break out of last row
                    break
                elif newList[i][0] == newList[i+1][0] and newList[i][1] == newList[i+1][1]: #when the next in_VLAN and next out_VLAN are same as the current
                    sum += int(newList[i][4]) #add the packet size
                    count += 1
                    if i == (len(newList) - 2): #to separately handle the second last row(98) and last row(99)
                        sum += int(newList[i+1][4])
                        newList[i+1].append(count)
                        newList[i+1].append(sum)
                        newList[i+1].append(mac_add_sets)
                        sum = 0
                        count = 1
                        mac_add_sets = set()
                else: #when current VLAN pair is different from the next pair, append then reset variables
                    if sum == 0:
                        sum = int(newList[i][4])
                    else:
                        sum += int(newList[i][4])
                    newList[i].append(count)
                    newList[i].append(sum)
                    newList[i].append(mac_add_sets)
                    sum = 0
                    count = 1
                    mac_add_sets = set()
            for i in range(0, len(newList)): #deleting packet_size column throughout then shift subsequent columns
                if (len(newList[i]) > 7):
                    newList[i][4] = newList[i][5]
                    newList[i][5] = newList[i][6]
                    newList[i][6] = newList[i][7]
                    del newList[i][7]
        index = filename.find('.csv')
        filename = filename[:index] + '_output' + filename[index:]
        with open(filename, 'w', newline = '') as csvfile2:
            spamwriter = csv.writer(csvfile2) #this section is to write the rows with count,sum and mac_add_set
            for i in range(0, len(newList)):
                if (len(newList[i]) > 6):
                    spamwriter.writerow(newList[i])
        with open(filename, newline = '') as csvfile3:
            spamreader = csv.reader(csvfile3) #this section is to delete src&dst mac add rows(2  and 3)
            newList2 = []
            for row in spamreader:
                smallList2 = []
                smallList2.append(row[0])
                smallList2.append(row[1])
                smallList2.append(row[4])
                smallList2.append(row[5])
                smallList2.append(row[6])
                newList2.append(smallList2)
        with open('VLAN_Names.csv', newline = '') as csvfile4: #This section is to save the vlan number and names in nameList array
            spamreader = csv.reader(csvfile4)
            nameList = []
            for row in spamreader:
                smallnameList = []
                smallnameList.append(row[0])
                smallnameList.append(row[1])
                nameList.append(smallnameList)
        for i in range(0, len(newList2)):
            description_str = '' 
            for j in range(0, len(nameList)):
                if newList2[i][0] == nameList[j][0]:
                    description_str = description_str + nameList[j][1]
                    newList2[i].append(description_str)
            if  (len(newList2[i]) < 6):
                newList2[i].append('[None]')  
        for i in range(0, len(newList2)):
            description_str = ''
            for j in range(0, len(nameList)):
                if newList2[i][1] == nameList[j][0]:
                    description_str = newList2[i][5] + ' to ' + nameList[j][1]
                    newList2[i][5] = description_str
            if  not description_str:
                newList2[i][5] = newList2[i][5] + ' to ' + '[None]'
        with open(filename, 'w', newline = '') as csvfile5:
            spamwriter = csv.writer(csvfile5)
            headerRow = ['From', 'To', 'Count', 'Total Size', 'MAC Address Pairs', 'Description']
            spamwriter.writerow(headerRow)
            for i in range(0, len(newList2)):
                spamwriter.writerow(newList2[i])
        if (curr_time_Str == end_date_str):
            break
        current_time = current_time + datetime.timedelta(minutes = 15)