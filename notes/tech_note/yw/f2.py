#coding:utf8
#!/usr/bin/env python

class Person(object):
    count = 0
    
    def __init__(self, n, s):
        self.name = n
        self.sex = s
        Person.add_count()
        print 'a person created'
        #Person.get_count()
        #print "welcome %s, sex is %s"%(self.name, self.sex)
    
    def __del__(self):
        pass

    def say(self):
        Person.add()
        return "hello!! Person has %s "%Person.get_count()
    
    def get_name(self):
        return self.name

    def get_count_all(self):
        return Person.get_count()
    
    @classmethod
    def add_count(cls):
        cls.count += 1

    @classmethod
    def get_count(cls):
        return  cls.count
    
    @staticmethod
    def add():
        print "call add()! "

class Emp(Person):
    def __init__(self,name, sex, dept):
        Person.__init__(self, name, sex)
        self.dept = dept

    def work(self):
        print "I m working!!"


    def say(self):
        print "Im %s. "%self.name
    

if __name__ == "__main__":
    alen = Emp('alen', 'male', 'dp1')
    print alen.get_name()
    alen.say()

