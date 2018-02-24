## Data Interview Project

First, we need to create a virtualenv and activate it.

1. pip install virtualenv
2. from desired directory: virtualenv peerfit_project
3. source peerfit_project/bin/activate
4. Your virtual environment should now be activated
5. From project directory, run: pip install -r requirements.txt

Now that you have the necessary python packages, clone the repo git@gitlab.com:dwmorrison33/peerfit-project.git and setup MySQL on your local machine.

To install MySQL on your local machine, execute the following commands:
1. **sudo apt-get update
2. sudo apt-get install mysql-server
3. You need to start server like: sudo service mysql restart and then check status like: sudo service mysql status
4. Sign in with the root user like:
	mysql -u root -p
5. Run the command: CREATE DATABASE peerfit;

You are all set with your database now. To create a table with all the data execute a command similar to following from the project/solution directory:

1. python project_solution.py localhost root Password123 peerfit

Thats it, you can now view all your data. If you entered the python command incorrectly, you should get a printout in your terminal that gives instuctions for Usage.