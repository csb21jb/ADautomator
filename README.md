```
       d8888 8888888b.                    888                                   888                    
      d88888 888  "Y88b                   888                                   888                    
     d88P888 888    888                   888                                   888                    
    d88P 888 888    888  8888b.  888  888 888888 .d88b.  88888b.d88b.   8888b.  888888 .d88b.  888d888 
   d88P  888 888    888     "88b 888  888 888   d88""88b 888 "888 "88b     "88b 888   d88""88b 888P"   
  d88P   888 888    888 .d888888 888  888 888   888  888 888  888  888 .d888888 888   888  888 888     
 d8888888888 888  .d88P 888  888 Y88b 888 Y88b. Y88..88P 888  888  888 888  888 Y88b. Y88..88P 888     
d88P     888 8888888P"  "Y888888  "Y88888  "Y888 "Y88P"  888  888  888 "Y888888  "Y888 "Y88P"  888
```
## Overview

ADautomator is a comprehensive toolkit designed for cybersecurity professionals focusing on Active Directory environments. It automates various tasks related to Active Directory security, including package installation, domain enumeration, and advanced network analysis. The tool is built in Python and integrates various external tools and scripts, making it a versatile solution for network administrators and security experts. 

## This tool will not automatically exploit a vulnerability and should be allowed to use on popular penetration testing certifications such as PNPT and OSCP. This can easily be done, but I wont include that capability for public use.
---

## Key Features

- Automated Package Installation: Streamlines the setup process by installing essential tools like seclists, crackmapexec, ntpdate, and python3-impacket.
- Facilitates thorough scanning and enumeration of Active Directory domains.
- Includes features for detecting lockout policies, finding NTLM hash segments, and identifying potential vulnerabilities.
- Automated SMB and LDAP protocol penetration testing via crackmapexec.
- Output Management: Capable of redirecting output to files for further analysis.
- User Interaction and Alerts: Provides interactive prompts and color-coded alerts to inform users about critical findings or potential risks.

## How to use ADautomator
### Installation
```bash
python3 ADautomator.py --install
```
### Get Help
```bash
python3 ADautomator.py -h
```
### Basic Commands
- Run an anonymous scan on the AD network
```bash
python3 ADautomator.py --adnuke -ip [IP_ADDRESS]
```
- Execute a full frontal attack on the Active Directory network
```bash
python3 ADautomator.py --adnuke -ip [IP_ADDRESS] -u [USERNAME] -p [PASSWORD] -out [OUTPUT_FILE]
```

## Upcoming Features!!

- Cradle to grave Active Directory Penetration testing using the PTES framework
- The use of kerbrute to gather usernames
- Automated password and username spraying after usernames are identified


## Help 
![image](https://github.com/csb21jb/ADautomator/assets/94072917/93354f62-d48a-42a3-b8cc-e9df3a2e1eb8)

## Detects Domain Lockout Policy with user input to understand the danger
![image](https://github.com/csb21jb/ADautomator/assets/94072917/82054d5d-b697-4aea-9cf1-3783acefdcde)

## Get Hashes to use in a pass the hash attack or login with PSexec
![image](https://github.com/csb21jb/ADautomator/assets/94072917/974e8e83-ad15-47a1-97d5-3e87b931a40f)

## Get users and save them to a file
![image](https://github.com/csb21jb/ADautomator/assets/94072917/bb177e90-d1a4-405c-9af6-9e6fe49fd7c7)

![image](https://github.com/csb21jb/ADautomator/assets/94072917/86872e78-4c51-4428-8c5b-bfec993fa014)



![Supported Python versions](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10-blue.svg)


