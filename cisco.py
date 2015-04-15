from Exscript.protocols import SSH2
from Exscript import Account

command = raw_input('Command? ')
account = Account('username', 'password')  

hosts_file = open('hostfile', 'r+')
for ipaddress in hosts_file:
    if ipaddress[0] is not "#":
        conn = SSH2()                       
        conn.connect(ipaddress)
        conn.login(account)

        conn.execute('terminal length 0')           

        conn.execute(command)
        print conn.response

        running_configuration = conn.response
        write_file = open(ipaddress+' '+command,'w')
        write_file.write(running_configuration)
        write_file.close()

        conn.send('exit\r')               
        conn.close()

hosts_file.close() 
