@echo off
git status

MD tempF1
CD tempF1
for /F "usebackq tokens=1" %%A IN (`git config user.name`) do (
  set gituser=%%A
)
echo  ^<-- GIT User> "%gituser%"
findstr /A:0a /S "<--" "%gituser%" 
cd..
RD /s /q tempF1
echo.

git add -A

REM tambien en la fecha se puede usar el %date%
:: git commit -m "[%gituser%] [%datestr%] %commit% "
call npm version patch -f
FOR /F "tokens=* USEBACKQ" %%F IN (`jq -r ".token" "token.json"`) DO (
SET var=%%F
)
ECHO 
call vsce publish -p %var%
git push origin master