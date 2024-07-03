# Book Managemnt System
Api system to manage books and authors, users able to register, login in and log out and after login able to do some actions for books like
list all books, retrieve specific book, add specific book, update or delete specific book.

## API Postman Documentation
https://documenter.getpostman.com/view/28439113/2sA3dxDrRG

## Prerequisite
>python

>postgressql (not required you use any database management system you prefer)


## Installtion & Running

     1- Create .env file and place these environment variables with your data:
         - SECRET_KEY
         - DATABASE_URL
         - TEST_DATABASE_URL
         - JWT_SECRET_KEY
         - FLASK_ENV
         - FLASK_DEBUG
         note: FLASK_ENV can be either development or testing) if you choose development your value for this variable DATABASE_URL is applied  if testing value for this variable TEST_DATABASE_URL is applied
               in another word development env use a database and testing use another one, you can make them both the same database but be aware that after tests are finsihed database tables are deleted.
               
      2- Create a virtual environment and activate thie venv using this commands
         - python -m venv venv
         - (source venv/bin/activate) for ubuntu activation
         - (venv/scripts/activate) for windows activation
         
      3- Install requirements 
         - pip install -r requirements.txt

      4- Create a database and make sure to include the path in DATABASE_URL env variable
         
      5- flask db upgrade
         - For running migrations
         
      6- flask run
         - App is running on port 5000

  ## Testing

         To run unit tests make sure:
          - Set TEST_DATABASE_URL with your prefered database engine
         Run  
           - python -m unittest test
       
