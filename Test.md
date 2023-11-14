## Puppets:
Facebook:
TikTok:

## Frameworks
https://osintframework.com/

## All in one scanners:
### Email
- hunter.io
- https://phonebook.cz
- https://www.voilanorbert.com/
- https://tools.emailhippo.com/
- https://email-checker.net/validate
- https://chrome.google.com/webstore/detail/clearbit-connect-supercha/pmnhcgfcafcnkbengdcanjablaabjplo?hl=en
- clearbit
- https://Dehashed.com (paid only option)
- Crt.sh (searches for certificates
```
sublist3r -d DOMAIN > domains.txt
```

## Social Media
Search for pictures (badges, etc)

## Domains
Grab ASN - https://bgp.he.net/
```
curl -s https://crt.sh/\?q\=google.com\&output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u
```

#### Photon
```
sudo git clone https://github.com/s0md3v/Photon.git

cd Photon

sudo python photon.py -u taupe-solutions.com -l 3 -t 100 --wayback
```
- Builtwith.com
- karma
```
python3 subbrute.py <domain.com>
```

```
dnsenum -p 20 -s 100 --threads 5 DOMAIN
```


```
recon.sh in 1-recon folder "recon.sh <DOMAIN>"
```
```
whois megacorpone.com
```

#### Discover
```
cd /opt/discover/
sudo ./discover.sh
```
#### Knockpy
```
cd /opt/
sudo git clone https://github.com/guelfoweb/knock.git
cd knock/knockpy
```

```
python3 knockpy.py <website>
```

- viewdns.info
- https://searchdns.netcraft.com/

#### recon-ng
1. marketplace install hackertarget
2. modules load hackertarget
3. options set SOURCE DOMAIN
4. run

Assetfinder website or domain- assetfinder tesla.com

gowitness file

```
nslookup hostname hostname
```

#### DNS recon - GitHub - aboul3la/Sublist3r

```
theHarvester -d tesla.com -b google -l 500
```


```
subfinder -d DOMAIN
```

### Sockpockets (create a fake alias)

- Fakenamegenerator.com
- privacy.com for burner CC

### Search Engine Operators
- https://www.google.com/advanced_search
- chris brown site:airforce.com
- chris brown AND "TACP" site:airforce.com
- chris brown OR "TACP" site:airforce.com
- site:airforce.com password
- site:airforce.com password filetype:xlsx
- "chris brown" intext:password
- "chris brown" intitle:password
- "thepastamentors.com" site: *

### Image Search

1. images.google.com
2. drag and drop picture in search bar
3. on the images tab, click the camera button in the search bar

- https://Yandex.com
- https://tineye.com/

### Image OSINT

- exiftool
	
### Password

- Get hashes - https://Dehashed.com (paid only option)
- https://weleakinfo.io
- https://scylla.sh/

### Usernames

- https://namechk.com/
- https://whatsmyname.app/
- https://namecheckup.com/
```
sherlock USERNAME
```

```
whatsmyname -u thecybermentor
```

### Recon-ng

1. marketplace install profiler
2. modules load profiler
3. options set SOURCE USERNAME
4. run
5. show profiles

### People OSINT

- https://www.whitepages.com
- https://www.truepeoplesearch.com/
- https://www.fastpeoplesearch.com/
- https://www.fastbackgroundcheck.com/
- https://webmii.com/com
- https://peekyou.com
- https://www.411.com
- https://www.spokeo.com/
- https://thatsthem.com
- https://www.social-searcher.com

### Voters
- https://www.voterrecords.com/

### Phone Numbers

- https://www.truecaller.com/
- https://calleridtest.com/

	https://infobel.com

	
### Phoneinfoga:

```
phoneinfoga scan -n PHONE_NUMBER
```
```
phoneinfoga serve -p 8080
```

### Social Media

- https://socialbearing.com

### Business

 - https://opencorporates.com
 - https://www.aihitdata.com
 - https://indeed.com

### Wifi

- https://wigle.net

### Documents:

#### Powermeta (use on windows, better results)

1. Get PowerMeta.ps1 on attacking machine
	- from kali: "pwsh"
```
powershell -ep bypass
```
```
Import-Module PowerMeta.ps1
```
```
Invoke-PowerMeta -TargetDomain taupe-solutions.com -Download -Extract
```
