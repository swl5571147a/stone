#coding:utf8
#!/usr/bin/env python

class Person(object):
    count = 0
    
    def __init__(self, n, s):
        self.name = n
        self.sex = s
        Person.add_count()
        #Person.get_count()
        #print "welcome %s, sex is %s"%(self.name, self.sex)
    
    def __del__(self):
        Person.count -= 1
        print "user %s is delete  ! just %s mumbers "%(self.name, Person.count)
        
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
    pass






#print __name__


if __name__ == "__main__":
    p1 = Person('alen', 'male')
    p1.say()
    Person.add()
    '''
    print Person.get_count()
    p1 = Person('alen', 'male')
    p2 = Person('ben', 'male')
    p3 = Person('ben1', 'male')
    del p1
    print Person.get_count()
    p4 = Person('ben2', 'male')
    p5 = Person('ben3', 'male')
    print Person.get_count()
    p6 = Person('ben4', 'male')
    #print p1.get_count_all() 
    

    print id(p1)
    print type(p1)
    p2 = Person()
    print id(p1)
    print type(p1)
    print p1.say()
    print p1.get_name()
    '''
    #print Person.count
    
    #Person.add_count()
    #print Person.get_count()
    #print "p1 call",p1.count
    #p1.count += 10
    #print "p1 call",p1.count


    #Person.add_count()
    #print Person.get_count()
    


