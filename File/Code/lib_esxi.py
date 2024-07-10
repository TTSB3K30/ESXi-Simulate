from ESXi_config import create_config_file
from ESXi_config import create_directory
from ESXi_config import generate_random_string

def create_esx_lib(lib_path="/ESXI 7/lib/"):
    security_path='/ESXI 7/lib/security'
    create_directory(security_path)

    lib_file = {
        "ld-2.17.so": 165614,
        "ld-linux.so.2": 16,
        "libc-2.17.so": 45513,
        "libc.so.6": 16,
        "libcrypt.so.1": 16,
        "libcrypt.so.1.0": 5615,
        "libcrypto.so": 11,
        "libcrypto.so.1.0.2": 56411,
        "libdl-2.17.so": 5415,
        "libdl.so.2": 1145,
        "libexpat.so": 16,
        "libgcc_s.so": 16,
        "libgcc_s.so.1": 16,
        "libm-2.17.so": 16,
        "libm.so.6": 16,
        "libnsl-2.17.so": 16,
        "libnsl.so.1": 16,
        "libnss_compat-2.17.so": 16,
        "libnss_compat.so.2": 16,
        "libnss_dns-2.17.so": 16,
        "libnss_dns.so.2": 16,
        "libnss_files-2.17.so": 16,
        "libnss_files.so.2": 16,
        "libnss_nis-2.17.so": 16,
        "libnss_nis.so.2": 16,
        "libnss_nisplus-2.17.so": 16,
        "libnss_nisplus.so.2": 16,
        "libpthread-2.17.so": 16,
        "libpthread.so.0": 16,
        "libresolv-2.17.so": 16,
        "libresolv.so.2": 16,
        "librt-2.17.so": 16,
        "librt.so.1": 16,
        "libssl.so": 16,
        "libssl.so.1.0.2": 16,
        "libstdc++.so": 16,
        "libstdc++.so.6": 16,
        "libstdc++.so.6.0.22": 16,
        "libthread_db-1.0.so": 16,
        "libthread_db.so.1": 16,
        "libutil-2.17.so": 16,
        "libutil.so.1": 16,
        "libvmkmgmt.so": 16,
        "libvmksysinfoNoVob.so": 16,
        "libvmkuser.so": 16,
        "libvmkuser.so.0": 16,
        "libvmkuser.so.0.21": 16,
        "libvmlibs.so": 16,
        "libxml2.so": 16,
        "libxml2.so.2": 16,
        "libxml2.so.2.9.14": 16,
        "libz.so": 16,
        "libz.so.1": 16,
        "libz.so.1.2.12": 16,
    }
    for libn,libs in lib_file.items():
        create_config_file(lib_path,libn,generate_random_string(libs))