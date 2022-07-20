# Make My Day   
  
## Overview:  
  
Students in a class get one question a day by email or SMS or WhatsApp from their instructor at a time of their choice (e.g., morning 8 AM). By taking few minutes every day to answer one question, they improve their skills steadily throughout the semester. The questions are relevant to what is going on in class that week. If they give a correct answer, the system reinforces their answer and gives them more details.Otherwise, it tells when why they are wrong and tells them more information about the correct answer. There may also be optional reading material on the question for the student to learn more.  
  
## Links:  
  
Mysql commands:  
https://linuxhint.com/mysql-commands-tutorial/  
  
Django Tutorial:    
https://youtube.com/playlist?list=PLzMcBGfZo4-kQkZp-j9PNyKq7Yw5VYjq9  
  
MySQL installation:  
https://youtu.be/IiUYyZo2gTk  
  
MySQL path for zsh:  
https://stackoverflow.com/questions/35858052/how-to-fix-command-not-found-mysql-in-zsh  
  
Flower Installation:  
https://flower.readthedocs.io/en/latest/install.html    
  
# Running with Docker:  
  
Make sure you have docker installed  
https://docs.docker.com/get-docker/  
  
In the command line, make your way to the "makemyday" directory (the outer one, not the app) and run:  
**docker-compose up**  

# Docker Setup with Windows
Proceed to website and install Docker for Windows: https://docs.docker.com/get-docker/

Go to Windows Features on your computer and enable Hyper-V and Containers

If a message stating WSL 2 installation is incomplete pops up, go to this link https://aka.ms/wsl2kernel and
download the latest package. 

In the command line, make your way to the "makemyday" directory (the outer one, not the app) and run:  
**docker-compose up**

  
# Running without Docker:  
  
If the above method did not work, below is a more detailed alternative way.  
  
## Installation:  
  
create a folder and place the repository inside  
python3 -m venv /the/folder/where/repository/lies  
To activate virtual environment from the folder:  
source bin/activate  
  
### Inside venv:  
  
pip install -r requirements.txt  
or   
brew install mysql  
pip install mysqlclient  
python -m pip install Django  
pip install django-crispy-forms  
pip install django-tables2  
pip install django-bootstrap-datepicker-plus  
pip install celery  
pip install django-celery-beat  
pip install flower  
  
extra step for Windows flower:  
in "venv/lib/site-packages/tornado/platform/asyncio.py" type  
import sys  
if sys.platform == "win32":  
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  
  
  
Installing RabbitMQ on Mac:  
https://www.rabbitmq.com/install-homebrew.html  
https://code2care.org/pages/permanently-set-path-variable-in-mac-zsh-shell  
brew install rabbitmq  
rabbitmq-server start  
or  
brew services start rabbitmq  
rabbitmqctl status  
brew services stop rabbitmq  
  
Installing RabbitMQ on Linux:  
https://www.youtube.com/watch?v=fBfzE0yk97k  
  
Installing RabbitMQ on Windows:  
https://www.youtube.com/watch?v=8lnybIaDz2M  
  
## Running Flower:  
  
celery flower -A makemyday --port=5555  
url: http://localhost:5555/  
  
## Running the website (Mac)  
  
The steps below detail the commands need to run the website for Mac. They should be somewhat the same for other operating systems.  
  
Steps **1-4** are only for the email/notifcation system.  
Steps **2-5** make sure your in the makemyday directory (the outer one, not the app itself).  
  
1. terminal 1: "rabbitmq-server start"  
This starts the messaging queue for the asyncronous sending of Email.
  
2. terminal 2: "celery -A makemyday worker -l info"  
This creates the celery worker for handling emails to be sent out.  
  
3. terminal 3: "celery flower -A makemyday --port=5555"  
For debugging purposes  
  
4. terminal 4: "celery -A makemyday beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"  
This is for checking the database for any scheduled emails to be sent out.  
  
5. terminal 5: "python manage.py runserver"  
Running the website itself  


