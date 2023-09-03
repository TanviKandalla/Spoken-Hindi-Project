from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import os
def returnString(text,sentence_id,file_name):
    data = StringIO(text)
    df = pd.read_csv(data, sep='\t', header=None)
    df = df.fillna(' ')
    string = ''
    for i in range(0,len(df)):
        if df[1][i] != '((' and df[1][i] != '))':
            string += df[1][i] + ' '

    string = file_name + '_'+ str(sentence_id) + ' \t ' + string
    return string

def modifyFiles(file_path, file_name,extension):
    with open(file_path+"\\"+file_name+extension,'r',encoding='utf-8') as file:
        file_contents = file.read()

    # Create a Beautiful Soup object
    soup = BeautifulSoup(file_contents, 'html.parser')

    # Find all <text> tags and extract their content
    sentence_tags = soup.find_all('sentence')
    new_string = ''
    for i in range(0,len(sentence_tags)):
        temp = returnString(sentence_tags[i].text, sentence_tags[i]['id'],file_name)
        new_string += temp + '\n'
    # Open the file in write mode and write the new format string
    with open(file_path+"\\Modified Files\\"+file_name+'.txt', 'w', encoding = 'utf-8') as file:
        file.write(new_string)
    return

def main():
    file_path = input("Path of the folder with files to be converted: ")
    files = os.listdir(file_path)
    os.mkdir(file_path+"\\Modified Files")
    for i in files:
        file_name, file_extension = os.path.splitext(i)

        modifyFiles(file_path, file_name, file_extension)


  
if __name__=="__main__":
    main()