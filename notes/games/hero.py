#!/usr/bin/python
#coding:utf8

import random

def add_act(hero):
	hero[2] *= 2
	print 'Oh,yeah!Your act change to double!'

def add_blood(hero):
	hero[1] += 20
	print 'Oh,yeah!Your blood add 20!'

def minus_blood(hero):
	hero[1] -= 20
	print 'Oh,yeah!Your blood minus 20!'

def go_left(hero):
	guess = random.randint(1,4)
	if guess == 1:
		add_act(hero)
	elif guess == 2:
		add_blood(hero)
	else:
		minus_blood(hero)

def go_back(hero):
	pass		

def welcom(hero):
	print '''If you want go to the next romm,please enter "G"
	and if you want to go left to look for something in the left room, please enter "L"
	Now please give your choise-->'''
	

hero = ['hero',100,5,1]
boss = ['boss',200,10]


