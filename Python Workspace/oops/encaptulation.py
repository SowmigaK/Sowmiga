#encaptulation
#(limit and product(we cannot able to see it outside))
        #limits-setter and product-getter
class students:  
#protect     
self.attendance=attendance    
#0 to 100     
def attendance(self,value):         
if 0<=value<=100:            
    self._attendance=value         
else:            
    print("enter valid attendance ranging from 0 to 100")     
#when needed,display(getter)     
def attendance(self):         
    return  self.attendance 
def display(self):     
    return f"student name:{self.name}\n attendance-{self.attendance}%"