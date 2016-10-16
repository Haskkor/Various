@echo off

:choiceGlob

cls
echo 1 - Liste interfaces
echo 2 - Renommer interface
echo 3 - Adressage IP
echo 4 - DNS
echo 5 - Ipconfig
echo 6 - Sortir
echo.

set /p choix=Choix : 
If %choix% EQU 1 goto listInt
If %choix% EQU 2 goto renamInt
If %choix% EQU 3 goto choiceAdd
If %choix% EQU 4 goto choiceDNS
If %choix% EQU 5 goto ipConfig
If %choix% EQU 6 goto fin

:listInt

cls
netsh interface ip show config
PAUSE
goto choiceGlob

:renamInt

cls
set /p nameOldInt=Ancien nom de l'interface : 
set /p nameNewInt=Nouveau nom de linterface : 
netsh interface set interface name="%nameOldInt%" newname="%nameNewInt%"
goto choiceGlob

:choiceAdd

cls
echo 1 - DHCP
echo 2 - IP Statique
echo 3 - Sortir
echo.

set /p choixAdd=Choix : 
If %choixAdd% EQU 1 goto addDhcp
If %choixAdd% EQU 2 goto addStatic
If %choixAdd% EQU 3 goto choiceGlob

:choiceDNS

cls
echo 1 - Dynamique
echo 2 - Statique
echo 3 - Sortir
echo.

set /p choixDns=Choix : 
If %choixDns% EQU 1 goto dnsDyn
If %choixDns% EQU 2 goto dnsStat
If %choixDns% EQU 3 goto choiceGlob

:ipConfig
ipconfig /all
PAUSE
goto choiceGlob

:addDhcp

set /p nameAddDyn=Nom de l'interface : 
netsh interface ip set address name="%nameAddDyn%" dhcp
goto choiceAdd

:addStatic

set /p nameAddStat=Nom de l'interface : 
set /p ipAddStat=Adresse IP : 
set /p subAddStat=Masque de sous-r‚seau : 
set /p gwAddStat=Passerelle : 
set /p gwMetrAddStat=M‚trique : 
netsh interface ip set address name="%nameAddStat%" source=static addr="%ipAddStat%" mask="%subAddStat%" gateway="%gwAddStat%" gwmetric="%gwMetrAddStat%"
goto choiceAdd

:dnsDyn

set /p nameDnsDyn=Nom de l'interface : 
netsh interface ip set dns name="%nameDnsDyn%" dhcp
goto choiceDns

:dnsStat

set /p nameDnsStat=Nom de l'interface : 
set /p ipDnsStatPri=DNS Primaire : 
set /p ipDnsStatSec=DNS Secondaire : 
netsh interface ip set dns name="%nameDnsStat%" static "%ipDnsStatPri%"
netsh interface ip add dns name="%nameDnsStat%" addr="%ipDnsStatSec%"
goto choiceDns

:fin