'''
Created on Jul 27, 2017

@author: user
'''
import os
if __name__ == '__main__':
    path = os.getcwd()
    files = os.listdir(path)
    for file in files:
        if file.startswith("singarenSFlow"):
            os.rename(file, file[:25] + ".csv")