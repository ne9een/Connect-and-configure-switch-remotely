import paramiko
import sys
import time
import subprocess
import threading
import pdb



HOST = "10.50.171.22"
USER = "advanced"
PASS = "ett,30"
PORT=2024
kill = False
stop = False

class progress_bar_loading(threading.Thread):
        def run(self):
                global stop
                global kill
                print 'loading....',
                sys.stdout.flush()
                i=0
                while stop!=True:
                        if (i%4) == 0:
                                sys.stdout.write('\b/')
                        elif (i%4) == 1:
                                sys.stdout.write('\b-')
                        elif (i%4) == 2:
                                sys.stdout.write('\b\\')
                        elif (i%4) == 3:
                                sys.stdout.write('\b|')
                        sys.stdout.flush()
                        time.sleep(0.2)
                        i+=1
                if kill == True:
                   print '\b\b\b\b ABORT!',
                else:
                   print '\b\b Done!',

def fetchvlan():
        print "please write the stack name"
        vlansName=raw_input()
        print "start to remove the L3 configuration for {}".format(vlansName)
        p.start()
        vlans= subprocess.Popen ("for i in $(neutron net-list|grep -v int \
                | grep -i {} | awk '{{print $2}}'); do neutron net-show $i \
            | grep -i segmentation|awk '{{print $4}}' ; done".format(vlansName), shell=True, \
            stdout=subprocess.PIPE).communicate()[0].strip().split('\n')
        return vlans

def fn():
        client1= paramiko.SSHClient()
        client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client1.connect(HOST,username=USER,password=PASS,port=PORT)
        print "SSH connection to %s established" %HOST
        remote_conn=client1.invoke_shell()
        vlans=fetchvlan()
        for i in vlans:
                remote_conn.send("\n")
                remote_conn.send("configure \n")
                ############### OM OSPF ##############
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-26-om_cn_vr,\
Ospfv2=ospfv2id-om_cn_vr,Area=area-0.0.1.1,Interface=if-0.0.1.1-{}\n".format(i))
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-28-om_cn_vr,\
Ospfv2=ospfv2id-om_cn_vr,Area=area-0.0.1.1,Interface=if-0.0.1.1-{}\n".format(i))
                remote_conn.send("commit \n")
                remote_conn.send("configure \n")
                ############### SIG OSPF ##############
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-26-sig_cn_vr,\
Ospfv2=ospfv2id-sig_cn_vr,Area=area-0.0.1.2,Interface=if-0.0.1.2-{}\n".format(i))
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-28-sig_cn_vr,\
Ospfv2=ospfv2id-sig_cn_vr,Area=area-0.0.1.2,Interface=if-0.0.1.2-{}\n".format(i))
                remote_conn.send("commit\n")
                remote_conn.send("configure \n")
                ############### OM Interface ##############
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-26-om_cn_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-28-om_cn_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("commit \n")
                remote_conn.send("configure \n")
                ############### SIG Interface ##############
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-26-sig_cn_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-28-sig_cn_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("commit\n")
                remote_conn.send("configure \n")
                ############### CORE Interface ##############
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-26-core_cn_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-28-core_cn_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("commit\n")
                remote_conn.send("configure \n")
                ############### ACC Interface ##############
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-26-fix_acc_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-28-fix_acc_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("commit\n")
                remote_conn.send("configure \n")
                ############### MOB Interface ##############
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-26-mob_acc_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("no ManagedElement=1,Transport=1,Router=0-28-mob_acc_vr,\
InterfaceIPv4=vlan1.{}\n".format(i))
                remote_conn.send("commit\n")
                remote_conn.send("configure \n")
                time.sleep(1)
                output =remote_conn.recv(10000)
                print output

        client1.close()

p= progress_bar_loading()
try:
        fn()
        time.sleep(1)
        stop=True
except KeyboardInterrupt or EOFError:
        kill= True
        stop= True
