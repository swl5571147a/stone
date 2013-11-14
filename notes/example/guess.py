#!/usr/bin/python
#coding:utf8

import random

num = random.randint(1,20)

for i in '123456':
	guess = input('Please enter your guess number:')
	if guess == num:
		print 'you are right!'
		break
	else:
		if i == '6':
			print 'you are so .....'
			break
		if guess > num:
			print 'your enter number is large'
			continue
		elif guess < num:
			print 'your enter number is little'
			continue
