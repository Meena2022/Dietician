# Dietician

Below Tools are required, please follow the steps for reference

Download DynamoDB from below link https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html#DynamoDBLocal.DownloadingAndRunning.title

Below are the steps to run the server locally 
Download the archive, -->extract the contents —--->copy the extracted directory to a location on the computer.

To start DynamoDB on your computer, open a command prompt window, navigate to the directory where you extracted DynamoDBLocal.jar, and enter the following command.
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

NoSQL Workbench IDE:-  Download NoSQL workbench from below link
 
https://s3.amazonaws.com/nosql-workbench/NoSQL%20Workbench-win-3.3.0.exe

Python: - Install latest version of python from https://www.python.org/

PyCharm: - This is the Python IDE. Install the community version from https://www.jetbrains.com/pycharm

1)	Clone the repository from below link 
    https://github.com/Meena2022/Dietician

2)	Create a virtual environment in the project folder using below command 
    python -m venv venv

3)	Activate the virtual environment with below steps
    1.	Open terminal in pycharm 
    2.	Go to your project directory, where you create your virtual environment for this project.
    3.	run this command-> .\venv_name\Scripts\activate.
 
4)	Install the requirement.txt file using below command
    pip install -r requirements.txt

5)	Start the server with below command 
    flask run
    server starts on this port
    http://127.0.0.1:5000/






 


