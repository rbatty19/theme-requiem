FOR /F "tokens=* USEBACKQ" %%F IN (`jq -r ".version" "package.json"`) DO (
SET var=%%F
)
ECHO %var%