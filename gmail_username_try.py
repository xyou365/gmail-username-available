# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import re
import time
import random
import string

from datetime import datetime
from datetime import timedelta


# Part 1: Username dict
USERNAME_LIST_FULL = []
# with open('4_letter_words.txt') as fp:
#     USERNAME_LIST_FULL = fp.read().splitlines()

with open('words_raw.txt') as fp:
    results = fp.read().splitlines()

rr = ''.join(word for word in results)
USERNAME_LIST_FULL = [word.lower() for word in re.findall('"word":"(\w{4})"', rr)]

PREFIX = 'zz'
NUM_SELECT = 100
USERNAME_LIST = random.sample(USERNAME_LIST_FULL, NUM_SELECT) 
print('There are total %d/%d name available' % (len(USERNAME_LIST_FULL), len(USERNAME_LIST)))


# Part 2: Helper function
# Function used to randomize credentials
def randomize(
                _length_
            ):

    if _length_ > 0 :

        string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        _generated_info_=''
        for _counter_ in range(0,_length_) :
            _generated_info_= _generated_info_ + random.choice(string._characters_)

        return _generated_info_

    else:
        msg(3,'No valid length specified...')
        ext()


# Part 3: Main function
def main():

    curl_link = ''
    if not curl_link:
        curl_link = input('请输入你的专属链接：\n')

    curl_link = re.sub(r'curl', r'curl -s', curl_link)
    print(curl_link) 

    gmail_address_okay = []
    for ii in range(len(USERNAME_LIST)):
        # gmail_address_try = randomize(6)
        gmail_address_try = PREFIX + USERNAME_LIST[ii]
        print(gmail_address_try)
    
        curl_link = re.sub(r'GmailAddress=(\w+)&', r'GmailAddress={}&'.format(gmail_address_try), curl_link)
    
        response = subprocess.check_output(curl_link, shell=True)
        #print(response)
    
        if b'This username is already taken' in response:
            print('%d: The username of %s is taken\n' % (ii, gmail_address_try))
        elif b'Your username is' in response:
            print('%d: The username of %s is okay\n' % (ii, gmail_address_try))
            gmail_address_okay.append(gmail_address_try)
        else:
            print('更新您的专属链接或者更换ip')
        
        time.sleep(random.randint(1, 3))
 
    print('Mail okay\n')
    print(gmail_address_okay)

    with open('gmail_okay.txt', 'w') as fp:
        for mail in gmail_address_okay: fp.write(mail + '\n') 

if __name__ == '__main__':
    main()
