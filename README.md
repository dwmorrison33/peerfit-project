## Data Interview Project

#### Create a virtual environment for your python packages

```sh
$ pip install virtualenv
```

**From desired directory:**
```sh
$ virtualenv peerfit_project
```

**Activate virtualenv**
```sh
$ source peerfit_project/bin/activate
```
Your virtual environment should now be activated

**Install required packages**
```sh
pip install -r requirements.txt**
```
Now that you have the necessary python packages, clone the repo git@gitlab.com:dwmorrison33/peerfit-project.git and setup MySQL on your local machine.

#### MySQL installation

```sh
$ sudo apt-get update
$ sudo apt-get install mysql-server
```
** Start mysql service**
```sh
sudo service mysql restart
sudo service mysql status
```
**Login to MySQL**
```sh
mysql -u root -p
```

#### Create a database for the project
```sh
CREATE DATABASE peerfit;
```

You are all set with your database now. To create a table with all the data, from the project/solution directory:

#### Usage

```sh
$ python <name_of_script> <host> <user> <password> <database>
```

* host - database host
* user - database username
* password - database password
* database - name of your database

#### Example command

```sh
$ python python project_solution.py localhost root Password123 peerfit
```

#### Final
Thats it, you can now view all your data. If you entered the python command incorrectly, you should get a printout in your terminal that gives instuctions for Usage.