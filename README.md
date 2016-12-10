# CLI_ContactManager-SMS_App
A console application for contact management and sending SMS

**Installation**

`$ git clone https://github.com/giddygitau/contactmanager.git`

`$ cd contactmanager`
 
 Create and activate a virtual environment.
 
 ```
 $ virtualenv .env
 $ source .env/bin/activate
 ```
 
 Install dependencies
 
 `$ pip install -r requirements.txt`


Create the database by running the following command

```

 python ./lib/database/table_def.py

```


 **Commands**
 
 ```
 app.py (-i | --interactive)
 app.py (-h | --help )
 app.py (-v | --version)
 Contact-Manager$: add -f <first_name> -l <last_name> -p <phone_number>
 Contact-Manager$: view
 Contact-Manager$: search <first_name>
 Contact-Manager$: edit <first_name>
 Contact-Manager$: del <first_name>
 Contact-Manager$: text <first_name> -m <message>
 Contact-Manager$: sync
 Contact-Manager$: help

```
 