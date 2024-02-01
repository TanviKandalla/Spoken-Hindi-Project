#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import csv
import math
import os
import itertools
import re
import string
import numpy as np
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")


# In[2]:


def sentence_creation(file_contents):
    # Create a Beautiful Soup object
    soup = BeautifulSoup(file_contents, 'html.parser')
    # Find all <text> tags and extract their content
    sentence_tags = soup.find_all('sentence')
    return sentence_tags


# In[3]:


def create_df(text): #input should be sentence_tags[i], it will return the dataframe for that
    text = str(text)
    lines = text.split("\n")
    # Remove the first and last lines.
    lines = lines[1:-1]
    # Join the lines back into a string.
    text = "\n".join(lines)
    
    data_list = []
    lines = text.split("\n")
    
    for line in lines:
        columns = line.split("\t")
        data_list.append(columns)

    # Create a DataFrame from the list of lists
    df = pd.DataFrame(data_list)
    df = df.fillna('')
    
    df['Chunk Number'] = 0
    for i in range(len(df)):
        if df[0][i] == '':
            df['Chunk Number'][i] = df['Chunk Number'][i-1]
        else:
            if '.' in df[0][i]:
                match = re.search(r'(\d+)\.\d+', df[0][i])
                if match:
                    df['Chunk Number'][i] = int(match.group(1))
            else:
                    df['Chunk Number'][i] = int(df[0][i])
            
#             df['Chunk Number'][i] = math.floor(float(df[0][i]))
    return df


# In[4]:


def split_tags(df,tag_column):
    import numpy as np
    # Create a DataFrame with a column containing tags.
    df2 = pd.DataFrame(df[tag_column])
    # Create a new DataFrame to store the extracted attributes.
    new_df = pd.DataFrame()
    # Iterate over the rows in the new DataFrame.
    for i in range(len(df2)):
        if df2[tag_column][i] != '':
            # Parse the tag and extract the attributes.
            soup = BeautifulSoup(df2[tag_column][i], 'html.parser')
            t = soup.find('fs')
            attributes = t.attrs
        else:
            # Create a dictionary of NaN values for all existing attribute columns.
            attributes = {key: np.nan for key in new_df.columns}
        # Add the attributes to the row as new columns.
        for key, value in attributes.items():
            new_df.loc[i, key] = value

    # Concatenate the new DataFrame back to the original DataFrame.
    df3 = pd.concat([df2, new_df], axis=1)
    df3 = df3.fillna('')
    df = pd.concat([df, df3.drop(3, axis = 1)], axis = 1)
    
    if 'drel' not in df.columns:
    	df['drel'] = ':'
    else:
        for i in range(0,len(df)):
            if df['drel'][i] == '':
                df['drel'][i] = ':'
    if 'drel' in df.columns:
        # Split the column into two columns containing `type` and `location`.
        drels = df['drel']
        df_drel = pd.DataFrame([x.split(':') for x in df['drel']], columns=['drel_type', 'drel_location'])

        df = pd.concat([df, df_drel], axis=1)
    return df


# In[5]:


def linked_vgf(df): #to generate list of indices linked to vgf
    variant_dfs = []
    vgf_linked = []
    last_vgf = 0
    for i in range(0,len(df)):
        if 'VGF' in df['name'][i]:
            last_vgf = i

    for i in range(0,len(df)):
        if df['drel_location'][i] == df['name'][last_vgf]:
            vgf_linked.append(i)
    vgf_linked = [x for x in vgf_linked if x <= last_vgf]
    
    for i in range(0,len(vgf_linked)): #check linked rows for each entry in vgf_linked
        temp = []
        temp.append(vgf_linked[i])
        last_chunk = vgf_linked[i]
        for j in range(vgf_linked[i] - 1, -1, -1): #iterate over the df backwards from i to find the linked rows
            if df[0][j] == '':
                continue
            chunk = 0
            if '.' in df[0][j]:
                match = re.search(r'(\d+)\.\d+', df[0][j])
                if match:
                    chunk = int(match.group(1))
            else:
                    chunk = int(df[0][j])
            if (chunk) != float(df['Chunk Number'][j]):
                continue
            if df['drel_location'][j] == df['name'][last_chunk]:
                temp.append(j)
            else:
                break
            if chunk == df['Chunk Number'][j]:
                last_chunk = j
        vgf_linked[i] = temp

    for i in range(0,len(vgf_linked)):
        vgf_linked[i].reverse()
        
    
    #to generate vgf_linked with index of every element in that chunk
    for i in range(0,len(vgf_linked)):
        for j in range(0,len(vgf_linked[i])): #consider each individual element in vgf_linked
            for k in range(vgf_linked[i][j]+1,len(df)):
                if df["Chunk Number"][vgf_linked[i][j]] == df["Chunk Number"][k]:
                    vgf_linked[i].append(k)
                else:
                    break
        vgf_linked[i].sort()

    return vgf_linked,last_vgf


# In[6]:


def count_words(result):
    s = (' '.join(result).split(' '))
    words = 0
    #print(s)
    for i in s:
        if '((' in i or '))' in i or '।' in i or i== ' ' or i in string.punctuation:
            continue
        words += 1
        #print(i)
    #print(words)
    return words


# In[7]:


def fill_and_flatten(original_list, permutation, original_permutation):
    new_list = []
    
    filled_original = []
    for i in range(0,len(original_permutation)):
        filled_original.append(original_permutation[i])
        prev = original_permutation[i][len(original_permutation[i])-1]
        if i!= len(original_permutation)-1:
            succ = original_permutation[i+1][0]
            temp = list(range(prev+1,succ))
            filled_original.append(temp)
        else:
            temp = list(range(prev+1, len(original_list)))
            filled_original.append(temp)
    
    index = 0
    flag = 0 #0 means first index is chunk, next is not, etc. & 1 means first index is not, next is chunk, etc.
    if filled_original == []:
    	return new_list
    if original_permutation[0][0] != 0:
        temp = list(range(0,original_permutation[0][0]))
        filled_original.insert(0, temp)
    if filled_original[0] not in permutation:
        flag = 1
    for i in range(0,len(filled_original)):
        if flag==0:
            if i%2==0:
                new_list.append(permutation[int(np.floor(i/2))])
            else:
                new_list.append(filled_original[i])
        else:
            if i%2==0:
                new_list.append(filled_original[i])
            else:
                new_list.append(permutation[int(np.floor(i/2))])
                
#     remaining_indices = set(range(len(original_list))) - set(index for chunk in permutation for index in chunk)
#     for chunk_indices in permutation:
#         #chunk_indices = [18,19,20]
#         for i in chunk_indices:
#             #i = 18
#             new_list.append(original_list[i])
#     #remaining_indices = [0-24 - ]
    
#     for i in sorted(remaining_indices):
#         new_list.append(original_list[i])

    return sum(new_list, [])


# In[8]:


def apply_permutation(original_list, permutations):
    new_list = []
    for i in range(0,len(permutations)):
        new_list.append(original_list[permutations[i]])
    return new_list


# In[20]:


def split_at_double_parentheses(lst):
    result = []
    for item in lst:
        while '))((' in item:
            item = item.replace('))((', '((', 1)  # Replace the first occurrence
            item = item.replace('))(((', '((', 1)  # If you have '(((', replace it with '))'
            result.append('))')
        result.append(item)
    return result


# In[144]:


def dependency_length(input_text, vgf_word, linked_chunk_endings):
    words_in_sentence = input_text
    # print(words_in_sentence)

    chunk_positions = []
    vgf_position = 0
    for i in range(len(words_in_sentence)-1,-1,-1):
        if vgf_word == words_in_sentence[i]:
            vgf_position = i
            break
    for i in linked_chunk_endings:
        for j in range(len(words_in_sentence)-1,-1,-1):
#             print(j, words_in_sentence[j])
            if i==words_in_sentence[j]:
                chunk_positions.append(j)
                break


    #now we have to find the sum of distances.
    sum_distances = 0
    for i in range(0,len(chunk_positions)): #for each chunk ending we need to iterate and calculate number of words i.e ignore brackets+punctuation
        temp_count = 0
    #     print(linked_chunk_endings[i])
        for j in range(vgf_position-1,chunk_positions[i],-1):
            if words_in_sentence[j] not in string.punctuation and words_in_sentence[j]!='))' and words_in_sentence[j]!='((' and words_in_sentence[j]!='।' and words_in_sentence[j]!= '’':
                temp_count += 1
#                 print(words_in_sentence[j])
    #     print(temp_count)
        sum_distances += temp_count

    # print(sum_distances)
    return sum_distances

# print(linked_chunk_endings)


# In[148]:


file_path = input("Enter the path of the folder: ")
files = [file for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file))]
pattern = r'^(.+)\.([a-zA-Z0-9]+)$'
file_name = []
file_extension = []

for i in range(len(files)):
    match = re.match(pattern, files[i])
    if match:
        file_name.append(match.group(1))
        file_extension.append('.' + match.group(2))
    else:
        file_name.append(files[i])
        file_extension.append('')
different_words = []
for i in range(0,len(file_name)):
    print("Current file: "+file_name[i])
    os.makedirs(file_path + '\\' + file_name[i] + ' Variants', exist_ok=True)

    with open(file_path+"\\"+file_name[i]+file_extension[i],'r',encoding='utf-8') as file:
        file_contents = file.read()

    sentence_tags = sentence_creation(file_contents)
    for sentence in range(0,len(sentence_tags)):
        soup = BeautifulSoup(str(sentence_tags[sentence]), 'xml')
        sentence_id = soup.sentence['id']
        save_to_file = "Sentence ID: " + str(sentence_id) + "\n"
        original_sentence = ""
        df = create_df(sentence_tags[sentence])
        df = split_tags(df, 3)
        vgf_linked, last_vgf = linked_vgf(df)
        
        linked_chunk_endings = []
        for j in vgf_linked:
            # i = [48,49,50]
            linked_chunk_endings.append(df[1][j[-2:-1][0]])
        
        for j in range(last_vgf,len(df)):
            if df[1][j] == '))':
                last_vgf = j-1
                vgf_word = df[1][j-1]
                break
        
        permutations = list(itertools.permutations(vgf_linked))

        # Original sentence
        original = ' '.join(df[1])  # Joining all words in the original sentence

        original_sentence = "Sentence ID: " + str(sentence_id) + "\n"
        original_sentence += ''.join(re.findall(r'\(\(.*?\)\)', original)).translate(str.maketrans("", "", string.punctuation))

        variants = []
        dep_length = []
        for j in range(len(permutations)):
            temp = [item for sublist in permutations[j] for item in sublist]
#             print(original)
            result2 = ''.join(re.findall(r'\(\(.*?\)\)', original)).split(' ').copy()
#             print(result2)
            result2 = split_at_double_parentheses(result2)
#             print(result2)
            temp_permutation = fill_and_flatten(result2, permutations[j], vgf_linked)
            output = []
            for k in range(0,len(temp_permutation)):
                output.append(result2[temp_permutation[k]])
#             for k in range(0,len(output)):
#                 if output[k] == '))' or output[k] == '((':
#                     output[k] = ''
            #result2 = apply_permutation(result2, temp_permutation)
    #         result2 = ' '.join(result2).translate(str.maketrans("", "", string.punctuation)).split()
            variants.append(output)
#             print(output)
            dep_length.append(dependency_length(output, vgf_word, linked_chunk_endings))

        all_variants = [' '.join(variant) for variant in variants]
        flag = 0
        print("Original sentence: ",original_sentence, str(count_words(original_sentence.split())))
        for j in range(len(permutations)):
            save_to_file += all_variants[j] + '\t' + str(count_words(all_variants[j].split())+3) + '\t' + str(dep_length[j]) + '\n'
            if count_words(all_variants[j].split()) != count_words(original_sentence.split())-3:
                print("This variant has a different number of words: ", all_variants[j], count_words(all_variants[j].split()))
                different_words.append(sentence_id)
                flag = 1

#             if flag == 0:
#                 print("All variants have the same number of words")
        with open(file_path + '\\' + file_name[i] + " Variants\\Variants.txt", 'a', encoding='utf-8') as f:
            f.write("\n")
            f.write(save_to_file)
        with open(file_path + '\\' + file_name[i] + " Variants\\Original.txt", 'a', encoding='utf-8') as f:
            f.write("\n")
            f.write(original_sentence + '\t' + str(count_words(original_sentence.split())) + '\t' + str(dep_length[0]))


# In[101]:


input_text = "(( कोये से )) (( रेशे )) (( निकालने की )) (( क्रिया को )) (( ’ रीलिंग ’ )) (( ( reeling ) )) (( कहते हैं )) (( । ))"


# In[102]:


vgf_linked


# In[126]:


linked_chunk_endings = []
for i in vgf_linked:
    # i = [48,49,50]
    linked_chunk_endings.append(df[1][i[-2:-1][0]])


# In[127]:


for i in range(last_vgf,len(df)):
    if df[1][i] == '))':
        last_vgf = i-1
        vgf_word = df[1][i-1]
        break
print(vgf_word)


# In[ ]:





# In[139]:


print(linked_chunk_endings)
print(vgf_linked)
print(last_vgf)


# In[140]:


print(dependency_length(input_text.split(),vgf_word,linked_chunk_endings))


# In[141]:


input_text


# In[ ]:




