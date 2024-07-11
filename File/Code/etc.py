import os 
import random
import uuid

from ESXi_config import create_config_file
from ESXi_config import create_directory
from ESXi_config import create_ssh_keys
from ESXi_config import create_sshd_config
from ESXi_config import create_hosts_file
from ESXi_config import create_vmware_lic
from ESXi_config import create_passwd_file
from ESXi_config import generate_random_string

def create_esx_etc(etc_path="/ESXI 7/etc/"):
# Thư mục /etc/vmware
    vmware_path = os.path.join(etc_path, "vmware")

    #Folder vmwauth
    vmwauth_path = '/ESXI 7/etc/vmware/vmwauth/'
    create_config_file(vmwauth_path,"authentication.conf",generate_random_string(10))
    create_config_file(vmwauth_path,"camprovider.conf",generate_random_string(10))
    create_config_file(vmwauth_path,"provider.conf",generate_random_string(10))

    #Folder default-config
    default = os.path.join(vmware_path,"default-config")
    create_config_file(default,"esx-base-7.0.3_0.50.20036589-default.json",generate_random_string(10))

    #Folder stats.d
    create_config_file(os.path.join(vmware_path,"stats.d"),"esxtokend.conf",generate_random_string(10))

    #Folder service
    service_path = '/ESXI 7/etc/vmware/service/'
    create_config_file(service_path,"dpd-service.xml",generate_random_string(12))
    create_config_file(service_path,"likewise.xml",generate_random_string(12))
    create_config_file(service_path,"service.xml",generate_random_string(12))
    create_config_file(service_path,"vltd-service.xml",generate_random_string(12))

    # Tạo file esx.conf
    esx_conf_content = f"""# ESXi Configuration File
hostname = "esxi-{random.randint(1, 10)}.example.com"
hostname = "prod-esxi-02.domain.com"
hostname = "esxi-{random.randint(1, 10)}.example.com"
# Cấu hình mạng giả mạo
/net/ipv4/interfaces/vmk0/ipAddress = "10.10.10.100"
/net/ipv4/interfaces/vmk0/subnetMask = "255.255.255.0"
/net/ipv4/gateway = "10.10.10.1"
net.dns.servers = "1.1.1.1, 8.8.8.8"
net.ipv4.tcp_syncookies = {random.randint(0, 1)}
net.ipv4.tcp_timestamps = {random.randint(0, 1)}
vmkernel.boot.diskUUID = "{generate_random_string(36)}"
vmkernel.boot.diskDevice = "{generate_random_string(10)}"
vmkernel.boot.diskType = "{random.choice(['disk', 'cdrom'])}"
vmkernel.boot.diskPath = "{generate_random_string(20)}"
# Phiên bản ESXi giả mạo (cũ hơn, có thể chứa lỗ hổng)
/product/version = "6.7.0" 
/product/build = "14320388"

# Vô hiệu hóa SSH (hoặc thay đổi cổng)
/system/services/ssh/enabled = "0" 
# /system/services/ssh/port = "2222"

# Cấu hình SNMP giả mạo
/snmp/enabled = "1"
/snmp/community = "public" 

# Thêm thông tin giả mạo (có thể ẩn trong comment)
# FAKE_FLAG = "Ransomware_Deception"
# BACKUP_SERVER = "10.10.10.200"
# ADMIN_PASSWORD = "password123"
    """
    create_config_file(vmware_path, "esx.conf", esx_conf_content)

    # Tạo file encryption.info
    encryption_content = f""".encoding = "UTF-8"
includeKeyCache = "FALSE"
mode = "NONE"
ConfigEncData = "keyId={generate_random_string(24)}%3d%3d:data1={generate_random_string(20)}/{generate_random_string(3)}%3d%3d:data2=+{generate_random_string(6)}/{generate_random_string(18)}%3d%3d:version=1"
"""
    create_config_file(vmware_path, "encryption.info", encryption_content)

    # Tạo file vmware/firewall/service.xml
    firewall_path = os.path.join(vmware_path, "firewall")
    firewal_content = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\Firewall.txt"
    with open(firewal_content, 'r', encoding='utf-8') as f:
        firewall_xml_content = f.read()  # Đọc nội dung file vào biến chuỗi
    create_config_file(firewall_path, "service.xml", firewall_xml_content)

    vltd_firewall_xml_content = """<ConfigRoot>
<service id='0000'>
   <id>vltd</id>
   <rule id='0000'>
      <direction>outbound</direction>
      <protocol>tcp</protocol>
      <porttype>dst</porttype>
      <port>1492</port>
   </rule>
   <enabled>false</enabled>
   <required>false</required>
</service>
</ConfigRoot>
"""
    create_config_file(firewall_path,"vltd-firewall.xml",vltd_firewall_xml_content)

    vsanhealth_xml_content = """<ConfigRoot>

  <service id='0100'>
    <id>vsanhealth-unicasttest</id>
    <rule id='0000'>
      <direction>outbound</direction>
      <protocol>udp</protocol>
      <port type='dst'>5201</port>
    </rule>
    <rule id='0001'>
      <direction>inbound</direction>
      <protocol>udp</protocol>
      <port type='dst'>5201</port>
    </rule>
    <rule id='0002'>
      <direction>outbound</direction>
      <protocol>tcp</protocol>
      <port type='dst'>5201</port>
    </rule>
    <rule id='0003'>
      <direction>inbound</direction>
      <protocol>tcp</protocol>
      <port type='dst'>5201</port>
    </rule>
   <enabled>false</enabled>
   <required>false</required>
  </service>

</ConfigRoot>
"""
    create_config_file(firewall_path,"vsanhealth.xml",vsanhealth_xml_content)

    # Tạo file vmware/snmp.xml
    snmp_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <snmp>
            <enabled>{random.choice([True, False])}</enabled>
            <community>{generate_random_string(10)}</community>
            <port>{random.randint(161, 65535)}</port>
        </snmp>
    </config>
    """
    create_config_file(vmware_path, "snmp.xml", snmp_xml_content)

    # Tạo file vmware/locker.conf
    locker_conf_content = f"""
    # vSphere Locker Configuration
    locker.port = {random.randint(1024, 65535)}
    locker.enabled = {random.choice([True, False])}
    """
    create_config_file(vmware_path, "locker.conf", locker_conf_content)

    # Tạo file vmware/license.cfg
    license_cfg_content = f"""
    # ESXi License File
    <ConfigRoot>
        <epoc>"{generate_random_string(45)}"/5z+Dn9/"{generate_random_string(16)}"</epoc>
        <float>"{generate_random_string(90)}"=</float>
        <mode>eval</mode>
        <owner/>
    </ConfigRoot>
    """
    create_config_file(vmware_path, "license.cfg", license_cfg_content)

    # Tạo file vmware/vmware.lic
    create_vmware_lic(vmware_path)

#Folder hostd
    # Tạo file hostd/config.xml
    hostd_path = os.path.join(vmware_path, "hostd")
    hostd_config_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <network>
            <port>{random.randint(1024, 65535)}</port>
        </network>
        <storage>
            <path>{generate_random_string(10)}</path>
        </storage>
    </config>
    """
    create_config_file(hostd_path, "config.xml", hostd_config_xml_content)

    # Tạo file hostd/proxy.xml
    hostd_proxy_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <proxy>
            <enabled>{random.choice([True, False])}</enabled>
            <port>{random.randint(1024, 65535)}</port>
        </proxy>
    </config>
    """
    create_config_file(hostd_path, "proxy.xml", hostd_proxy_xml_content)

    # Tạo file hostd/vmInventory.xml
    hostd_vminventory_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <inventory>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
        </inventory>
    </config>
    """
    create_config_file(hostd_path, "vmInventory.xml", hostd_vminventory_xml_content)

    # Tạo file hostd/vmAutoStart.xml
    hostd_vmautostart_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <autostart>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
            <vm name="{generate_random_string(10)}" uuid="{str(uuid.uuid4()).replace('-', '')}"/>
        </autostart>
    </config>
    """
    create_config_file(hostd_path, "vmAutoStart.xml", hostd_vmautostart_xml_content)

    hostd_file = {
    "cgi-config.xml",
    "config-defs.xml",
    "etc-config-defs.xml",
    "hostd-config-defs.xml",
    "hostProfileEngine.xml",
    "hostsvc.xml",
    "IpmiSelDate.bin",
    "settings-defs.xml",
    "pools.xml",
    "vmciAccessManager.xml",
    }
    for hostdn in hostd_file:
        create_config_file(hostd_path,hostdn,generate_random_string(10))

#Folder SSL 
    # Tạo file ssl/rui.crt
    ssl_path = os.path.join(vmware_path, "ssl")
    ssl_rui_crt_content = generate_random_string(1024)
    create_config_file(ssl_path, "rui.crt", ssl_rui_crt_content)

    # Tạo file ssl/rui.key
    ssl_rui_key_content = generate_random_string(1024)
    create_config_file(ssl_path, "rui.key", ssl_rui_key_content)

    # Tạo file ssl/vsan_kms_client.crt
    vsan_kms_client_crt_content = generate_random_string(1024)
    create_config_file(ssl_path, "vsan_kms_client.crt", vsan_kms_client_crt_content)

    # Tạo file ssl/vsan_kms_client.key
    vsan_kms_client_key_content = generate_random_string(1024)
    create_config_file(ssl_path, "vsan_kms_client.key", vsan_kms_client_key_content)

    ssl_file = {
        ".#castore.pem",
        ".#rui.crt",
        ".#rui.key",
        "castore.pem",
        "iofiltervp.pem",
        "iofiltervp_castore.pem",
        "openssl.cnf",
        "vsan_kms_castore.pem",
        "vsan_kms_castore_old.pem",
        "vsan_kms_client_old.crt",
        "vsan_kms_client_old.key",
        "vsanvp_castore.pem",
    }
    for ssln in ssl_file:
        create_config_file(ssl_path,ssln,generate_random_string(1024))

#Folder Vsan
    # Tạo file vsanfs_endpointmgmt.conf
    vsan_path = os.path.join(vmware_path, "vsan")

    vsanfs_conf_content = f"""
    # vSAN Management Configuration
    vsanmgmtd.port = {random.randint(1024, 65535)}
    vsanmgmtd.enabled = {random.choice([True, False])}
    """
    create_config_file(vsan_path, "vsanfs_endpointmgmt.conf", vsanfs_conf_content)

    vsantraced_conf_content = f"""#
# vsantraced.conf --
#
#      Configuration for the VSAN trace daemon.
#
#      Some parameters like MAX_FILES, FILE_SIZE, and LOGFILE
#      can be set separately for the normal and low bandwidth
#      streams.  The remaining parameters apply to both streams.

# Trace log location. If empty, a suitable default is chosen, in order of
# descending preference:
#
#  - /scratch/vsantraces (if backed by persistent storage)
#  - A vsantraces subdirectory on the first discovered VMFS volume
#  - A ramdisk (parameterized below)
#
#VSANTRACED_VOLUME={random.choice(['/scratch/vsantraces', '/tmp/vsantraces'])}

# A symlink to the (auto-)configured trace log location.
#VSANTRACED_VOLUME_SYMLINK="/var/log/vsantraces"

# Set to 1 to prefer a ramdisk over persistent storage (only applicable if
# VSANTRACED_VOLUME is empty).
#VSANTRACED_PREFER_RAMDISK=0

# Ramdisk name and mountpoint
#VSANTRACED_RAMDISK_NAME="vsantraces"
#VSANTRACED_RAMDISK_MOUNT="/vsantraces"

#VSANTRACED_RAMDISK_SIZE={random.randint(100, 500)}

# Location to persist ramdisk tracefiles on shutdown and restore from on boot.
# Set to a non-persistent volume (/tmp) to suppress persisting of tracefiles.
# Note: tracefiles won't be copied to or restored from a non-persitent volume.
# VSANTRACED_PERSISTENT_VOLUME=/scratch
# VSANTRACED_PERSISTENT_VOLUME=/tmp

# Trace log base file name
#VSANTRACED_LOGFILE=vsantraces.log

# Trace log base file name for the low-bandwidth stream
#VSANTRACED_URGENT_LOGFILE = vsantracesUrgent.log

# Trace log base file name for LSOM Debuggability
#VSANTRACED_LSOM_LOGFILE = vsantracesLSOM.log

# Trace log base file name for LSOM Verbose Traces.
#VSANTRACED_LSOM_VERBOSE_LOGFILE = vsantracesLSOMVerbose.log

# Trace log base file name for DOM object Debuggability
#VSANTRACED_DOM_OBJ_LOGFILE = vsantracesDOMObj.log

# Trace log base file name for object IO diagnostics
# VSANTRACED_IO_DIAG_LOGFILE = vsantracesIODiag.log

# Set to 1 to gzip trace logs.
#VSANTRACED_USE_GZIP=1

# Compression level. Note: higher levels result in
# high CPU usage without much size benefit
#VSANTRACED_GZIP_LEVEL=3

# Trace log rotation parameterization
# Size is compressed size in MB
#VSANTRACED_ROTATE_MAX_FILES={random.randint(4, 16)}
#VSANTRACED_ROTATE_FILE_SIZE={random.randint(10, 50)}

# Trace log rotation parameterization
# Size is compressed size in MB
#VSANTRACED_LSOM_ROTATE_MAX_FILES={random.randint(8, 16)}
#VSANTRACED_LSOM_ROTATE_FILE_SIZE={random.randint(22, 50)}

# Trace log rotation parameterization
# Size is compressed size in MB
#VSANTRACED_LSOM_VERBOSE_ROTATE_MAX_FILES={random.randint(8, 16)}
#VSANTRACED_LSOM_VERBOSE_ROTATE_FILE_SIZE={random.randint(22, 50)}

# Trace log rotation parameterization
# Size is compressed size in MB
#VSANTRACED_DOM_OBJ_ROTATE_MAX_FILES={random.randint(2, 6)}
#VSANTRACED_DOM_OBJ_ROTATE_FILE_SIZE={random.randint(10, 20)}

# Trace log rotation parameterization
# File size is compressed size in MB
#VSANTRACED_OBJLIB_ROTATE_MAX_FILES={random.randint(2, 6)}
#VSANTRACED_OBJLIB_ROTATE_FILE_SIZE={random.randint(10, 20)}
# UDP receive buffer size in Bytes (default 32KB)
#VSANTRACED_OBJLIB_UDP_BUFFER_SIZE=32768

# Trace log rotation parameterization for the low bandwidth stream.
# Size is compressed size in MB
#VSANTRACED_URGENT_ROTATE_MAX_FILES={random.randint(2, 8)}
#VSANTRACED_URGENT_ROTATE_FILE_SIZE={random.randint(10, 35)}

# Trace log rotation parameterization
# File size is compressed size in MB
#VSANTRACED_IO_DIAG_ROTATE_MAX_FILES={random.randint(3 , 10)}
#VSANTRACED_IO_DIAG_ROTATE_FILE_SIZE={random.randint(5, 15)}

# Extra parameters, passed to logchannellogger
#VSANTRACED_EXTRA_PARAM=

# Previously selected VSAN trace partition
#VSANTRACED_LAST_SELECTED_VOLUME

# Log urgent traces to syslog folder
#VSANTRACED_LOG_URGENT_TO_SYSLOG=1

# Amount of observer data to keep around in MB (compressed size)
#VSANOBSERVER_MAX_MB_SIZE={random.randint(50, 200)}

    """
    create_config_file(vsan_path, "vsanfs_endpointmgmt.conf", vsantraced_conf_content)

    # Tạo file vsan/vsansvc.xml
    vsan_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <vsan>
            <cluster name="{generate_random_string(10)}" id="{random.randint(1, 100)}"/>
            <storage capacity="{random.randint(100, 1000)}"/>
        </vsan>
    </config>
    """
    create_config_file(vsan_path, "vsansvc.xml", vsan_xml_content)

    # Tạo file vsan/fa_ext_to_type.json
    vsan_json_content = f"""{{
        "cluster": {{
            "name": "{generate_random_string(10)}",
            "id": {random.randint(1, 100)}
        }},
        "storage": {{
            "capacity": {random.randint(100, 1000)}
        }}
    }}
    """
    create_config_file(vsan_path, "fa_ext_to_type.json", vsan_json_content)

    # Tạo file vsan/vsanperf.conf
    vsanperf_conf_content = f"""
    # vSwitch Configuration
    vswitch.name = "{generate_random_string(10)}"
    vswitch.portgroup = "{generate_random_string(10)}"
    vswitch.network = "{generate_random_string(10)}"
    """
    create_config_file(vsan_path, "vsanperf.conf", vsanperf_conf_content)

#Folder SSH
    # Tạo file /etc/ssh/sshd_config và các key
    ssh_path = os.path.join(etc_path,"ssh")
    key_path = os.path.join(ssh_path,"keys-root")
    create_ssh_keys(ssh_path)  # Tạo key trước khi tạo sshd_config
    fake_ssh_port = 2222 
    allowed_ips = ["10.0.0.1", "192.168.1.100"]  
    create_sshd_config(ssh_path, fake_ssh_port, allowed_ips)
    create_sshd_config(ssh_path)
    create_config_file(ssh_path,"moduli",generate_random_string(12))
    create_config_file(key_path,"authorized_keys",generate_random_string(10))
    create_config_file(ssh_path,".#ssh_host_ecdsa_key",generate_random_string(12))
    create_config_file(ssh_path,".#ssh_host_ecdsa_key.pub",generate_random_string(12))
    create_config_file(ssh_path,".#ssh_host_rsa_key",generate_random_string(12))
    create_config_file(ssh_path,".#ssh_host_rsa_key.pub",generate_random_string(12))

#các file trong thư mục etc
    Datashadow = "S:\Summer2024\IAP491_G2\Code\Luaga\Engine\Code\ESXi\shadow"
    with open(Datashadow, 'r', encoding='utf-8') as f:
        content_shadow = f.read()  # Đọc nội dung file vào biến chuỗi 
    create_config_file(etc_path,"shadow",content_shadow)
    create_config_file(etc_path,"rc.local",generate_random_string(50))

    # Tạo file /etc/hosts
    create_hosts_file(etc_path)

    # Tạo file passwd
    create_passwd_file(etc_path)

    etc_file = {
        ".#chkconfig.db": 54,
        ".#dhclient-vmk0.leases": 62,
        ".#krb5.conf": 693,
        ".#random-seed": 54,
        "banner": 54,
        "chkconfig.db": 54,
        "dhclient-vmk0.conf": 54,
        "dhclient-vmk0.leases": 5045,
        "dhclient6-vmk0.conf": 54,
        "dhclient6-vmk0.leases": 54,
        "environment": 54,
        "eToken.conf": 54,
        "group": 54,
        "host.conf": 54,
        "profile": 54,
        "inittab": 54,
        "issue": 54,
        "krb5.conf": 54,
        "krb5.keytab": 54,
        "localtime": 54,
        "motd": 54,
        "nscd.conf": 54,
        "nsswitch.conf": 54,
        "ntp.conf": 54,
        "ntp.drift": 54,
        "ntp.keys": 54,
        "passwdqc.conf": 54,
        "profile.local": 54,
        "protocols": 5459,
        "ptp.conf": 54,
        "random-seed": 54,
        "resolv.conf": 54,
        "services": 20584,
        "SHAC_Config.ini": 54,
        "shells": 54,
        "slp.reg": 54,
        "vmotion-resolv.conf": 54,
        "vmsyslog.conf": 54,
        "vSphereProvisioning-resolv.conf": 54,
    }
    for etcname,etcsize in etc_file.items():
        create_config_file(etc_path,etcname,generate_random_string(etcsize))

#Folder vmkiscsid
    # Tạo file vmkiscsid/vmkiscsid.db
    vmkiscsid_path = os.path.join(vmware_path, "vmkiscsid")
    iscsid_conf_content = f"""
    # iSCSI Configuration File
    node.name = "{generate_random_string(10)}"
    discovery.sendtargets.all = yes
    discovery.sendtargets.port = 3260
    """
    create_config_file(vmkiscsid_path, "vmkiscsid.db", iscsid_conf_content)

    # Tạo file vmkiscsid/.#vmkiscsid.db
    create_config_file(vmkiscsid_path, ".#vmkiscsid.db", generate_random_string(10))

#Folder rhttpproxy
    # Tạo file rhttpproxy/config.xml
    network_path = os.path.join(vmware_path, "rhttpproxy")
    vnet_conf_content = f"""
    # Virtual Network Configuration
    vnet.name = "{generate_random_string(10)}"
    vnet.vswitch = "{generate_random_string(10)}"
    vnet.network = "{generate_random_string(10)}"
    """
    create_config_file(network_path, "vnet.conf", vnet_conf_content)

    # Tạo file rhttpproxy/default-config.xml
    vmxnet3_conf_content = f"""
    # vmxnet3 Network Configuration
    vmxnet3.name = "{generate_random_string(10)}"
    vmxnet3.vswitch = "{generate_random_string(10)}"
    vmxnet3.network = "{generate_random_string(10)}"
    """
    create_config_file(network_path, "default-config.xml", vmxnet3_conf_content)

    # Tạo file rhttpproxy/endpoints.conf
    vnic_conf_content = f"""
    # Virtual NIC Configuration
    vnic.name = "{generate_random_string(10)}"
    vnic.vswitch = "{generate_random_string(10)}"
    vnic.network = "{generate_random_string(10)}"
    """
    create_config_file(network_path, "endpoints.conf", vnic_conf_content)

#Folder sysyem
    # Tạo file system/custom_config.xml
    system_path = os.path.join(vmware_path, "system")
    custom_config_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <customConfig>
            <setting name="{generate_random_string(10)}" value="{generate_random_string(10)}"/>
        </customConfig>
    </config>
    """
    create_config_file(system_path, "custom_config.xml", custom_config_xml_content)

#Folder config
    config = '/ESXI 7/etc/config/EMU/mili/'
    create_config_file(config,"intr_logopts.txt",generate_random_string(5284))
    create_config_file(config,"savestp.txt",generate_random_string(5284))
    create_config_file(config,"savetgt.txt",generate_random_string(5284))

#Folder init.d
    init = '/ESXI 7/etc/init.d/'
    init_file = {
        "apiForwarder": 654,
        "attestd": 758,
        "cdp": 52,
        "clomd": 2,
        "cmmdsd": 452,
        "cmmdsTimeMachine": 24,
        "dcbd": 24,
        "DCUI": 52,
        "dpd": 452,
        "epd": 52,
        "esxgdpd": 5,
        "ESXShell": 52,
        "esxTokenCPS": 52,
        "esxui": 52,
        "fsvmsockrelay": 3,
        "gstored": 38,
        "health": 57,
        "hostd": 82,
        "hostdCgiServer": 8,
        "iofilterd-spm": 8,
        "iofilterd-vmwarevmcrypt": 2,
        "iofiltervpd": 28,
        "kmxa": 75,
        "kmxd": 52,
        "lacp": 58,
        "lbtd": 53,
        "loadESX": 1,
        "lsud": 158,
        "lwsmd": 15,
        "nicmgmtd": 4,
        "pmemGarbageCollection": 14,
        "sfcbd-watchdog": 1,
        "vsandevicemonitord": 633,
        "vsanmgmtd": 85,
        "vsanObserver": 7,
        "vsantraced": 599,
        "vvold": 18,
        "wsman": 15,
        "xorg": 85,
    }
    for initname, initsize in init_file.items():
        create_config_file(init,initname,generate_random_string(initsize))

#Folder vmsyslog
    vmsyslog = '/ESXI 7/etc/vmsyslog.conf.d/'
    for initname, initsize in init_file.items():
        create_config_file(vmsyslog,initname,generate_random_string(initsize))

#Folder likewise
    like = '/ESXI 7/etc/likewise/'
    create_directory(like)

#Folder openwsman
    openw = '/ESXI 7/etc/openwsman/'
    create_config_file(openw,"identify.xml",generate_random_string(54))
    create_config_file(openw,"openwsman.conf.tmpl",generate_random_string(54))
    create_config_file(openw,"owsmangencert.sh",generate_random_string(54))
    create_config_file(openw,"subscriptions",generate_random_string(54))

#Folder opt
    opt = '/ESXI 7/etc/opt/'
    create_directory(opt)

#Folder pam.d
    pam_tem = '/ESXI 7/etc/pam.d/template/'
    create_directory(pam_tem)

    pam = '/ESXI 7/etc/pam.d/'
    pam_file = {
        "daemondk": 12,
        "dcui": 12,
        "hostd-cgi": 12,
        "login": 12,
        "openwsman": 12,
        "other": 12,
        "settingsd": 12,
        "passwd": 12,
        "settingsd": 12,
        "system-auth-generic": 12,
        "vmtoolsd": 12,
        "vmware-authd": 12,
    }
    for pamname,pamsize in pam_file.items():
        create_config_file(pam,pamname,generate_random_string(pamsize))

#Folder rc.local.d
    rc = '/ESXI 7/etc/rc.local.d/'
    rc_file = {
        "009.vsanwitness.sh": 15,
        "cleanupStatefulHost.py": 15,
        "kickstart.py": 15,
        "local.sh": 15,
        "psaScrub.py": 15,
    }
    for rcname,rcsize in rc_file.items():
        create_config_file(rc,rcname,generate_random_string(rcsize))
    
#Folder security
    se = '/ESXI 7/etc/security/'
    se_file = {
        ".#access.conf": 13,
        "access.conf": 13,
        "dcui-access.conf": 13,
        "opasswd": 13,
        "pam_env.conf": 13,
        "ssh_limits.conf": 13,
    }
    for sename,sesze in se_file.items():
        create_config_file(se,sename,generate_random_string(sesze))

#Folder sfcb
    sfcb = '/ESXI 7/etc/sfcb/'
    create_config_file(sfcb,"repository",generate_random_string(12))
    create_config_file(sfcb,"sfcb.cfg",generate_random_string(12))
    create_config_file(os.path.join(sfcb,"omc"),"sensor_health",generate_random_string(12))

#Folder shutdown.d
    shut = '/ESXI 7/etc/shutdown.d/'
    create_config_file(shut,"iofilterd-spm",generate_random_string(13))
    create_config_file(shut,"iofilterd-vmwarevmcrypt",generate_random_string(13))

#Folder vmware_tool
    vmt = '/ESXI 7/etc/vmware-tools/'
    vmt_file = {
        "poweroff-vm-default": 354,
        "poweron-vm-default": 354,
        "resume-vm-default": 354,
        "statechange.subr": 10,
        "suspend-vm-default": 354,
        "tools.conf": 10,
    }
    for vmtn,vmts in vmt_file.items():
        create_config_file(vmt,vmtn,generate_random_string(vmts))

    com = '/ESXI 7/etc/vmware-tools/plugins/common/'
    create_directory(com)

    vmsvc = '/ESXI 7/etc/vmware-tools/plugins/vmsvc/'
    create_directory(vmsvc)

    script = '/ESXI 7/etc/vmware-tools/script-data/'
    create_directory(script)

    vmware = '/ESXI 7/etc/vmware-tools/scripts/vmware/'
    create_config_file(vmware,"network",generate_random_string(25))

#Folder X11
    X11 = '/ESXI 7/etc/X11/'
    create_config_file(X11,"server.xkm",generate_random_string(1035))
    create_config_file(X11,"xorg.conf",generate_random_string(10))
