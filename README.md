```
   ###    ########     ###    ##     ## ########  #######  ##     ##    ###    ########  #######  ########  
  ## ##   ##     ##   ## ##   ##     ##    ##    ##     ## ###   ###   ## ##      ##    ##     ## ##     ## 
 ##   ##  ##     ##  ##   ##  ##     ##    ##    ##     ## #### ####  ##   ##     ##    ##     ## ##     ## 
##     ## ##     ## ##     ## ##     ##    ##    ##     ## ## ### ## ##     ##    ##    ##     ## ########  
######### ##     ## ######### ##     ##    ##    ##     ## ##     ## #########    ##    ##     ## ##   ##   
##     ## ##     ## ##     ## ##     ##    ##    ##     ## ##     ## ##     ##    ##    ##     ## ##    ##  
##     ## ########  ##     ##  #######     ##     #######  ##     ## ##     ##    ##     #######  ##     ## 
```
## Description

**This repository contains `ADautomator.py`, an automated script that provides the user with an interactive interface to conduct Kerberoasting, ASREProasting, domain controller enumneration that is focused on Active Directory penetration testing. 

The overall intent of this project is to provide a user with a graphical user interface in which you can use the penetration testing evaluation standard (PTES) to create a methodological approach and penetration testing from a graphical user interface written in Python. 

## This tool will not automatically exploit a vulnerability and should be allowed to use on popular penetration testing certifications such as PNPT and OSCP

**Currently only crackmapexec works in the toolset so use with caution.**
---

### Usage

```bash
python3 ADautomator.py
```


## Features

- Automated SMB and LDAP protocol penetration testing via crackmapexec.
- Ability to customize command execution for targeted assessments.
- Scripted interaction with CrackMapExec for enhanced testing procedures.
- Output pattern matching for quick identification of key security insights.
- Designed with DoD-level security and private sector flexibility in mind.

## Features We are Working On!!

- Cradle to grave Active Directory Penetration testing using the PTES framework
- Ability to upload usernames to create a custom username list, i.e. mike jones =mike.jones, mjones, mikej, jones.mike, jonesm, etc
- Industry standard tools such as impacket for kerberoasting, asreproasting,
- Automatically identify if printnightmare and zerologin are vulnerable


![Supported Python versions](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10-blue.svg)


