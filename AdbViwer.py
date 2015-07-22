import re
import os
import sys
import time
import pickle
import subprocess as sp

'''
Created on 16.07.2015

@author: s.tischenko
'''
class AdbViwer:
    '''
    initialize adb shell
    check connected device id
    check device id from previous connected device table
    get device id, name, build type, android version 
    save device id, name, build type, android version to previous connected device table
    '''
    def __init__(self):
        self.device_list = self.initialize()
        self.device_info = self.analize_data()
    
    def initialize(self):
        adb=sp.call("adb devices", shell=True)
        if adb!=0:
            print "Adb shell can't be started!!!\nCheck Adb shell folder in system path!\n"
            time.sleep(3)
            sys.exit()
        else:
            return  re.findall(r'\s(\w*\d\w*)+?\s',os.popen("adb devices").read(), re.S)
        
    def get_prop(self,device_id):
        id_data = {}
        com = 'adb -s '+device_id+' shell getprop ro.'
        id_data['model'] = os.popen(com+'product.model').read().rstrip()
        id_data['android_version'] = os.popen(com+'build.version.release').read().rstrip()
        id_data['build_type'] = os.popen(com+'build.type').read().rstrip()
        return id_data
    
    def get_pickle_data(self):
        if os.path.exists('data.pickle')==False:
            self.update_data({})
        with open('data.pickle', 'rb') as f:
            return pickle.load(f)
                
    def update_data(self,pickle_data,data={}):
        with open('data.pickle', 'wb') as f:
            pickle_data.update(data)
            pickle.dump(pickle_data, f)
            
    def update_pickle_data(self):
        '''
        Method for update data from device to previously saved data in pickle file
        '''
        time.clock()
        self.initialize()
        pickle_data = self.get_pickle_data()
        data = {device_id:self.get_prop(device_id) for device_id in self.device_list}
        self.update_data(pickle_data,data)
        print time.clock(),data
            
    def analize_data(self):
        time.clock()
        pickle_data = self.get_pickle_data()
        data = {device_id:self.get_prop(device_id) for device_id in self.device_list if device_id not in pickle_data.keys()}
        data.update({device_id:pickle_data[device_id] for device_id in self.device_list if device_id in pickle_data.keys()})
        self.update_data(pickle_data,data)
        print time.clock(),data
        
adb = AdbViwer()
