from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import os

def returnString(text, sentence_id, file_name):
    data = StringIO(text)
    df = pd.read_csv(data, sep='\t', header=None)
    df = df.fillna(' ')
    string = ''
    for i in range(0, len(df)):
        if df[1][i] != '((' and df[1][i] != '))':
            string += df[1][i] + ' '
    string = file_name + '_' + str(sentence_id) + ' \t ' + string
    return string

def modifyFiles(input_folder, output_folder):
    files = os.listdir(input_folder)
    print(files)
    os.makedirs(output_folder, exist_ok=True)
    for file_name in files:
        print(file_name)
        base_name, file_extension = os.path.splitext(file_name)
        file_path = os.path.join(input_folder, file_name)
        output_file_name = base_name + '_modified.txt'
        output_file_path = os.path.join(output_folder, output_file_name)
        print(output_file_path)
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

def main():
    input_folder = input("Enter the path of the input folder:")
    output_folder = input_folder + '\Modified Files'

    modifyFiles(input_folder, output_folder)

if __name__ == "__main__":
    main()
