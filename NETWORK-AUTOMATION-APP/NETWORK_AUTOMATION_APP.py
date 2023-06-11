from netmiko import ConnectHandler
import pyfirmata
from pyfirmata import Arduino, util, STRING_DATA
import cv2
import numpy as np
import face_recognition
import os
import sys
import time

############################################ ARDUINO COMPONENT CONFIGURATION ########################################################
#####################################################################################################################################

board = pyfirmata.Arduino('COM7')
red_led1 = board.digital[4]             #NETWORK STABILITY
green_led1 = board.digital[5]           #NETWORK ACCESS CONTROL
red_led2 = board.digital[2]             #NETWORK ACCESS CONTROL
green_led2 = board.digital[3]           #NETWORK STABILITY


################################################## SUCCESSFUL ACCESS ################################################################
successful_login1 = "ADMIN.ZARKA"
successful_login2 = "SUCCESFUL ACCESS"
def successful_access (board, green_led1, successful_login1, successful_login2):
    green_led1.write(1)
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(successful_login1))
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(successful_login2))


#################################################### CONFIGURATION STATUS ##########################################################
config_status1 = "SUCCESSFUL"
config_status2 = "CONFIGURATION!!"

def successful_config(board, green_led2, config_status1, config_status2) :
    green_led2.write(1)
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(config_status1))
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(config_status2))


####################################################### DENIED ACCESS ###############################################################
buzzer = board.digital[7]
Button = board.digital[8]
iteration = pyfirmata.util.Iterator(board)
iteration.start()
Button.mode = pyfirmata.INPUT
alert1 = " ALERT ATTACK!!"
def access(board, alert1):
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(alert1))


################################################# NETWORK AUTOMATION CONFIGURATION ##################################################
#####################################################################################################################################

##################################################### SET OF THE FUNCTIONS ##########################################################

# SSH CONFIGURATION FUNCTION
def remote_login_ssh():
    ip_addr = str(input("Set the IP_ADDR of the remote device:\n"))
    username = str(input("Set the username:\n"))
    password = str(input("Set the password:\n"))
    secret_password = str(input("Set the secret_password:\n"))  
    Network_Device = {
        'ip' : ip_addr,
        'username' : username,
        'password' : password,
        'device_type' : 'cisco_ios',
        'secret' : secret_password
    }
    return Network_Device

# IP ADDRESS CONFIGURATION
def ip_addr_config():
    nbr_interface = int(input("Set the number of interfaces we want to configure:\n"))
    print(ssh_connection._send_command_timing_str("configure terminal\n"))
    for nbr in range (1, (nbr_interface+1)):
        interface_name = str(input("Set the interface name:\n"))
        ip_addr = str(input("Set IP address:\n"))
        mask = str(input("Set the mask:\n"))
        print(ssh_connection._send_command_timing_str(f"interface {interface_name}\n"))
        print(ssh_connection._send_command_timing_str(f"ip address {ip_addr} {mask}\n"))
        print(ssh_connection._send_command_timing_str("no shutdown\n"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("end\n"))
    print(ssh_connection._send_command_timing_str("copy running-config startup-config\n"))

# OSPF ROUTING PROTOCOL CONFIGURATION
def ospf_config():
    nbr_networks = int(input("Set the number of networks we want to configure with OSPF:\n"))
    for nbr in range(1, (nbr_networks+1)):
        network_id = str(input("Set the network ID:\n"))
        wild_card_mask = str(input("Set the wild card mask:\n"))
        print(ssh_connection._send_command_timing_str("configure terminal\n"))
        print(ssh_connection._send_command_timing_str("router ospf 1\n"))
        print(ssh_connection._send_command_timing_str(f"network {network_id} {wild_card_mask} area 0\n"))
    print(ssh_connection._send_command_timing_str("end\n"))
    print(ssh_connection._send_command_timing_str("copy running-config startup_config\n"))

# VTP CONFIGURATION FUNCTION
def vtp_config():
    vtp_mode = input("Set VTP mode:\n")
    vtp_domain = input("Set VTP domain:\n")
    vtp_password = input("Set VTP password:\n")
    print(ssh_connection._send_command_timing_str("configure terminal\n"))
    print(ssh_connection._send_command_timing_str(f"vtp mode {vtp_mode}\n"))
    print(ssh_connection._send_command_timing_str("vtp version 2\n"))
    print(ssh_connection._send_command_timing_str(f"vtp domain {vtp_domain}\n"))
    print(ssh_connection._send_command_timing_str(f"vtp password {vtp_password}\n"))
    print(ssh_connection._send_command_timing_str("end\n"))
    print(ssh_connection._send_command_timing_str("copy running-config startup-config\n"))

# VLAN CONFIGURATION FUNCTION
def vlan_config():
    vlan_nbr = int(input("Set the number of vlan's we want to create:\n"))
    print(ssh_connection._send_command_timing_str("configure terminal\n"))
    for vlan in range (1,(vlan_nbr+1)):
        vlan=(vlan+1)
        print(ssh_connection._send_command_timing_str(f"vlan {vlan}\n"))
        print(ssh_connection._send_command_timing_str(f"name vlan{vlan}\n"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("end\n"))

# VLAN NATIVE CONFIG FUNCTION
def vlan_native():
    print(ssh_connection._send_command_timing_str("configure terminal\n"))
    print(ssh_connection._send_command_timing_str("vlan 99\n"))
    print(ssh_connection._send_command_timing_str("name native\n"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("end\n"))

# SWITCHPORT TRUNK MODE FUNCTION
def switchport_trunk():
    nbr_interface = int(input("Set how many Interfaces we want to configure as trunk mode:\n"))
    print(ssh_connection._send_command_timimg_str("configure terminal\n"))
    for nbr in range(1, (nbr_interface+1)):
        f_name = str(input("Set Interface name:\n"))
        print(ssh_connection._send_command_timing_str(f"interface {f_name}\n"))
        print(ssh_connection._send_command_timing_str("switchport trunk encapsulation dot1q\n"))
        print(ssh_connection._send_command_timing_str("switchport mode trunk\n"))
        print(ssh_connection._send_command_timing_str("switchport trunk native vlan 99\n"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("end\n"))

# SWITCHPORT ACCESS MODE FUNCTION
def switchport_access():
    nbr_interface = int(input("Set how many Interfaces you want to configure as access mode:\n"))
    print(ssh_connection._send_command_timing_str("configure terminal\n"))
    for nbr in range(1, (nbr_interface+1)):
        f_name = str(input("Set Interface name:\n"))
        vlan_ID = int(input("Set the vlan_ID:\n"))
        print(ssh_connection._send_command_timing_str(f"interface {f_name}\n"))
        print(ssh_connection._send_command_timing_str("switchport mode access\n"))
        print(ssh_connection._send_command_timing_str(f"switchport access vlan {vlan_ID}"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("end\n"))

# STP AND ETHERCHANNEL FUNCTION
def stp_etherchannel():
    print(ssh_connection._send_command_timing_str("configure terminal\n"))
    print(ssh_connection._send_command_timing_str("spanning-tree mode pvst\n"))
    interface_range = str(input("Set the interface range:\n"))
    print(ssh_connection._send_command_timing_str(f"interface range {interface_range}\n"))
    print(ssh_connection._send_command_timing_str("channel-group 1 mode active\n"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("interface port-channel1\n"))
    print(ssh_connection._send_command_timing_str("switchport trunk encapsulation dot1q\n"))
    print(ssh_connection._send_command_timing_str("switchport mode trunk\n"))
    print(ssh_connection._send_command_timing_str("switchport trunk native vlan 99\n"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("end\n"))

# SVI INTERFACES CONFIGURATION FUNCTION
def svi_inter():
    nbr_svi = int(input("Set the number of SVI interfaces you want to configure:\n"))
    print(ssh_connection._send_command_timing_str("configure terminal\n"))
    for nbr in range (1, (nbr_svi+1)):
        svi_name = str(input("Set the name of SVI interface:\n"))
        ip_addr = str(input("Set the IP address:\n"))
        mask = str(input("Set the IP address mask:\n"))
        print(ssh_connection._send_command_timing_str(f"interface {svi_name}\n"))
        print(ssh_connection._send_command_timing_str(f"ip address {ip_addr} {mask}\n"))
        print(ssh_connection._send_command_timing_str("no shutdown\n"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("end\n"))

# DHCP CONFIGURATION FUNCTION
def dhcp_config():
    print(ssh_connection._send_command_timing_str("configure terminal\n"))
    nbr_dhcp_config = int(input("Set how many times we want to configure DHCP:\n"))
    for nbr in range(1, (nbr_dhcp_config+1)):
        # DHCP INFORMATIONS SERVER
        excluded_addr = str(input("Set the excluded_address from the range:\n"))
        pool_name = str(input("Set the pool name:\n"))
        network_id = str(input("Set the network ID:\n"))
        subnet = str(input("Set the subnet mask:\n"))
        gateway = str(input("Set the gateway:\n"))
        dns_server = str(input("set the DNS_SERVER IP address:\n"))
        # DHCP CONFIG
        print(ssh_connection._send_command_timing_str(f"ip dhcp excluded-address {excluded_addr}\n"))
        print(ssh_connection._send_command_timing_str(f"ip dhcp pool {pool_name}\n"))
        print(ssh_connection._send_command_timing_str(f"network {network_id} {subnet}\n"))
        print(ssh_connection._send_command_timing_str(f"default-router {gateway}\n"))
        print(ssh_connection._send_command_timing_str(f"dns-server {dns_server}\n"))
    print(ssh_connection._send_command_timing_str("exit\n"))
    print(ssh_connection._send_command_timing_str("end\n"))

# VERIFY CONFIGURATION OF L3 SWITCHES
def L3sw_verify_config():
    print(str("#"*int(65)) + " VERIFY THE CONFIGURATION " + str("#"*int(65)))
    print(ssh_connection._send_command_timing_str("show ip interface brief\n"))
    print(str("#"*int(149)))
    print(ssh_connection._send_command_timing_str("show vlan brief\n"))
    print(str("#"*int(149)))
    print(ssh_connection._send_command_timing_str("show vtp status\n"))
    print(str("#"*int(149)))
    print(ssh_connection._send_command_timing_str("show ip route\n"))
    print(str("#"*int(149)))
    print(ssh_connection._send_command_timing_str("copy running-config startup-config\n"))
    time.sleep(3)
    print(str("#"*int(55)) + " SUCCESSFUL VERIFICATION!! " + str("#"*int(55)))
    print("\n")

# VERIFY CONFIGURATION OF L2 SWITCHS
def L2sw_verify_config():
    print(str("#"*int(65))+" VERIFY THE CONFIGURATION "+str("#"*int(65)))
    print(ssh_connection._send_command_timing_str("show ip interface brief\n"))
    print(str("#"*int(149)))
    print(ssh_connection._send_command_timing_str("show vlan brief\n"))
    print(str("#"*int(149)))
    print(ssh_connection._send_command_timing_str("show vtp status\n"))
    print(str("#"*int(149)))
    time.sleep(2)
    print(str("#"*int(55))+" SUCCESSEFUL VERIFICATION!! "+str("#"*int(55)))
    print("\n")


######################################################## FACE RECOGNITION ###########################################################
#####################################################################################################################################

###################################################### SET OF THE FACE RECOGNITION ##################################################

# set the path of the directory who contain the pictures
dir_path = "C:\\Users\\who_I_am\\Desktop\\NETWORK_AUTOMATION\\admins\\"
# make a list to stock the pictures on it 
images = []
# make a list to stock the names of the pictures on it
Names = []
# stock the path of each picture who exist under users_pictures directory in personList variable
personsList = os.listdir(dir_path)

# for loop to make itteration over all the pictures inside users_pictures directory
for pic in personsList:
    # read and save the pictures in r_picture
    r_picture = cv2.imread(f'{dir_path}/{pic}')
    # append the saved pictures in r_picture variable in images list
    images.append(r_picture)
    # name of the picture is taken with the extension too, we want just the name without extension ==> use os.path.splitext() to remove it
    # save the names under Names list without extensions
    Names.append(os.path.splitext(pic)[0])

# create a function to make encoding of the pictures under users_pictures by using face_recognation
# to describe the coordinations of the faces in the pictures

def getEncodings(image):
    # create a list to save the pictures encodings
    encodeList = []
    # make an iterration over the pictures stared in the images list
    for img in images:
        # read the pictures and convert them from BGR to RGB
        # face_recognation necessite RGB pictures
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# save all the pictures encodings in a variable
encodeListKnown = getEncodings(images)

# set the camera
cam = cv2.VideoCapture(0)

############################################### SET OF THE FACE RECOGNITION FUNCTION ################################################

def face_recog(encodeListKnown, cam) :
    for t in range (10, 0, -1):
        ret, img = cam.read()
         # Resize the frames taken from the video
        imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
        # convert the color of the captured farmes from BGR to RGB
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        # make encoding to the captured frame from the video 
        faceCurentFrame = face_recognition.face_locations(imgS)
        encodeCurentFrame = face_recognition.face_encodings(imgS, faceCurentFrame)

        for encodeface, faceLoc in zip(encodeCurentFrame, faceCurentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeface)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
            # the lower value define the right picture by using numpy library
            matchIndex = np.argmin(faceDis)
            # in this bloc we set the name and the rectangle of the over the face of the user
            if matches[matchIndex]:
                name = Names[matchIndex].upper()
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
                cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,0,255), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 2)
                cv2.imshow('Face_recognition', img)
                cv2.waitKey(1)
            
            else :
                name = "NOT.ADMIN".upper()
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
                cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,0,255), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 2)
                cv2.imshow('Face_recognition', img)
                cv2.waitKey(1)
    cv2.destroyAllWindows()
    return name

##################################### START THE NETWORK AUTOMATION BY USING FACE RECOGNITION ########################################
#####################################################################################################################################

####################################### ASK THE USER WHAT NETWORK DEVICE HE WANT TO CONFIGURE #######################################

def network_device():
    net_device = input("""PLEASE SET A NUMBER CORRESPENDING TO THE NETWORK DEVICE THAT YOU WANT TO CONFIGURE:\n
                            1*CISCO_ROUTER\n
                            2*L2_CISCO_SWITCH\n
                            3*L3_CISCO_SWITCH\n
                            4*FIREWALL\n""")
    return net_device

def select_router_config():
    router_config = input("""PLEASE SET A NUMBER CORRESPONDING TO THE CONFIGURATION THAT YOU WANT TO CONFIGURE:\n
                                1*IP ADDRESS\n
                                2*OSPF PROTOCOL\n
                                3*DHCP PROTOCOL\n""")
    return router_config

def select_L2_switch_config():
    L2_switch_config = input("""PLEASE SET THE NUMBER CORRESPONDING TO THE CONFIGURATION THAT YOU WANT TO CONFIGURE:\n
                                    1*VTP_CONFIG\n
                                    2*VLAN_CONFIG\n
                                    3*VLAN_NATIVE\n
                                    4*TRUNK_MODE\n
                                    5*ACCESS_MODE\n
                                    6*STP_AND_ETHERCHANNEL\n
                                    7*VERIFY_CONFIG\n""")
    return L2_switch_config

def select_L3_switch_config():
    L3_switch_config = input("""PLEASE SET THE NUMBER CORRESPONDING TI THE CONFIGURATION THAT YOU WANT TO CONFIGURE:\n
                                    1*VTP_CONFIG\n
                                    2*VLAN_CONFIG\n
                                    3*VLAN_NATIVE\n
                                    4*TRUNK_MODE\n
                                    5*ACCESS_MODE\n
                                    6*ACCESS_MODE\n
                                    7*STP_AND_ETHERCHANNEL\n
                                    8*SVI_INTERFACES\n
                                    9*DHCP\n
                                    10*VERIFY_CONFIG\n""")
    return L3_switch_config

device = network_device()
###################################################### ROUTER ################################################################
if (device == "1"):
    print(str("#"*int(20))+" ROUTER CONFIGURATION: "+str("#"*int(20)))
    #--------------------------------------REMOTE ACCESS VIA SSH AND FACE RECOGNITION-----------------------------------------
    ssh_connection = ConnectHandler(**remote_login_ssh())
    name = face_recog(encodeListKnown, cam)
    if (name != "NOT.ADMIN") :
        successful_access(board, green_led1, successful_login1, successful_login2)
        ssh_connection.enable()
        print(str("#"*int(65))+ " SSH SESSION OPENED SUCCESSFULLY " + str("#"*int(65)))
        print("\n")
        r_config = select_router_config()
        while True :
            if (r_config == "1"):
                print(str("#"*int(20))+" IP ADDRESS CONFIGURATION "+str("#"*int(20)))
                ip_addr_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (r_config == "2"):
                print(str("#"*int(20))+" OSPF CONFIGURATION "+str("#"*int(20)))
                ospf_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (r_config == "3"):
                print(str("#"*int(20))+" DHCP CONFIGURATION "+str("#"*int(20)))
                dhcp_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            rproto_change_config = input("DO YOU WANT TO CONFIGURE OTHER ROUTER PROTOCOL: [Y/N]\n")
            if (rproto_change_config == "Y"):
                r_config = select_router_config()
            elif (rproto_change_config == "N"):
                break
    #-----------------------------------------CLOSE SSH SESSION-----------------------------------------------------------
        ssh_connection.disconnect()
        print(str("#"*int(65)) + " SSH SESSION CLOSED " + str("#"*int(65)))
        print("\n")        
    elif (name == "NOT.ADMIN"):
        red_led2.write(1)
        buzzer.write(1)
        access(board, alert1)
        while True : 
            Button_state = Button.read()
            print(Button_state)
            if Button_state is True :
                red_led2.write(0)
                buzzer.write(0)
                break
        time.sleep(1)
        exit("NOT ADMIN ACCESS DENIED!!!!")
##################################################### L2 SWITCH #################################################################
elif (device == "2"):
    print(str("#"*int(20))+" L2 SWITCH CONFIGURATION: "+str("#"*int(20)))
    #--------------------------------------- REMOTE ACCESS VIA SSH AND FACE RECOGNITION -----------------------------------------
    ssh_connection = ConnectHandler(**remote_login_ssh())
    name = face_recog(encodeListKnown, cam)
    if (name != "NOT.ADMIN") :
        successful_access(board, green_led1, successful_login1, successful_login2)
        ssh_connection.enable()
        print(str("#"*int(65))+ " SSH SESSION OPENED SUCCESSFULLY " + str("#"*int(65)))
        print("\n")
        s2_config = select_L2_switch_config()
        while True :
            if (s2_config == "1"):
                print(str("#"*int(20))+" VTP PROTOCOL CONFIGURATION "+str("#"*int(20)))
                vtp_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL VTP CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s2_config == "2"):
                print(str("#"*int(20))+" VLAN PROTOCOL CONFIGURATION "+str("#"*int(20)))
                vlan_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSUFUL VLAN CONFIGURATION!! ")
                print("\n")
            elif (s2_config == "3"):
                print(str("#"*int(20))+" VLAN NATIVE CONFIGURATION "+str("#"*int(20)))
                vlan_native()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL NATIVE VLAN CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s2_config == "4"):
                print(str("#"*int(20))+" TRUNK MODE CONFIGURATION "+str("#"*int(20)))
                switchport_trunk()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL TRUNK MODE CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s2_config == "5"):
                print(str("#"*int(20))+" ACCESS MODE CONFIGURATION "+str("#"*int(20)))
                switchport_access()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL ACCESS MODE CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s2_config == "6"):
                print(str("#"*int(20))+" STP AND ETHERCHANNEL CONFIGURATION "+str("#"*int(20)))
                stp_etherchannel()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL STP AND ETHERCHANNEL CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s2_config == "7"):
                print(str("#"*int(20))+" L2 SWITCH VERIFY CONFIGURATION "+str("#"*int(20)))
                L2sw_verify_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print("\n")
            s2_proto_change_config = input("DO YOU WANT TO CONFIGURE OTHER ROUTER PROTOCOL: [Y/N]\n")
            if (s2_proto_change_config == "Y"):
                s2_config = select_L2_switch_config()
            elif (s2_proto_change_config == "N"):
                break
        #----------------------------------------------- CLOSE SSH SESSION ------------------------------------------------------
        ssh_connection.disconnect()
        print(str("#"*int(65)) + " SSH SESSION CLOSED " + str("#"*int(65)))
        print("\n")
    elif (name == "NOT.ADMIN"):
        red_led2.write(1)
        buzzer.write(1)
        access(board, alert1)
        while True : 
            Button_state = Button.read()
            print(Button_state)
            if Button_state is True :
                red_led2.write(0)
                buzzer.write(0)
                break
        time.sleep(1)
        exit("NOT ADMIN ACCESS DENIED!!!!")

########################################################## L3 SWITCH ###########################################################
elif (device == "3"):
    print(str("#"*int(20))+" L3 SWITCH CONFIGURATION "+str("#"*int(20)))
    #---------------------------------------- REMOTE ACCESS VIA SSH AND FACE RECOGNITION ---------------------------------------
    ssh_connection = ConnectHandler(**remote_login_ssh())
    name = face_recog(encodeListKnown, cam)
    if (name != "NOT.ADMIN") :
        successful_access(board, green_led1, successful_login1, successful_login2)
        ssh_connection.enable()
        print(str("#"*int(65))+ " SSH SESSION OPENED SUCCESSFULLY " + str("#"*int(65)))
        print("\n")
        s3_config = select_L3_switch_config()
        while True :
            if (s3_config == "1"):
                print(str("#"*int(20))+" VTP PROTOCOL CONFIGURATION "+str("#"*int(20)))
                vtp_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL VTP PROTOCOL CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s3_config == "2"):
                print(str("#"*int(20))+" VLAN CONFIGURATION "+str("#"*int(20)))
                vlan_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL VLAN CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s3_config == "3"):
                print(str("#"*int(20))+" VLAN NATIVE CONFIGURATION "+str("#"*int(20)))
                vlan_native()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL VLAN NATIVE CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s3_config == "4"):
                print(str("#"*int(20))+" TRUNK MODE CONFIGURATION "+str("#"*int(20)))
                switchport_trunk()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL TRUNK MODE CONFIGURATION!! "+str("#"*int(20)))
            elif (s3_config == "5"):
                print(str("#"*int(20))+" ACCESS MODE CONFIGURATION "+str("#"*int(20)))
                switchport_access()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL ACCESS MODE CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s3_config == "6"):
                print(str("#"*int(20))+" STP AND ETHERCHANNEL CONFIGURATION "+str("#"*int(20)))
                stp_etherchannel()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL STP AND ETHERCHANNEL CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s3_config == "7"):
                print(str("#"*int(20))+" SVI INTERFACES CONFIGURATION "+str("#"*int(20)))
                svi_inter()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL SVI INTERFACES CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s3_config == "8"):
                print(str("#"*int(20))+" DHCP PROTOCOL CONFIGURATION: "+str("#"*int(20)))
                dhcp_config()
                successful_config(board, green_led2, config_status1, config_status2)
                print(str("#"*int(20))+" SUCCESSEFUL DHCP PROTOCOL CONFIGURATION!! "+str("#"*int(20)))
                print("\n")
            elif (s3_config == "9"):
                print(str("#"*int(20))+" L3 CONFIGURATION VERIFICATION "+str("#"*int(20)))
                L3sw_verify_config()
                successful_config()
                print(str("#"*int(20))+" SUCCESSEFUL L3 SWITCH VERIFICATION!! "+str("#"*int(20)))
                print("\n")
            s3_proto_change_config = input("DO YOU WANT TO CONFIGURE OTHER ROUTER PROTOCOL: [Y/N]\n")
            if (s3_proto_change_config == "Y"):
                s3_config = select_L3_switch_config()
            elif (s3_proto_change_config == "N"):
                break
    #-------------------------------------------------- CLOSE SSH SESSION ---------------------------------------------------------
        ssh_connection.disconnect()
        print(str("#"*int(65)) + " SSH SESSION CLOSED " + str("#"*int(65)))
        print("\n")
    elif (name == "NOT.ADMIN"):
        red_led2.write(1)
        buzzer.write(1)
        access(board, alert1)
        while True : 
            Button_state = Button.read()
            print(Button_state)
            if Button_state is True :
                red_led2.write(0)
                buzzer.write(0)
                break
        time.sleep(1)
        exit("NOT ADMIN ACCESS DENIED!!!!")    

restart = sys.executable
os.execl(restart, restart, * sys.argv)
