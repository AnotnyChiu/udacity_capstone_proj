# Udacity Casting API

## Description
This is a casting api for udacity FSND capstone project. This api allows normal client users to view actors,movies,directors, and casting information. Also a assistant or producer can manipulate those information.

Api itself is a flask project which use sqlAlchemy ORM and postgres database. For authentication, Auth0 is served as the third party authentication system for the application.

This api can be run locally, and it's also deployed on heroku. 
- https://antony-chiu-udacity-capstone.herokuapp.com


---

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3 and pip installed on their local machines.

From the starter folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `app.py` file. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).
The application is run on `http://0.0.0.0:8080/` by default. 

---
## Authentication Setup

To get authentication setup:
- 1. Access the `GET/api/login` endpoint of the api. This will redirect the page to Auth0 login page.
- 2. Login with your email and password, get the JWT sent back.
- 3. Since this is a backend only project, when accessing endpoints with bearer token, postman is recommended.

---
## Data Models


```
  1. Movie: basic info about a movie
```
| Column | Type | Description ( * for required field)               |
| :-------- | :------- | :------------------------- |
| `id` | `Integer` | * Movie ID (Primary key) |
| `title` | `String` | * Movie title |
| `release_date` | `TimeStamp` | * Release date of the movie |
| `director_id` | `integer` | * Movie director's ID (Foreign key) |

```
  2. Actor: basic info about an actor
```
| Column | Type | Description ( * for required field)               |
| :-------- | :------- | :------------------------- |
| `id` | `Integer` | * Actor ID (Primary key) |
| `name` | `String` | * Actor's name |
| `age` | `Integer` | * Actor's age |
| `gender` | `String` | * Actor's gender (in form of 'male' of 'female') |

```
  3. Director: basic info about a director
```
| Column | Type | Description ( * for required field)               |
| :-------- | :------- | :------------------------- |
| `id` | `Integer` | * Director ID (Primary key) |
| `name` | `String` | * Director's name |
| `age` | `Integer` | * Director's age |
| `gender` | `String` | * Director's gender (in form of 'male' of 'female') |

```
  4. MovieActor: Joint object for many to many relationship between movies and actors
```
- An actor can participate in several different movies.
- A movie's cast has several actors.
- Also an actor get different pay from each movie.

| Column | Type | Description ( * for required field)               |
| :-------- | :------- | :------------------------- |
| `id` | `Integer` | * Director ID (Primary key) |
| `actor_id` | `Integer` | * Actor ID (Foreign key)|
| `movie_id` | `Integer` | * Movie ID (Foreign key) |
| `actor_pay` | `Integer` | Actor's pay from the movie (in US dollars) |


---

## API Reference

### 1. Getting Started
- Base URL: This app can be run locally and is also held on Heroku. The backend app is hosted at the default 0.0.0.0, port 8080
- Heroku application Base URL: https://antony-chiu-udacity-capstone.herokuapp.com
- Authentication: Application perform RBAC control and requires several authentication through JWT. Roles and Permissions seen as below

### 2. Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return error types as below when requests fail:
- 400: Bad Request
- 401: Forbidden (with detailed error message)
- 403: Unauthorized (with detailed error message)
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

### 3. RBAC - Roles and Permissions

| Role | Description | 
| :-------- | :------- |
| `Client` | `Who can view the movies' info` |
| `Casting Assistant ` | `Who can add new movie and new actor, also update the info` |
| `Executive Producer` | `Who can perform all actions, include deleting the entity as well as assign actor to movie and decide the pay` |

| Permission | Assigned role | 
| :-------- | :------- |
| `get:movies` | `All` |
| `get:actors` | `All` |
| `get:directors` | `All` |
| `get:movieactors` | `All` |
| `post:movies` | `Casting Assistant, Executive Producer` |
| `post:actors` | `Casting Assistant, Executive Producer` |
| `post:directors` | `Casting Assistant, Executive Producer` |
| `post:movieactors` | `Executive Producer` |
| `put:movies` | `Casting Assistant, Executive Producer` |
| `put:actors` | `Casting Assistant, Executive Producer` |
| `put:directors` | `Casting Assistant, Executive Producer` |
| `put:movieactors` | `Executive Producer` |
| `delete:movies` | `Executive Producer` |
| `delete:actors` | `Executive Producer` |
| `delete:directors` | `Executive Producer` |
| `delete:movieactors` | `Executive Producer` |



### 4. Endpoints
- 21 endpoints in total
- (1) for welcome message
- (2) for redirect to login page on auth0
- (3)-(7) for movies
- (8)-(12) for actors
- (13)-(17) for directors
- (18)-(21) for movie_actors

#### (1) Welcome page

```http
  GET /api/
```
- sample request- http://192.168.1.97:8080/ (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/ (heroku)
- sample response:

```
Welcome To My Casting API!
```

#### (2) Login page

```http
  GET /api/login
```
- sample request- http://192.168.1.97:8080/login (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/login (heroku)
- response: redirect to auth0 login page

#### (3) Get all movies

```http
  GET /api/movies (requires auth - 'get:movies' )
```
- sample request- http://192.168.1.97:8080/movies (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movies (heroku)
- sample response:
```
{
    "movies": [
        {
            "actors": [
                {
                    "age": 22,
                    "gender": "male",
                    "id": 7,
                    "name": "test_actor",
                    "pay": 10000
                },
                {
                    "age": 22,
                    "gender": "male",
                    "id": 8,
                    "name": "test_actor",
                    "pay": 10000
                }
            ],
            "director": {
                "age": 25,
                "gender": "male",
                "id": 1,
                "name": "antony"
            },
            "id": 2,
            "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
            "title": "test_movie"
        },
        {
            "actors": [
                {
                    "age": 22,
                    "gender": "male",
                    "id": 8,
                    "name": "test_actor",
                    "pay": 10000
                }
            ],
            "director": {
                "age": 25,
                "gender": "male",
                "id": 1,
                "name": "antony"
            },
            "id": 3,
            "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
            "title": "test_movie"
        },
    ],
    "success": true
}
```

#### (4) Get single movie by movie id

```http
  GET /api/movies/${movie_id} (requires auth - 'get:movies' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `movie_id` | `Integer` | **Required**. Id of movie to fetch |

- sample request- http://192.168.1.97:8080/movies/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movies/1 (heroku)
- sample response:
```
{
    "movie": {
        "actors": [
            {
                "age": 22,
                "gender": "male",
                "id": 8,
                "name": "test_actor",
                "pay": 10000
            }
        ],
        "director": {
            "age": 25,
            "gender": "male",
            "id": 1,
            "name": "antony"
        },
        "id": 1,
        "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
        "title": "test_movie"
    },
    "success": true
}
```

#### (5) Post movie

```http
  POST /api/movies (requires auth - 'post:movies' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `movie` | `Movie Object` | **Required**. new movie to add |

- sample request- http://192.168.1.97:8080/movies (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movies (heroku)
- sample request body:
```
{
    "title": "fly me to the moon",
    "release_date": "2021-09-30",
    "director_id": 1
}
```
- sample response:
```
{
    "new_movie": 39,
    "success": true
}
```

#### (6) Put movie

```http
  PUT /api/movies/${movie_id} (requires auth - 'put:movies' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `movie_id` | `Integer` | **Required**. Id of target movie |
| `movie` | `Movie Object` | **Required**. updated movie object |

- sample request- http://192.168.1.97:8080/movies/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movies/1 (heroku)
- sample request body:
```
{
    "title": "fly me to the moon",
    "release_date": "2021-09-30",
    "director_id": 1
}
```
- sample response:
```
{
    "success": true,
    "updated_movie": {
        "actors": [],
        "director": {
            "age": 25,
            "gender": "male",
            "id": 1,
            "name": "antony"
        },
        "id": 1,
        "release_date": "Wed, 29 Sep 2021 16:00:00 GMT",
        "title": "fly me to the moon"
    }
}
```

#### (7) Delete movie

```http
  DELETE /api/movies/${movie_id} (requires auth - 'delete:movies' )
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `movie_id` | `Integer` | **Required**. Id of target movie to delete |

- sample request- http://192.168.1.97:8080/movies/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movies/1 (heroku)
- sample response:
```
{
    "deleted_movie": 1,
    "success": true
}
```

#### (8) Get all actors

```http
  GET /api/actors (requires auth - 'get:actors' )
```
- sample request- http://192.168.1.97:8080/actors (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/actors (heroku)
- sample response:
```
{
    "actors": [
        {
            "age": 22,
            "gender": "male",
            "id": 1,
            "movies": [],
            "name": "test_actor"
        },
        {
            "age": 22,
            "gender": "male",
            "id": 8,
            "movies": [
                {
                    "id": 2,
                    "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                    "title": "test_movie"
                },
                {
                    "id": 3,
                    "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                    "title": "test_movie"
                }
            ],
            "name": "test_actor"
        },
        {
            "age": 22,
            "gender": "male",
            "id": 30,
            "movies": [
                {
                    "id": 10,
                    "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                    "title": "test_movie"
                }
            ],
            "name": "test_actor"
        },
    ],
    "success": true
}
```

#### (9) Get single actor by actor id

```http
  GET /api/actors/${actor_id} (requires auth - 'get:actors' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `actor_id` | `Integer` | **Required**. Id of actor to fetch |

- sample request- http://192.168.1.97:8080/actors/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/actors/1 (heroku)
- sample response:
```
{
    "actor": {
        "age": 22,
        "gender": "male",
        "id": 1,
        "movies": [
            {
                "id": 2,
                "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                "title": "test_movie"
            },
            {
                "id": 3,
                "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                "title": "test_movie"
            }
        ],
        "name": "test_actor"
    },
    "success": true
}
```

#### (10) Post actor

```http
  POST /api/actors (requires auth - 'post:actors' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `actor` | `Actor Object` | **Required**. new actor to add |

- sample request- http://192.168.1.97:8080/actors (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/actors (heroku)
- sample request body:
```
{
   "name": "Antony Chiu",
   "age": 25,
   "gender": "male"
}
```
- sample response:
```
{
    "new_actor": 39,
    "success": true
}
```

#### (11) Put actor

```http
  PUT /api/actors/${actor_id} (requires auth - 'put:actors' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `actor_id` | `Integer` | **Required**. Id of target actor |
| `actor` | `Actor Object` | **Required**. updated actor object |

- sample request- http://192.168.1.97:8080/actors/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/actors/1 (heroku)
- sample request body:
```
{
   "name": "Antony Chiu",
   "age": 25,
   "gender": "male"
}
```
- sample response:
```
{
    "success": true,
    "updated_actor": {
        "age": 25,
        "gender": "male",
        "id": 1,
        "movies": [],
        "name": "Antony Chiu"
    }
}
```

#### (12) Delete actor

```http
  DELETE /api/actors/${actor_id} (requires auth - 'delete:actors' )
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `actor_id` | `Integer` | **Required**. Id of target actor to delete |

- sample request- http://192.168.1.97:8080/actors/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/actors/1 (heroku)
- sample response:
```
{
    "deleted_actor": 1,
    "success": true
}
```

#### (13) Get all directors

```http
  GET /api/directors (requires auth - 'get:directors' )
```
- sample request- http://192.168.1.97:8080/directors (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/directors (heroku)
- sample response:
```
{
    "directors": [
        {
            "age": 25,
            "gender": "male",
            "id": 1,
            "movies": [
                {
                    "id": 34,
                    "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                    "title": "test_movie"
                },
                {
                    "id": 2,
                    "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                    "title": "test_movie"
                },
                {
                    "id": 3,
                    "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                    "title": "test_movie"
                },
            ],
            "name": "antony"
        },
        {
            "age": 30,
            "gender": "female",
            "id": 2,
            "movies": [],
            "name": "test_director"
        },
    ],
    "success": true
}
```

#### (14) Get single director by director id

```http
  GET /api/directors/${director_id} (requires auth - 'get:directors' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `director_id` | `Integer` | **Required**. Id of director to fetch |

- sample request- http://192.168.1.97:8080/directors/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/directors/1 (heroku)
- sample response:
```
{
    "director": {
        "age": 25,
        "gender": "male",
        "id": 1,
        "movies": [
            {
                "id": 34,
                "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                "title": "test_movie"
            },
            {
                "id": 2,
                "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                "title": "test_movie"
            },
            {
                "id": 3,
                "release_date": "Mon, 20 Sep 2021 16:00:00 GMT",
                "title": "test_movie"
            },
        ],
        "name": "antony"
    },
    "success": true
}
```

#### (15) Post director

```http
  POST /api/directors (requires auth - 'post:directors' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `director` | `Director Object` | **Required**. new director to add |

- sample request- http://192.168.1.97:8080/directors (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/directors (heroku)
- sample request body:
```
{
   "name": "Kenny Robert",
   "age": 45,
   "gender": "male"
}
```
- sample response:
```
{
    "new_director": 38,
    "success": true
}
```

#### (16) Put director

```http
  PUT /api/directors/${director_id} (requires auth - 'put:directors' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `director_id` | `Integer` | **Required**. Id of target director |
| `director` | `Director Object` | **Required**. updated director object |

- sample request- http://192.168.1.97:8080/directors/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/directors/1 (heroku)
- sample request body:
```
{
   "name": "Kenny Robert",
   "age": 45,
   "gender": "male"
}
```
- sample response:
```
{
    "success": true,
    "updated_director": {
        "age": 45,
        "gender": "male",
        "id": 1,
        "movies": [],
        "name": "Kenny Robert"
    }
}
```

#### (17) Delete director

```http
  DELETE /api/directors/${director_id} (requires auth - 'delete:directors' )
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `director_id` | `Integer` | **Required**. Id of target director to delete |

- sample request- http://192.168.1.97:8080/directors/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/directors/1 (heroku)
- sample response:
```
{
    "deleted_director": 1,
    "success": true
}
```

#### (18) Get all movie_actors

```http
  GET /api/movie_actors (requires auth - 'get:movieactors' )
```
- sample request- http://192.168.1.97:8080/movie_actors (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movie_actors (heroku)
- sample response:
```
{
    "movie_actors": [
        {
            "actor_id": 30,
            "actor_pay": 20000,
            "id": 1,
            "movie_id": 10
        },
        {
            "actor_id": 7,
            "actor_pay": 10000,
            "id": 48,
            "movie_id": 2
        },
        {
            "actor_id": 8,
            "actor_pay": 10000,
            "id": 49,
            "movie_id": 2
        },
        {
            "actor_id": 8,
            "actor_pay": 10000,
            "id": 50,
            "movie_id": 3
        }
    ],
    "success": true
}
```


#### (19) Post movie_actor

```http
  POST /api/movie_actors (requires auth - 'post:movieactors' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `movie_actor` | `MovieActor Object` | **Required**. new movie_actor to add |

- sample request- http://192.168.1.97:8080/movie_actors (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movie_actors (heroku)
- sample request body:
```
{
    "actor_id": 1,
    "movie_id": 2,
    "actor_pay": 30000
}
```
- sample response:
```
{
    "new_movie_actor": 51,
    "success": true
}
```

#### (16) Put movie_actor

```http
  PUT /api/movie_actors/${movie_actor_id} (requires auth - 'put:movieactors' )
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `movie_actor_id` | `Integer` | **Required**. Id of target movie_actor |
| `movie_actor` | `MovieActor Object` | **Required**. updated movie_actor object |

- sample request- http://192.168.1.97:8080/movie_actors/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movie_actors/1 (heroku)
- sample request body:
```
{
    "actor_id": 1,
    "movie_id": 2,
    "actor_pay": 30000
}
```
- sample response:
```
{
    "success": true,
    "updated_movie_actor": {
        "actor_id": 1,
        "actor_pay": 30000,
        "id": 1,
        "movie_id": 2
    }
}
```

#### (17) Delete director

```http
  DELETE /api/movie_actors/${movie_actor_id} (requires auth - 'delete:movieactors' )
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `movie_actor_id` | `Integer` | **Required**. Id of target movie_actor |

- sample request- http://192.168.1.97:8080/movie_actors/1 (local)
- sample request- https://antony-chiu-udacity-capstone.herokuapp.com/movie_actors/1 (heroku)
- sample response:
```
{
    "deleted_movie_actor": 1,
    "success": true
}
```
---

## Deployment
### Currently Serving on Heroku:  https://antony-chiu-udacity-capstone.herokuapp.com
---
## Authors
Antony Chiu. Udacity student
