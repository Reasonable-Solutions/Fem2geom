# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:32:54 2012
 .FEM -> .JNL utility. fulkod (tm)
@author: carhe
"""
import Tkinter, tkFileDialog
#from PyQt4 import QtCore 
#from PyQt4 import QtGui
#import win32ui,win32con 

ROOT = Tkinter.Tk()
FA = tkFileDialog.askopenfile(parent=ROOT, mode='r', title='Choose a .FEM file')
   

#
#fd = win32ui.CreateFileDialog(1,'','', 0,'Text |*.txt') 
#fd.SetOFNTitle("Select Text File") 
#print 'path' fd.GetPathName()
#FA = open(fd.GetPathName(),'r') #.replace('\\','/') 



 

def fulconvert(li):
    """
    Hänger på lite nollor och Pn och tabs på ett eller flera listelement
    """
    if len(li) > 2: #liner är a-b, patches är a-b-c-d-a(?) really?
        li.append(li[0])
    #return  "".join(map(lambda x: 'P'+x+'\t\t', map(lambda k: k.zfill(4), map(str, map(int, (map(float, li)))))))
    return  "".join(['P'+c+'\t\t' for c in [c.zfill(4) for c in[str(c) for c in\
    [int(c) for c in [float(c) for c in li]]]]])
    
    
p = {} #points
Q = {} #quads
L = {} #lines
T = {} #triangles
for line in FA:
    if line.find('GCOORD') == 0:
        # FIXED!  ---TODO: FAIL PÅ GCOORD t.ex.   8.00000000e+000 8.75000000e+004 3.99200000e+003-2.59528006e-005
        # eftersom det saknas mellanrum i mellan Y o Z . Räkna tecken? .split() magi? regexp? IDK.. 
        #e = line.split()
       
        #implementera en char-count split function... eftersom gammal fortranskit är på colonner kan vi oxå gøra colonner..  
        a = [0]*5
        a[0] = line[0:8]
        a[1] = line[8:24]
        a[2] = line[24:40]
        a[3] = line[40:56]
        a[4] = line[56:72]
     
        n = int(float(a[1]))
        x = a[2]
        y = a[3]
        z = a[4]
        p[n] = [x, y, z]
        
    if line.find('GELMNT1') == 0:
        e = line.split()
        print(line)
        n = int(float(e[1]))
       
        if int(float(e[3])) in  [9, 24]:
            line2 = next(FA).split()
            Q[n] = [line2[0], line2[1], line2[2], line2[3]]
           
        if int(float(e[3])) in  [3, 25]:
            line2 = next(FA).split()
            T[n] = [line2[0], line2[1], line2[2]]
        
        if int(float(e[3])) in  [15]:
            line2 = next(FA).split()
            L[n] = [line2[0], line2[1]]
            

f = open('PRE5GEO.JNL', 'w')
f.write('%%')
f.write(FA.name)
FA.close()
f.write('\n')
f.write('\n')
f.write('%% ')
f.write(str(len(p)))
f.write(' Points\n')
f.write('%% ')
f.write(str(len(T)))
f.write(' Triangles\n')
f.write('%% ')
f.write(str(len(Q)))
f.write(' Quads\n')
f.write('%% ')
f.write(str(len(L)))
f.write(' Lines\n')



f.write('DEFINE POINT\n')
for k, v in p.iteritems():
    f.write('P')
    f.write(str(k).zfill(4))
    f.write('\t\t\t')
    values = v[0]+'\t\t'+v[1]+'\t\t'+v[2]
    f.write(values)    
    f.write('\n')
    
f.write('end\n')    
f.write('end\n')
f.write('\n')
    
    
    
f.write('define surface\n')
for k, v in Q.iteritems():
    f.write('S')
    f.write(str(k).zfill(4))
    f.write('\t\t\t')
    f.write(fulconvert(v))     
    f.write('\n')
    
f.write('end\n')    
f.write('end\n')
f.write('\n')
    
    
    
    
f.write('define surface\n')
for k, v in T.iteritems():
    f.write('T')
    f.write(str(k).zfill(4))
    f.write('\t\t\t ')
    f.write(fulconvert(v))     
    f.write('\n')
    
f.write('end\n')    
f.write('end\n')
f.write('\n')
        
        
        
        
f.write('define line\n')
for k, v in L.iteritems():
    f.write('L')
    f.write(str(k).zfill(4))
    f.write('\t\t\t')
    f.write(fulconvert(v))    
    f.write('1')
    f.write('\n')
    
f.write('end\n')    
f.write('end\n')
f.write('\n')
f.close()
    
