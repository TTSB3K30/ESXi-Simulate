import time
import subprocess


from ESXi_config import generate_random_string
from ESXi_config import create_config_file
from ESXi_config import create_directory
from bin import create_esx_bin
from dev import create_esx_dev
from etc import create_esx_etc
from include_esxi import create_esx_include
from lib_esxi import create_esx_lib
from lib64_esxi import create_esx_lib64
from opt import create_esx_opt
from tardisks import create_esx_tardisks
from tmp import create_esx_tmp
from usr import create_esx_usr
from var import create_esx_var
from vmfs import create_esx_vmfs

def create_esx_proc(proc="/ESXI 7/proc/"):
    create_directory(proc)

def create_esx_tardisks_noauto(noauto="/ESXI 7/tardisks_noauto/"):
    create_directory(noauto)
         
def create_esx_vmimages(vmimages ="/ESXI 7/vmimages"):
    create_config_file(vmimages,"floppies",generate_random_string(15))
    create_config_file(vmimages,"tools-isoimages",generate_random_string(15))

def create_esx_config_files(base_path="/ESXI 7"):
    """Tạo các file cấu hình ESXi 7."""
    boot_cfg_content_1 = """
    atlantic.v00  elx_esx_.v00  iavmd.v00     loadesx.v00   lsuv2_nv.v00  nhpsa.v00     nvmxnet3.v00  qfle3i.v00    tpmesxup.v00  vmkusb.v00
b.b00         elxiscsi.v00  icen.v00      lpfc.v00      lsuv2_oe.v00  nmlx4_co.v00  nvmxnet3.v01  qflge.v00     trx.v00       vmw_ahci.v00
basemisc.tgz  elxnet.v00    igbn.v00      lpnic.v00     lsuv2_oe.v01  nmlx4_en.v00  onetime.tgz   qlnative.v00  uc_amd.b00    vmware_e.v00
bmcal.v00     esx_dvfi.v00  imgdb.tgz     lsi_mr3.v00   lsuv2_oe.v02  nmlx4_rd.v00  procfs.b00    rste.v00      uc_hygon.b00  vmx.v00
bnxtnet.v00   esx_ui.v00    ionic_en.v00  lsi_msgp.v00  lsuv2_sm.v00  nmlx5_co.v00  pvscsi.v00    s.v00         uc_intel.b00  vsan.v00
bnxtroce.v00  esxio_co.v00  irdman.v00    lsi_msgp.v01  mtip32xx.v00  nmlx5_rd.v00  qcnic.v00     sb.v00        useropts.gz   vsanheal.v00
boot.cfg      esxupdt.v00   iser.v00      lsi_msgp.v02  native_m.v00  ntg3.v00      qedentv.v00   sfvmk.v00     vdfs.v00      vsanmgmt.v00
brcmfcoe.v00  features.gz   ixgben.v00    lsuv2_hp.v00  ne1000.v00    nvme_pci.v00  qedrntv.v00   smartpqi.v00  vim.v00       weaselin.v00
btldr.v00     gc.v00        jumpstrt.gz   lsuv2_in.v00  nenic.v00     nvmerdma.v00  qfle3.v00     state.tgz     vmkata.v00    xorg.v00
crx.v00       i40en.v00     k.b00         lsuv2_ls.v00  nfnic.v00     nvmetcp.v00   qfle3f.v00    tpm.v00       vmkfcoe.v00
    """
    create_config_file(base_path,"bootbank",boot_cfg_content_1)

    boot_file = {
        ".#encryption.info": 584,
        ".mtoolsrc": 452,
        "altbootbank": 455,
        "bootpart.gz": 45,
        "bootpart4kn.gz": 2147,
        "local.tgz": 2452,
        "local.tgz.ve": 245,
        "locker": 264,
        "productLocker": 314,
        "sbin": 941,
        "scratch": 45,
        "store": 43,
    }
    for bname, bsize in boot_file.items():
        create_config_file(base_path,bname,generate_random_string(bsize))

def start_Luaga():
    """Bắt đầu honeypot Luaga."""
    try:
        subprocess.Popen(["Luaga"])
        print("Luaga honeypot đang chạy...")
    except FileNotFoundError:
        print("Luaga không được cài đặt. Vui lòng cài đặt Luaga trước khi chạy.")

def monitor_Luaga_log():
    """Giám sát log của Luaga để phát hiện kết nối SSH."""
    log_file = "S:/ESXI 7/var/log/auth.log" #file log chứa dữ liệu để nhận bt ssh
    last_line = None
    while True:
        time.sleep(1)  # Kiểm tra log mỗi giây
        with open(log_file, "r") as f:
            for line in f:
                if line != last_line:
                    last_line = line
                    if "SSH" in line or "Client" in line:
                        # Phát hiện kết nối SSH từ Client
                        attacker_ip = line.split(" ")[4].strip()
                        print(f"Phát hiện kết nối SSH từ: {attacker_ip}")
                        # Xử lý khi attacker SSH từ ESXi 1 sang ESXi khác
                        if attacker_ip == "192.168.1.1":  # Địa chỉ ESXi 1
                            create_esx_config_files()
                            create_esx_bin()
                            create_esx_dev()
                            create_esx_etc(config_type="ESXI 2")
                            create_esx_include()
                            create_esx_lib()
                            create_esx_lib64()
                            create_esx_opt()
                            create_esx_proc()
                            create_esx_tardisks()
                            create_esx_tardisks_noauto()
                            create_esx_tmp()
                            create_esx_usr()
                            create_esx_var()
                            create_esx_vmfs()
                            create_esx_vmimages()
                            print("Tạo lại file cấu hình ESXi 7 với cấu hình khác.")
                        elif attacker_ip == "192.168.1.2":  # Địa chỉ ESXi 2
                            # create_esx_config_files(config_type="advanced")  # Tạo lại file cấu hình với cấu hình khác
                            create_esx_config_files()
                            create_esx_bin()
                            create_esx_dev()
                            create_esx_etc(config_type="ESXI 3")
                            create_esx_include()
                            create_esx_lib()
                            create_esx_lib64()
                            create_esx_opt()
                            create_esx_proc()
                            create_esx_tardisks()
                            create_esx_tardisks_noauto()
                            create_esx_tmp()
                            create_esx_usr()
                            create_esx_var()
                            create_esx_vmfs()
                            create_esx_vmimages()
                            print("Tạo lại file cấu hình ESXi 7 với cấu hình khác.")
                        elif attacker_ip == "192.168.1.162":  # Địa chỉ ESXi 3
                            create_esx_config_files()
                            create_esx_bin()
                            create_esx_dev()
                            create_esx_etc(config_type="ESXI 4")
                            create_esx_include()
                            create_esx_lib()
                            create_esx_lib64()
                            create_esx_opt()
                            create_esx_proc()
                            create_esx_tardisks()
                            create_esx_tardisks_noauto()
                            create_esx_tmp()
                            create_esx_usr()
                            create_esx_var()
                            create_esx_vmfs()
                            create_esx_vmimages()
                            print("Tạo lại file cấu hình ESXi 7 với cấu hình khác.")
                        elif attacker_ip == "192.168.1.16":  # Địa chỉ ESXi 4
                            create_esx_config_files()
                            create_esx_bin()
                            create_esx_dev()
                            create_esx_etc(config_type="ESXI 5")
                            create_esx_include()
                            create_esx_lib()
                            create_esx_lib64()
                            create_esx_opt()
                            create_esx_proc()
                            create_esx_tardisks()
                            create_esx_tardisks_noauto()
                            create_esx_tmp()
                            create_esx_usr()
                            create_esx_var()
                            create_esx_vmfs()
                            create_esx_vmimages()
                            print("Tạo lại file cấu hình ESXi 7 với cấu hình khác.")