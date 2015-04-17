meet-street
=====
## Developer setup for Ubuntu
###Core packages
```
$ sudo apt-get install git pip
```

###Setting up virtualenv
This is only necessay if you work on a lot of Python projects. It's mainly to deal with package dependencies. It's not completely necessary, but its a good habit.
```
$ sudo apt-get install virtualenv
$ virtualenv <environment_name>
$ . <environment_name>/bin/activate
```
You'll see in your terminal that it has \<environment_name\> at the start of the line

### Installing packages
Run the following
```
$ git clone git@github.com:vincentt143/meet-street.git
$ cd meet-street
$ pip install -r requirements.txt
```
### Running the server
To start the server, run
```
$ python meet-street.py
```
Enjoy! You can access this at http://localhost:5000

#### PSA: Use 2 space indents (NO TABS PLEASE)
