#!/usr/bin/env python
# coding: utf-8

# In[30]:


import os
import argparse


# In[29]:


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Folder path')
    args = parser.parse_args()
    file_path = args.path
    file_name = [folder for folder in os.listdir(file_path) if os.path.isdir(os.path.join(file_path, folder))]

    save_to_file_1 = ''
    save_to_file_2 = ''
    for i in range(0,len(file_name)):
    #     print("____________________")
        print("Current file: "+file_name[i])
        with open(file_path+"\\"+file_name[i]+"\\Variants.txt",'r',encoding='utf-8') as file:
            file_contents = file.read()
        lines = (file_contents.splitlines())
        sentence_id = 0
        for j in range(0,len(lines)):
            if "Sentence ID" in lines[j]:
    #             print(lines[j])
                index = lines[j].find("ID")
                sentence_id = int(lines[j][index+4:])
                decimal_part = -1
            elif lines[j] != '':
                decimal_part += 1
    #             print(decimal_part)
                sentence_id_float = str(str(sentence_id) + '.' + str(decimal_part))
                temp_index = file_name[i].find("Variants")
                final_sentence_id = file_name[i][:temp_index-1] + "__" + str(sentence_id_float)
    #             print(final_sentence_id)
                save_to_file_1 += final_sentence_id + '\t' + lines[j][:lines[j].find('\t')] + '\n'
                save_to_file_2 += final_sentence_id + '\t' + lines[j][lines[j].find('\t')+1:] + '\n'

    with open("Sentences.dat",'a',encoding='utf-8') as file:
            file.write(save_to_file_1)

    with open("Sentence_Data.dat",'a',encoding='utf-8') as file:
            file.write(save_to_file_2)


# In[ ]:


if __name__ == "__main__":
    main()

