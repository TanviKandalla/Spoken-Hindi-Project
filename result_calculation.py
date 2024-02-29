#!/usr/bin/env python
# coding: utf-8

# In[1]:


with open("Sentence_Data.dat",'r',encoding='utf-8') as file:
        file_contents = file.read()


# In[69]:


import pandas as pd


# In[76]:


df = pd.read_csv("Sentence_Data.dat",delimiter = '\t',header = None)


# In[90]:


is_variant = []
total_sentences = 0
for i in range(0,len(df)):
    temp = (float(df[0][i][df[0][i].rindex("__")+2:]))
    if temp==round(temp):
        is_variant.append(0)
        total_sentences += 1
    else:
        is_variant.append(1)


# In[91]:


df[4] = is_variant


# In[92]:


df


# In[126]:


correct_sentences = 0 #matching sentences for non-pairwise dependency distance calculation
total_pairs = 0 #used to calculate pairwise dependency distance hypothesis
correct_pairwise = 0 #number of pairs with lower dep. distance for original sentence


# In[127]:


reference_index = -1
variant_dds = []
for i in range(0,len(df)):
    if df[4][i] == 0:
        if variant_dds != [] and df[2][reference_index]< min(variant_dds):
            correct_sentences += 1
        elif variant_dds == [] and i!=0:
            correct_sentences += 1
        
        reference_index = i
        variant_dds = []
    else: #perform pairwise comparison here
        total_pairs += 1
        if df[2][reference_index] <= df[2][i]:
            correct_pairwise += 1
        variant_dds.append(df[1][i])

if variant_dds != [] and df[2][reference_index]< min(variant_dds):
            correct_sentences += 1
elif variant_dds == []:
    correct_sentences += 1


# In[133]:


print("Number of sentences where original has minimum dependency distance: ", correct_sentences)
print("Accuracy: ", correct_sentences/total_sentences)

print("Accuracy when performing pairwise comparisons for the above: ", correct_pairwise/total_pairs)


# In[ ]:



