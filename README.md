## About
- This application was created as a result of a test task
- The purpose of the application is to build an online service for generating CSV files with fake (dummy) data using
Python and Django

## Technical Requirements
- Use PEP8 for your Python code
- Python 3
- Django
- Bootstrap, Bulma, UIKit, or any other similar framework for UI

## First:
```shell
git clone https://github.com/Fhockk/FakerCSVgenerator.git
```

## How to run this online service?
- Make sure you have python installed
- Open the terminal and hit the following command -

```shell
mkvirtualenv --python=python3.10 <virtualenv_name>
```
Change the directory:
```shell
cd FakerCSVgenerator/
```
Install the requirements
```shell
pip install -r requirements.txt
```

## Run the server
```shell
python manage.py runserver
```

And then open browser, go to [127.0.0.1:8000](http://127.0.0.1:8000/)

First, you need to login, enter the {
    username: admin,
    password: admin
}



- Endpoint which show all shemas [data_schemas](http://127.0.0.1:8000/data_schemas/)
- Endpoint which allow you create new shemas [new_schema](http://127.0.0.1:8000/new_schema/?)

**_For_** and **_To_** value is allowed only for Integer and Text (range number of sentences) Type.
- Endpoint where you can preview your CSV file and enter the number of rows to generate fake data.

By clicking on the Download button you can download your file when it is ready.
