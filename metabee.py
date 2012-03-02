#!/usr/bin/python
# coding: utf-8
from smtplib import *
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
            
            # Parse principal itens
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

    def brokenList(self):
        # List of informations when filtered
        profile = self.parse()
        oldlist = profile['list']
        newlist = []
        
        try:
            if oldlist and not newlist:
                oldlist = oldlist.split('),')
                for item in oldlist:
                    if item.startswith('('):
                        tempItem = re.sub('^[(]', '', item).split(',')
                    if tempItem[1].endswith(')'):
                        tempItem = [tempItem[0], re.sub('[)]$', '', tempItem[1])]
                    if tempItem[1].startswith(' '):
                        tempItem = [tempItem[0], re.sub('^[\s]', '', tempItem[1])]
                    
                    newlist.append(tempItem)

                profile['list'] = newlist
                
                return profile
        except Exception:
            return False

    def authAccount(self, addrs, email, password):
        try:
            if addrs and email and password:
                server = SMTP(addrs)
                
                if server.login(email, password):
                    return server
        except Exception:
            return False

    def mountMail(self, addrs, fromEmail, password, subject, toEmail, bodyMessage, pathfile):
        import pdb; pdb.set_trace()
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        from email.mime.multipart import MIMEMultipart

        server = self.authAccount(addrs, fromEmail, password)

        try:
            if addrs and password and subject and fromEmail and toEmail and bodyMessage and pathfile and server:
                message = MIMEMultipart()
                message['Subject'] = subject
                message['From'] = fromEmail
                message['To'] = toEmail

                # Preamble in message
                message.preamble = 'Multipart message.\n'

                # Message attach body text
                message.attach( MIMEText( bodyMessage ) )

                # Attach file type pdf
                archive = open(pathfile, 'rb')
                fileAttachment = MIMEApplication( archive.read() )
                fileAttachment.add_header('Content-Disposition', 'attachment', filename='{0}.pdf'.format(toEmail))
                # Attach file to the message
                message.attach(fileAttachment)

                log = server.sendmail( message['From'], message['To'], message.as_string())

                archive.close()
                server.quit()

                return log
        except Exception:
            return False

    def sendMail(self, addrs, email, password):
        import pdb; pdb.set_trace()
        profile = self.brokenList()
        log = []

        try:
            if profile and not log:
                for item in profile['list']:
                    item[0] = re.sub('\'', '', item[0])
                    item[0] = re.sub('\"', '', item[0])
                    item[0] = str(item[0])

                    if item[1]:
                        item[1] = re.sub('\'', '', item[1])
                        item[1] = re.sub('\"', '', item[1])
                        item[1] = str(item[1])

                    log.append( self.mountMail(addrs, email, password, profile['title'], item[0], profile['body'], item[1]) )
                return log
        except Exception:
            return False

if __name__ == '__main__':
    sender = Metabee('files/tosend.txt')
    print sender.sendMail('smtp.terra.com.br', 'kaique@editoraphoenix.com.br', 'ka0237')

