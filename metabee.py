#!/usr/bin/python
# coding: utf-8
import re

class Metabee(object):
    '''
        Metabee massive email send with attachment.
    '''
    def __init__(self, file_path):
        '''
            Set a file path of txt, when has the main informations.
        '''
        self.file_path = file_path

    def parse(self):
        '''
            Parse the main informations and return a dictionary.
        '''

        file = open(self.file_path, 'rb')
        file_contents = file.read()
        file.close()

        file_patterns = {
            'title': '',
            'body': '',
            'list': ''
        }

        if file_contents:
            file_patterns_list = re.split(';\n', file_contents)

            if len(file_patterns_list) > 0:
                for line in file_patterns_list:
                    # Get title information
                    if '#Title:' in line:
                        if not file_patterns['title']:
                            file_patterns['title'] = re.sub('#Title:', '', line)
                    # Get body information
                    if '#Body:' in line:
                        if not file_patterns['body']:
                            file_patterns['body'] = re.sub('#Body:', '', line)
                    # Get list information
                    if '#List:' in line:
                        if not file_patterns['list']:
                                file_patterns['list'] = re.sub('#List:', '', line)
                                file_patterns['list'] = re.sub('\n', '', file_patterns['list'])
                
                # Remove white space in the init of elements
                for item in file_patterns:
                    file_patterns[item] = re.sub('^[\s]', '', file_patterns[item])
        
        if file_patterns:
            return file_patterns
    
if __name__ == '__main__':
    text = Metabee('files/tosend.txt')
    text.parse()
