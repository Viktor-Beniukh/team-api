# Team Management API

API service for team management with the ability to assigning people to a team


### Installing using GitHub

- Python3 must be already installed
- Install PostgreSQL and create db

```shell
git clone https://github.com/Viktor-Beniukh/team-api.git
cd team-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver   
```
You need to create `.env` file and add there the variables with your according values:
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;

  
## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up`


## Features

- Admin panel /admin/;
- Implementing user authentication from the api page;
- Documentation is located at /api/doc/swagger/;
- Creating, updating and deleting teams, people(only admin);
- Filtering teams by name;
- Filtering people by last name;
- Assigning a person to a team(only admin).


### How to create superuser
- Run `docker-compose up` command, and check with `docker ps`, that services are up and running;
- Create new admin user. Enter container `docker exec -it <container_name> bash`, and create in from there.


### What do APIs do

- [GET] /api/ - obtains a list of endpoints;

- [GET] /api/teams/ - obtains a list of teams with the possibility of filtering by name;
- [GET] /api/people/ - obtains a list of persons with the possibility of filtering by last name;

- [GET] /api/teams/id/ - obtains the specific team information data;
- [GET] /api/people/id/ - obtains the specific person data;

- [POST] /api/teams/ - creates a team;
- [POST] /api/people/ - creates a person;

- [PUT] /api/teams/id/ - updates the specific team information data;
- [PUT] /api/people/id/ - updates the specific person data;
- [PUT] /api/people/id/assign-to-team/ - assigns the specific person to a team;

- [DELETE] /api/teams/id/ - removes the specific team;
- [DELETE] /api/people/id/ - removes the specific person; 


### Checking the endpoints functionality
- You can see detailed APIs at swagger page: `http://127.0.0.1:8000/api/doc/swagger/`.


## Testing

- Run tests using different approach: `docker-compose run app sh -c "python manage.py test"`.


## Check project functionality

Superuser credentials for test the functionality of this project:
- email address: `alex.shevelo@gmail.com`;
- password: `adminuserpassword`.
