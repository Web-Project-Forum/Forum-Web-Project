<img src="https://webassets.telerikacademy.com/images/default-source/logos/telerik-academy.svg)" alt="logo" width="300px" style="margin-top: 20px;"/>

# Forum-Web-Project

## 1. Project description
Design and implement a Forum System and provide RESTful API that can be consumed by different clients. High-level description:
- Users can read and create topics and message other users
- Administrators manage users, topics and categories

## 2. Instructions on how to setup and run the project locally

### 1) You need to have MariaDb server . You can install it from here - https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.3.2

### 2) You can set local virtual environment using your terminal and the commands are:
- For Linux/Mac: 
    - `python3 -m venv .venv`
    - `.venv/bin/activate`
- For Windows: 
    - `py -m venv .venv`
    - `.venv\Scripts\activate`

### 3) The modules that are used for this project can be found in `requirements.txt`. You can install them in your terminal using the command:
- For Linux/Mac: 
    - `python3 -m pip install -r requirements.txt`
- For Windows: 
    - `py -m pip install -r requirements.txt`

### 4) After you have registration for MariaDb you need to put your password so you can run a server. In file `server/data/database.py` in the function called `_get_connection()` on line 10 you can put your password   
- `password = {"YOUR_PASSWORD"}`

As well you need to set a key word that is used to create secure tokens in file `server/data/models.py` on line 82.
- `KEY = {"YOUR_KEY"}`

### 5) When you are ready with the instructions above you need to be in the folder where is the `main.py` file to start your server. You can use the command.
- `uvicorn main:app`

### 5) Once your server is on you can use `Postman` or your browser to check the functionality of the API
- `https://www.postman.com/downloads/`


## Schema:

-    ![Alt text](schema_image.png)

## 3. End Points

### `Users`

-  @POST - http://127.0.0.1:8000/users/register

Body input:
```
{
    "id":3,
    "username":"JT",
    "password":"B1234",
    "role":"user",
    "email": "jt1990@abc.com"
}
```
Body ouput if body valid:
```
{
    "id": 11,
    "username": "JT",
    "password": "*********",
    "role": "user",
    "email": "jt1990@abc.com"
}
```

-  @POST - http://127.0.0.1:8000/users/login

Body input:
```
{
    "username":"JT",
    "password":"B1234",
}
```
Body ouput if body valid:
```
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTEsInVzZXJuYW1lIjoiSlQiLCJyb2xlIjoidXNlciIsImlhdCI6MTcxNTI3MzMzMCwiZXhwIjoxNzE1MjgwNTMwfQ.Z3bfq2dvtiikv_tvQ1PgvYLmRQoRGd8CSmoq-4jRvoU"
}
```

-  @GET - http://127.0.0.1:8000/users/info

Body ouput if body valid:
```
{
    "id": 10,
    "username": "Ben",
    "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
    "role": "user",
    "email": "ben1987@gmail.com"
}
```

### `Messages`
-  @POST- http://127.0.0.1:8000/messages/{id}

Body input:
```
{
    "text":"HELLO"
}
```

Body ouput if body valid:
```
{
    "id": 27,
    "text": "HELLO",
    "date": "21:47:24, 05/09/2024",
    "sender_id": 4,
    "receiver_id": 1
}
```

-  @GET - http://127.0.0.1:8000/messages/

Body ouput if body valid:
```
[
    {
        "id": 1,
        "username": "Ben",
        "role": "user"
    },
    {
        "id": 2,
        "username": "JT",
        "role": "user"
    },
    {
        "id": 3,
        "username": "romario",
        "role": "admin"
    }
]
```

-  @GET - http://127.0.0.1:8000/messages/{id}
```
{
    "user": {
        "id": 4,
        "username": "laura",
        "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
        "role": "user",
        "email": "laura@gmail.com"
    },
    "messages": [
        {
            "id": 27,
            "text": "HELLO",
            "date": "2024-05-09T21:47:24",
            "sender_id": 4,
            "receiver_id": 1
        },
        {
            "id": 28,
            "text": "Hi",
            "date": "2024-05-09T21:47:29",
            "sender_id": 1,
            "receiver_id": 4
        },
        {
            "id": 30,
            "text": "How are you?",
            "date": "2024-05-09T21:47:37",
            "sender_id": 4,
            "receiver_id": 1
        },
        {
            "id": 31,
            "text": "Fine",
            "date": "2024-05-09T21:47:37",
            "sender_id": 1,
            "receiver_id": 4
        }
    ]
}
```

### `Categories`



-  @POST- http://127.0.0.1:8000/categories/

Body input:
```
{
        "id": 1,
        "name": "Python57",
        "is_private": 0,
        "is_locked": 0
}
```

Body ouput if body valid:
```
{
        "id": 1,
        "name": "Python57",
        "is_private": 0,
        "is_locked": 0
}
```

-  @PUT- http://127.0.0.1:8000/categories/{id}

Body input:
```
{
        "id": 1,
        "name": "Python57",
        "is_private": 0,
        "is_locked": 1
}
```

Body ouput if body valid:
```
{
        "id": 1,
        "name": "Python57",
        "is_private": 0,
        "is_locked": 1
}
```

-  @GET- http://127.0.0.1:8000/categories/

- Categories get params as: 
    - skip = `0`
    - take = `5`
    - search = `str` or `None`
    - sorting = `None` or (`asc` or `desc`)
    - sort_by = `id` or (`is_private` or `name`)


Body ouput if body valid:
```
[
    {
        "id": 1,
        "name": "Python57",
        "is_private": 0,
        "is_locked": 0
    },
    {
        "id": 2,
        "name": "Tiger99",
        "is_private": 0,
        "is_locked": 0
    },
    {
        "id": 7,
        "name": "Panda66",
        "is_private": 0,
        "is_locked": 1
    }
]
```

-  @GET- http://127.0.0.1:8000/categories/{id}

Body ouput if body valid:
```
{
    "category": {
        "id": 3,
        "name": "Bear88",
        "is_private": 1,
        "is_locked": 0
    },
    "topics": [
        {
            "id": 1,
            "title": "Meeting",
            "content": "Tomorrow we have meeting at 8:00 o'clock.",
            "best_reply_id": 0,
            "locked": false,
            "categories_id": 3,
            "author_id": 4
        }
    ]
}
```
-  @DELETE- http://127.0.0.1:8000/categories/{id}

Body ouput if body valid:

```
'Category {id} was deleted'
```

### `Permissions`

- @GET - http://127.0.0.1:8000/permissions/{category_id}

Body ouput:
```
[
    {
        "category_id": 3,
        "user_id": 1,
        "write_permission": false
    },
    {
        "category_id": 3,
        "user_id": 4,
        "write_permission": true
    }
]
```

- @POST - http://127.0.0.1:8000/permissions/all

Body input:
```
{
    "category_id":3,
    "user_id":2,
    "write_permission":1
}
```

Body ouput if body valid:
```
Permission created!
```

- @POST - http://127.0.0.1:8000/permissions/all

Body input:
```
{
    "category_id":3,
    "user_id":2,
    "write_permission":0
}
```

```
Read permission created!
```

- @PUT - http://127.0.0.1:8000/permissions/

Body input:
```
{
    "category_id":3,
    "user_id":2,
    "write_permission":1
}
```
Body ouput if body valid:
```
Permission updated!
```


- @DELETE - http://127.0.0.1:8000/permissions/

Body input:
```
{
    "category_id":3,
    "user_id":2,
    "write_permission":1
}
```

Body ouput if body valid:
```
Permissions for user 2 are removed!
```

### `Topics`

- @GET - http://127.0.0.1:8000/topics/

- Topics get params as: 
    - skip = `0`
    - take = `5`
    - search = `str` or `None`
    - sorting = `None` or (`asc` or `desc`)
    - sort_by = `id` or (`best_reply_id` or `title`)

Body ouput:
```
[
    {
        "id": 1,
        "title": "Meeting",
        "content": "Tomorrow we have meeting at 8:00 o'clock.",
        "best_reply_id": 0,
        "locked": false,
        "categories_id": 3,
        "author_id": 4
    },
    {
        "id": 2,
        "title": "Class is cancelled!",
        "content": "Friday all classes are cancelled!",
        "best_reply_id": 0,
        "locked": false,
        "categories_id": 3,
        "author_id": 1
    }
]
```
- @GET - http://127.0.0.1:8000/topics/{id}

Body output:
```
{
    "topic": {
        "id": 1,
        "title": "Meeting",
        "content": "Tomorrow we have meeting at 8:00 o'clock.",
        "best_reply_id": 0,
        "locked": false,
        "categories_id": 3,
        "author_id": 4
    },
    "replies": [
        {
            "id": 1,
            "text": "I'm coming",
            "topics_id": 1,
            "author_id": 1
        },
        {
            "id": 2,
            "text": "I'm out of town.  I can't come.",
            "topics_id": 1,
            "author_id": 2
        }
    ]
}
```

- @POST - http://127.0.0.1:8000/topics

Body input:
```
{
    "id": 1,
    "title": "Q&A",
    "content": "Tomorrow we have Q&A session at 8:00 o'clock.",
    "best_reply_id": 0,
    "locked": false,
    "categories_id": 3,
    "author_id": 3
}
```

Body ouput if body valid:
```
{
    "id": 6,
    "title": "Q&A",
    "content": "Tomorrow we have Q&A session at 8:00 o'clock.",
    "best_reply_id": 0,
    "locked": false,
    "categories_id": 3,
    "author_id": 3
}
```

- @PUT - http://127.0.0.1:8000/topics/{id}

Body input:
```
{
    "id": 1,
    "title": "Q&A",
    "content": "Tomorrow we have Q&A session at 8:00 o'clock.",
    "best_reply_id": 1,
    "locked": false,
    "categories_id": 3,
    "author_id": 3
}
```

Body ouput if body valid:
```
{
    "id": 6,
    "title": "Q&A",
    "content": "Tomorrow we have Q&A session at 8:00 o'clock.",
    "best_reply_id": 1,
    "locked": true,
    "categories_id": 3,
    "author_id": 3
}
```

### `Replies`

- @GET - http://127.0.0.1:8000/replies/

Body ouput:
```
[
    {
        "id": 1,
        "text": "I'm coming",
        "topics_id": 1,
        "author_id": 1
    },
    {
        "id": 2,
        "text": "I'm out of town.  I can't come.",
        "topics_id": 1,
        "author_id": 2
    },
    {
        "id": 3,
        "text": "No way!",
        "topics_id": 2,
        "author_id": 1
    }
]
```

- @GET - http://127.0.0.1:8000/replies/{id}

Body ouput:
```
{
    "id": 1,
    "text": "I'm coming",
    "topics_id": 1,
    "author_id": 1
}
```

- @POST - http://127.0.0.1:8000/replies/{id}

Body input:
```
{
    "id": 1,
    "text": "I'm ON MY WAY. Stuck in the trafic",
    "topics_id": 1,
    "author_id": 1
}
```

Body ouput if body valid:
```
{
    "id": 6,
    "text": "I'm ON MY WAY. Stuck in the trafic",
    "topics_id": 1,
    "author_id": 3
}
```

### `Votes`

- @POST - http://127.0.0.1:8000/votes/{reply_id}

Body input:
```
{
    "vote":"down"
}
```

or 
```
{
    "vote":"up"
}
```

Body ouput if body valid:
```
{
    "replies_id": 2,
    "users_id": 3,
    "vote": -1,
    "is_changed": false
}
```

- @PUT- http://127.0.0.1:8000/votes/{reply_id}

Body input:
```
{
    "vote":"up"
}
```
Body ouput if body valid:
```
{
    "replies_id": 2,
    "users_id": 3,
    "vote": 1,
    "is_changed": false
}
```

- @GET- http://127.0.0.1:8000/votes/{reply_id}
```
[
    1
]
```

