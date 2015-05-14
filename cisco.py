#Import libs
from Exscript.protocols import SSH2
from Exscript import Account
import socket
import os
import datetime

#User info
command = raw_input('Command? ')
account = Account('username', 'password')  
date = str(datetime.date.today())

#Translate hostfile and connect to IP
hosts_file = open('hostfile', 'r+')
for host in hosts_file:
    if '#' not in host:
        ipaddress = socket.gethostbyname(host.strip())
        conn = SSH2()                       
        conn.connect(ipaddress)
        conn.login(account)

        conn.execute('terminal length 0')           

        conn.execute(command)
        print conn.response

        #Saving output
        path = command + ' ' + date + '/'
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        os.chdir(path)
        running_configuration = conn.response
        write_file = open(host+'_'+command,'w')
        write_file.write(running_configuration)
        write_file.close()
        os.chdir('..')
        conn.send('exit\r')               
        conn.close()

hosts_file.close() 
