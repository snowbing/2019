
# coding: utf-8

# In[2]:


def find_cmd(word_list):
    i=word_list
    #for i in word_list:
    if( '不' in i or  '别' in i ):
        a=0
    elif( '前' in i  ):
        a=1
        #break
    elif( '后' in i or  '退' in i ):
        a=2
        #break
    elif( '左' in i ):
        a=5
        #break
    elif( '右' in i):
        a=6
        #break
    elif(  '停' in i  or  '关闭' in i ):
        a=7
        #break
    elif( '加' in i or  '快' in i):
        a=3
        #break
    elif( '减' in i or  '慢' in i ):
        a=4
        #break
    else:
        a=0
    return a
