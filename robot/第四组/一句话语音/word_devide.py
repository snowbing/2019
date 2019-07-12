
# coding: utf-8

# In[1]:


import jieba


# In[11]:


def jieba_devide(sentence):
    sen_list=[]
    seg_list = jieba.cut(sentence, cut_all=False)# 精确模式
    sen_str=" ".join(seg_list)
    sen_list=[str(i) for i in sen_str.split()]
    return sen_list

