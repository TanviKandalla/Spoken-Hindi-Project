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
    if 'novar' not in df[0][i][df[0][i].rindex("__")+2:]:
    	temp = (float(df[0][i][df[0][i].rindex("__")+2:]))
    else:
    	temp = (float(df[0][i][df[0][i].rindex("__")+2:df[0][i].rindex("-novar")]))

    if temp==round(temp):
        is_variant.append(0)
        total_sentences += 1
    else:
        is_variant.append(1)


# In[91]:


df[4] = is_variant


# In[92]:


result = ''


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



result = "Total number of sentences: " + str(total_sentences)
result+= "\nNumber of sentences where original has minimum dependency distance: "+ str(correct_sentences)
result+="\nAccuracy: "+ str(correct_sentences/total_sentences)
result+="\nTotal number of pairwise items: "+str(total_pairs)+"\nNumber of valid pairs: "+str(correct_pairwise)
result+="\nAccuracy when performing pairwise comparisons for the above: "+str(correct_pairwise/total_pairs)

print(result)

with open("Total Results.txt", 'w', encoding='utf-8') as f:
    f.write(str(result))

# In[ ]:




