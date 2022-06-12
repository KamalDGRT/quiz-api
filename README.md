# Quiz API

API Endpoints to be used in the Quiz App.

### How to setup the project

* Clone the repo.
* Go inside the root folder of the project and open a
    Terminal/Command Prompt there.
* Create a python virtual environment there.
* You can do that by
    * `pip install virtualenv`
    * `py -m venv env`
* Activate the virtual environment according to the OS that you have.
* For Windows - `env\Scripts\activate.bat`
* For Linux/Mac - `source env/bin/activate`
* Install the dependencies: `pip install -r requirements.txt`
* Copy the `.env-example` file and create a new file `.env`
* Create a database in the `mysql` server that you have.
* In the `.env` file, fill up the appropriate details.
* After you enter the database details in the above step, run this
  command to autogenerate the tables for the above database:
  `alembic upgrade head`
* After that, you may run the project by executing this command:
    `uvicorn app.main:app --reload`
