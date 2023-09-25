from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import os
import csv

def returnString(text, sentence_id, file_name):
    data = StringIO(text)
    df = pd.read_csv(data, sep='\t', header=None, quoting=csv.QUOTE_NONE)
    df = df.fillna(' ')
    string = ''
    for i in range(0, len(df)):
        if df[1][i] != '((' and df[1][i] != '))':
            string += df[1][i] + ' '
    string = file_name + '_' + str(sentence_id) + ' \t ' + string
    return string

def modifyFiles(input_folder, output_folder):
    files = os.listdir(input_folder)
    os.makedirs(output_folder, exist_ok=True)
    for file_name in files:
        if file_name == "Modified Files":
            continue
        base_name, file_extension = os.path.splitext(file_name)
        file_path = os.path.join(input_folder, file_name)
        output_file_name = base_name + '_modified.txt'
        output_file_path = os.path.join(output_folder, output_file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        
        soup = BeautifulSoup(file_contents, 'html.parser')
        sentence_tags = soup.find_all('sentence')
        new_string = ''
        
        for sentence_tag in sentence_tags:
            temp = returnString(sentence_tag.text, sentence_tag['id'], base_name)
            new_string += temp + '\n'
        
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(new_string)
        print("Done with ", file_path)

def main():
    input_folder = input("Enter the path of the input folder:")
    output_folder = input_folder + '\Modified Files'

    modifyFiles(input_folder, output_folder)

if __name__ == "__main__":
    main()
