from netmiko import ConnectHandler
import pyfirmata
from pyfirmata import Arduino, util, STRING_DATA
import time
import os
import sys

board = pyfirmata.Arduino('COM7')
green_led2 = board.digital[3]
red_led1 = board.digital[4]
buzzer = board.digital[7]
Button = board.digital[8]
iteration = pyfirmata.util.Iterator(board)
iteration.start()
Button.mode = pyfirmata.INPUT

def stable_network(board, status1):
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(status1))

def unstable_network(board, status2):
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(status2))

Network_Device = {
    'ip' : '10.200.106.80',
    'username' : 'admin_zarka',
    'password' : 'cisco1',
    'device_type' : 'cisco_ios',
    'secret' : 'cisco1'
}

ssh_connection = ConnectHandler(**Network_Device)
ssh_connection.enable()

interface_list = ["f1/0", "f0/0", "f0/1"]
for interface in interface_list :
    output_command = ssh_connection._send_command_timing_str(f"show interfaces {interface}\n")
    # Retrieve just the 1st line of the output_command
    output_command_1stline = output_command.splitlines()[0]
    # Convert the 1st line of the output_command to a list
    output_command_1stline_to_list = list(output_command_1stline.split(","))
    # Retrieve the 1st element of the output_command_1stline_to_list list and turn it to a list
    output_command_1stline_1stelement_to_list = list(output_command_1stline_to_list[0].split(" "))
    print(output_command_1stline_1stelement_to_list)
    for find in output_command_1stline_1stelement_to_list[0:]:
        if find == "up" :
            print(f"{interface} interface is up\n")
            status1 = (f"R1: {interface} is up")
            green_led2.write(1)
            stable_network(board, status1)
        elif find == "down" :
            print(f"{interface} interface is down")
            green_led2.write(0)
            red_led1.write(1)
            buzzer.write(1)
            status2 = (f"R1: {interface} is down")
            unstable_network(board, status2)
            while True : 
                Button_state = Button.read()
                print(Button_state)
                if Button_state is True :
                    red_led1.write(0)
                    buzzer.write(0)
                    break
                time.sleep(1)
    print(str("#"*int(150)))
    print(str("#"*int(150)))

restart = sys.executable
os.execl(restart, restart, * sys.argv)

#ssh_connection.disconnect()