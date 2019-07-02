## Docker via MSC

## before install brew correctly go to slack -> #bot ->> !brew
brew install python3

## /Users/$LOGNAME/.brew/bin/python3

pip3 install virtualenv

virtualenv -p   /Users/$LOGNAME/.brew/bin/python3 env/

env/bin/pip3 install -r requirements.txt


## To activate virtualenv
## source env/bin/activate
