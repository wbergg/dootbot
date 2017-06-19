#!/usr/bin/python
# - IRC-doot-bot -
#
# Thrown together with the help of internet and under the influence of alcohol
# during Dreamhack Summer 2017 by wberg and gson
#
# Connect a relay to GPIO18 / PIN12 on a raspberry pi.


#some necessary things in the life
import threading
from threading import Thread
import RPi.GPIO as GPIO
import socket
import re
import time
import subprocess


#HELLO WORLD EHEHEHHEE
print("Initializing IRC-doot-bot.")

#vars
dootinuse = False

#Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
print("GPIO initialized.")

#standard doot function with delay, type doot in same channel or query with doot-bot
def dootdelay():
    print("DOOT DOOT! (delayed)")
    global dootinuse
    dootinuse = True
    time.sleep(30)
    GPIO.output(12, GPIO.HIGH)
    time.sleep(0.10)
    GPIO.output(12, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(12, GPIO.HIGH)
    time.sleep(0.10)
    GPIO.output(12, GPIO.LOW)
    time.sleep(30)
    dootinuse = False

#standard doot function, but without a delay, type d00tinstant in query with doot-bot.
def d00tinstant():
    print ("DOOT DOOT! (instant)")
    global dootinuse
    dootinuse = True
    GPIO.output(12, GPIO.HIGH)
    time.sleep(0.10)
    GPIO.output(12, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(12, GPIO.HIGH)
    time.sleep(0.10)
    GPIO.output(12, GPIO.LOW)
    dootinuse = False

#sandstorm function mlg420blazefgt, no delay, type darude in query with doot-bot.
def darude():
    print("DOOT DARUDE")
    global dootinuse
    dootinuse = True
    subprocess.call(["python", "/home/pi/irc-doot-bot/darude.py"])
    dootinuse = False

#set vars for IRC
nick = 'doot' #define nick
debug = False # For debug Mode
network = 'se.quakenet.org' #Define IRC Network
port = 6667 #Define IRC Server Port

#debug?
if debug == True: #Check if Debug is True
    chan = '#doot-debug-channel'
elif debug == False: #Check if debus is false
    chan = '#dreamhack'

print("Connecting to server..")
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define  IRC Socket
irc.connect((network,port)) #Connect to Server
print("Connected I guess lol")

time.sleep(2) #chill for a couple a secs

print("Let's dance with the server, hold my beer.")
irc.send('NICK ' + nick + '\r\n') #Send our Nick(Notice the Concatenation)
while True:
    data = irc.recv (512) #Make Data the Receive Buffer
    print(data)
    if data.find('PING') != -1: #If PING is Found in the Data
        print "debug: DATA",data.split()[1]
        pong = re.findall(".*:([0-9]+).*",data)[0]
        print "debug: PONG",pong
        irc.send('PONG ' + data.split()[1] + '\r\n') #Send back a PONG
        break

time.sleep(2)
print("Sending user info.")
irc.send('USER doot doot doot doot\r\n') #Send User Info to the server
time.sleep(5)
print("Joining channel.")
irc.send('JOIN ' + chan + '\r\n') # Join the pre defined channel
time.sleep(2)
#print("Saying hello!")
irc.send('PRIVMSG wberg :Hello!\r\n') #Send a Message to the  channel
irc.send('PRIVMSG gson :Hello!\r\n') #Send a Message to the  channel


#Send IP to admin
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('google.com', 0))
print s.getsockname()[0]
irc.send('PRIVMSG wberg :My IP is ' + s.getsockname()[0] + '\r\n') #Send IP to admin
irc.send('PRIVMSG gson :My IP is ' + s.getsockname()[0] + '\r\n') #Send IP to admin

print("We are go. Users may type doot in chat. To kill this process, press CTRL + C.")
while True: #While Connection is Active
    data = irc.recv (4096) #Make Data the Receive Buffer
    #print data #Print the Data to the console(For debug purposes)
    if data.find('PING') != -1: #If PING is Found in the Data
        irc.send('PONG ' + data.split()[1] + '\r\n') #Send back a PONG
    #let's get those doots!
    elif data.find ( "PRIVMSG " + chan + " :doot" )  != -1: #doot in channel, with delay 30sec | DOOT DOOT | 30sec
        if 'doot' in data:
            if dootinuse == False:
                usernick = data.split('!')[0]
                irc.send( "PRIVMSG gson :doot made by " + usernick[1:] + "\r\n" )
                irc.send( "PRIVMSG wberg :doot made by " + usernick[1:] + "\r\n" )
                Thread(target = dootdelay).start()
    elif  data.find ( "PRIVMSG " + nick + " :doot" )  != -1: #doot in query, with delay 30sec | DOOT DOOT | 30sec
        if 'doot' in data:
            if dootinuse == False:
                usernick = data.split('!')[0]
                irc.send( "PRIVMSG gson :doot made by " + usernick[1:] + "\r\n" )
                irc.send( "PRIVMSG wberg :doot made by " + usernick[1:] + "\r\n" )
                Thread(target = dootdelay).start()
    elif  data.find ( "PRIVMSG " + nick + " :instantdewt" )  != -1: #obviously instant doot, only in query
        if 'instantdewt' in data:
            usernick = data.split('!')[0]
            irc.send( "PRIVMSG gson :instantdewt made by " + usernick[1:] + "\r\n" )
            irc.send( "PRIVMSG wberg :instantdewt made by " + usernick[1:] + "\r\n" )
            Thread(target = d00tinstant).start()
    elif  data.find ( "PRIVMSG " + nick + " :sandstorm" )  != -1: #best song ftp420blaseraden
        if 'sandstorm' in data:
            if dootinuse == False:
                usernick = data.split('!')[0]
                irc.send( "PRIVMSG gson :instantdewt made by " + usernick[1:] + "\r\n" )
                irc.send( "PRIVMSG wberg :instantdewt made by " + usernick[1:] + "\r\n" )
                Thread(target = darude).start()
