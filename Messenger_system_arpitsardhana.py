#Copyright (c) 2015 All Right Reserved,Arpit Singh(arpitsardhana2008@gmail.com)
#Date:12 September 2015
# Messenger_system_arpitsardhana.py is free program: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Messenger_system_arpitsardhana.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# for terms and conditions see, see <http://www.gnu.org/licenses/>.
#
#Summary: Messenger system is implemennted in which users can follow each other and post messages. 
#	On their respective timeline,can see messages posted by people whom they follow or reply to messages
#	originated from following users.


import os
import sys
import datetime
import random
from itertools import count

list_user = dict() #Hash table to keep track of all created users
list_msg  = dict() #Hash table to keep track of all created messages
graph = dict() #Hash table to keep track of folower list
start = 0 #bieber node
class user:
	_ids = count(0)
	def __init__(self):
		self.id = self._ids.next()#keep track of id of isntances created 
		self.following = [self.id]#keep track of messages posted by himself 
		self.follower = [self.id] #keep track of message posted by himself]
		self.time_line = [] #since we already has list_msg, we just need ID of msgs
		list_user[self.id] = self
		graph[self.id] = [] 

class message:
        _ids = count(0) 
        def __init__(self,msg_str,reply):
                self.id = self._ids.next() #keep track of message instances
                self.time_stamp = datetime.datetime.now().time()
                self.src = -1 #source set when message posted 
                self.msg = msg_str
                self.reply_id = reply #reply id set on reply otherwise remain -1
		list_msg[self.id] = self

#User  X to follow user Y
def follow(X,Y):
	if X in list_user and Y in list_user:
		user_x = list_user[X]
		user_y = list_user[Y]
		if Y not in user_x.following:
			user_x.following.append(Y)
			graph[X].append(Y)
			user_y.follower.append(X)

			
#User X unfollows user Y
def unfollow(X,Y):
	if X in list_user and Y in list_user:
		user_x = list_user[X]
		user_y = list_user[Y]
		if Y in user_x.following:	
			user_x.following.remove(Y)
			user_y.follower.remove(X)
			graph[Y].remove(Y)

#user Y post Message X
def post(X,Y):
	if X in list_msg and Y in list_user:
        	user_y = list_user[Y]
		msg_x  = list_msg[X]
		msg_x.src = Y
	#Post this message in timeline of all followers of Y
		for user in user_y.follower:
			temp_user = list_user[user]
			if X not in temp_user.time_line:
				temp_user.time_line.append(X)

	#If message X is reply to original message, post X to all followers of original sender
		rep = msg_x.reply_id
		if rep in list_msg:
			rep_msg = list_msg[rep] #find the original message
			if rep_msg.src < 0 :
				print "Message generated but not posted"
				return
			rep_user = list_user[rep_msg.src] #find original sender
			for usr in rep_user.follower: #recurse through original sender follower
				temp_user = list_user[usr]
				if X not in temp_user.time_line:
					temp_user.time_line.append(X) #Post in original sender's followers timeline if message is not already present.

#Print timeline of user X and print top K messages
def timeline(X,K):
	if X not in list_user :
		print "User does not exist"
		return
	user_x = list_user[X]
	timeline_usr = user_x.time_line
	timeline_usr = sorted(timeline_usr,reverse=True) #display timeline in reverese
	count = 1
	print "timeline of user " +str(X) 
	for msg in timeline_usr:
		temp_msg = list_msg[msg]
		print temp_msg.msg
		count += 1
		if count > K:
			break

#Function to find out minimum distance from bieber node
def bieber(X):
	if X not in list_user:
		print "User does not exist"
		return
        len_dict = { }
        count = 1
        flag = 1
        cur_list = graph[start]
        track_list =list()
        while (flag == 1):
                next_list = []
                #print "printing current_list " + str(cur_list)
                if not cur_list:
                        flag = 0
                        break
                for edge in cur_list:
                        len_dict[edge] = count
                        track_list.append(edge)
                        for next_no in  graph[edge]:#traversing list of vertices
                                if next_no != start:
                                        if next_no not in len_dict  and next_no != start:
                                                next_list.append(next_no)
                next_list = set(next_list)
                for key in len_dict: #deleting repeated elements
                        if key in next_list:
                                next_list.remove(key)
                if not next_list:
                        flag = 0
                        break
                cur_list = next_list

                count += 1


        output_list = list()
        tr_list = list()
        for key in graph:
                tr_list.append(int(key))

        tr_list = sorted(tr_list)
        #print tr_list . List finds out minimum distance with every node.
        for key1 in tr_list:
                key = key1
                if key == start:
                        continue
                if key in len_dict:
                        output_list.append(len_dict[key])
                else:
                        output_list.append(-1)
	#print str(len_dict)
	if X in len_dict:
		print len_dict[X]
	else : 
		print -1
        #print ' '.join(map(str,output_list))
				
def create_user():
	id_user = user()
	print "user id is "+ str(id_user.id)

def create_message():
	print "Write message"
	msg = raw_input()
	print "Type ID of original msg if msg is reply otherwise type -1"
	rep = int(raw_input())
	msgid = message(msg,rep)
	print "Message id is " + str(msgid.id)

def create_users(N):
	usr_l = []
        for i in range(0,N):
                id_user = user()
		usr_l.append(id_user.id)

	print "Userid is "+ ' '.join(map(str,usr_l))

def create_messages(M):
	msg_l = []
        for i in range(0,M):
               msg = "Message --" + str(i)
               reply = -1 
               msgid = message(msg,reply)
	       msg_l.append(msgid.id)
	print "messageid are "+ ' '.join(map(str,msg_l))

def see_all_userid():
	usr_l = []
	for key in list_user:
		usr_l.append(key)
	print ' '.join(map(str,usr_l))

def see_all_msgid():
	msg_l = []
	for key in list_msg:
		msg_l.append(key)
	print ' '.join(map(str,msg_l))
 
def set_bieber(N):
	global start
	if N in list_user:
		start = N

def create_random_following(N):
	total = len(list_user) 
	if total < 2:
		print "insufficent users"
		return	
	for i in range(0,N):
		x = random.randint(0,total)
		y = random.randint(0,total)
		follow(x,y)

def see_follower_map():
	print str(graph)
	for key in graph:
		print str(key) + " follows " + ' '.join(map(str,graph[key]))

def usr_msg(usr,msg):
	for i in range(0,usr):
        	id_user = user()

        for i in range(0,msg):
                msg = "Message --" + str(i)
                reply = -1 
                msgid = message(msg,reply)

	
def main_1(): #test function
        #print str(list_msg)
	usr_msg(5,10)
	
	for i in range(0,3):
		ran = random.randint(0,3)
		for j in range(0,ran):
			x = random.randint(0,3)
			follow(i,x)
		
	for i in range(0,3):
		print '\n'+"follower list of user" + str(i) 
		print str(list_user[i].follower)


	for j in range(0,5):
		x = random.randint(0,3)
		post(j,x)
		print str(x) + "has posted message" + str(j)


	for m in range(0,3):
		print '\n'+"timeline of user" + str(m)
		timeline(m,5)
	        usr_msg(10,20)
        
	follow(0,1)
        follow(0,2)
        follow(0,3)
        follow(1,2)
        follow(3,2)
        follow(2,3)
        follow(3,4)
        post(2,2)
        post(1,2)
        post(3,3)
	#post(5,1)
        timeline(0,2)
        timeline(2,3)
        timeline(3,3)
        bieber(4)
        usr_msg(10,0)
        follow(1,2)
        follow(2,3)
        msg1 = message("i am main",-1)
        msg2 = message("i am reply",5)
        post(msg1.id,2)
        post(msg2.id,3)
        timeline(1,3)



def main():
	flag = 1
        print "Messenger System"
        print "Enter the option you want to select"

	while(flag == 1):
		print "(1) Create User"
		print "(2)Create N users"
		print "(3)Create Message"
		print "(4)Create M messages"
		print "(5)See user ids"
		print "(6)See message ids"
		print "(7)Follow x to y"
		print "(8)unfollow x to y"
		print "(9)post message X as user Y"
		print "(10)timeline of user X and limit of Y messages"
		print "(11)set bieber"
		print "(12)find bieber"
		print "(13)create random following"
		print "(14)see followers map"
		print "(15)quit"


		op = raw_input()
		if op.isdigit():
			option = int(op)
		else:
			continue

		if option == 1 :	
			create_user()
		elif option == 2:
			print "enter no of users"
			a = int(raw_input())
			create_users(a)
		elif option == 3:
			create_message()
		elif option == 4:
                        print "enter no of messages"
                        a = int(raw_input())
                        create_messages(a)
		elif option == 5:
			see_all_userid()
		elif option ==6:
			see_all_msgid()
		elif option == 7:
			print "X Follows Y ,enter x and y separated by space"
			us = raw_input().split()
			if len(us) <= 1:
				print "enter correct no of arguments"
				continue
			x = int(us[0])
			y = int(us[1])
			follow(x,y)
                elif option == 8:
                        print "X unfollows Y,enter x and y separated by space"
                        us = raw_input().split()
                        if len(us) <= 1:
                                continue
                        x = int(us[0])
                        y = int(us[1])
                        unfollow(x,y)
                elif option == 9:
                        print "Msg X posted as User Y,enter x and y separated by space"
                        us = raw_input().split()
                        if len(us) <= 1:
				print "enter correct no of arguments"
                                continue
                        x = int(us[0])
                        y = int(us[1])
                        post(x,y)
                elif option == 10:
                        print "See K top messages of user X,enter x and k separated by space"
                        us = raw_input().split()
                        if len(us) <= 1:
				print "enter correct no of arguments"
                                continue
                        x = int(us[0])
                        y = int(us[1])
                        timeline(x,y)
		elif option == 11:
			print "enter bieber node"
			b = int(raw_input())
			set_bieber(b)
		elif option == 12:
			print "enter end node"
			n = int(raw_input())
			bieber(n)
		elif option == 13:
			print "enter no of follower nodes"
			n = int(raw_input())
			create_random_following(n)
		elif option == 14:
			see_follower_map()
		elif option == 15:
			flag = 0
			break

		print "Do you want to continue, enter yes or no"
		inp = raw_input()
		if inp == "no":
			flag = 0
			break

			



main()

