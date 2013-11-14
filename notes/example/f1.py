#!/usr/bin/env python
#coding:utf8

def pp():
	print 'pp'

class Person(object):
	count = 0
	
	def __init__(self,name,sex):
		self.name = name
		self.sex = sex
		Person.add_count()
		print 'Now %s is created!There are %s users!'%(self.name,Person.get_count())

	def __del__(self):
		Person.minus_count()
		print 'The user %s is deleted!Now just %s users left!'%(self.name,Person.get_count())

	def say(self):
		pp()

	def act(self):
		print 'act'

	def get_name(self):
		print 'Wlecom %s,your sex is %s' %(self.name,self.sex)

	@classmethod
	def add_count(cls):
		cls.count += 1

	@classmethod
	def get_count(cls):
		return cls.count

	@classmethod
	def minus_count(cls):
		cls.count -= 1

if __name__ == '__main__':
	p1 = Person('swl1','male')
	p2 = Person('222','male')
	p3 = Person('333','male')
	del p3
	p4 = Person('444','male')
#	print id(p1)
#	print type(p1)

