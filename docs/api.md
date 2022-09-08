# APIs needed #
A list of APIs needed based on different usr stories

## User

#### POST 
*Endpoint*  `/v1/users/users`

*Description*  
Create new user/participant

*Request Data*    
```
Field                   Type
--------                --------
first_name              string
last_name               string
location                string
username                string
no_of_users             positive integer
account_type(Choice)    string(Choice field)

{
    "first_name": "Foo",
    "last_name": "Bar",
    "location": "FooBar",
    "username": "FooBar",
    "no_of_users": 500,
    "account_type": (group, individual)
}
```

*Response*
```
Success
--------------------------------------------
| Status Code  |   Message
--------------------------------------------
| 200          |   User created successfully
--------------------------------------------

Error
--------------------------------------------
| Status Code  |   Message
--------------------------------------------
| 400          |   Bad Request
--------------------------------------------
```

#### GET
*Endpoint*  `/v1/users/users`

*Description*  
Get all users/participants

*Response data*    
```
Success
---------
Status Code     200

Data
[
    {
        "first_name": "Foo",
        "last_name": "Bar",
        "location": "FooBar",
        "username": "FooBar",
        "no_of_users": 500,
        "account_type": (group, individual)
    },
    {
        "first_name": "Foo",
        "last_name": "Bar",
        "location": "FooBar",
        "username": "FooBar",
        "no_of_users": 500,
        "account_type": (group, individual)
    }
]

Error
--------------------------------------------
| Status Code  |   Message
--------------------------------------------
| 400          |   Bad Request
--------------------------------------------
| 403          |   Unauthorized
--------------------------------------------
```

#### GET(Single user)
*Endpoint*  `/v1/users/users/<user-id>`

*Description*  
Get user detail that matches the id specified

*Response data*    
```
Success
---------
Status Code     200

Data
{
    "first_name": "Foo",
    "last_name": "Bar",
    "location": "FooBar",
    "username": "FooBar",
    "no_of_users": 500,
    "account_type": (group, individual)
}

Error
--------------------------------------------
| Status Code  |   Message
--------------------------------------------
| 400          |   Bad Request
--------------------------------------------
| 403          |   Unauthorized
--------------------------------------------
| 404          |   Not Found
--------------------------------------------
```

#### PATCH 
*Endpoint*  `/v1/users/users/<user-id>`

*Description*  
Update user detail specified by user-id

*Request Data*    
```
Field                   Type
--------                --------
first_name              string
last_name               string
location                string
username                string
no_of_users             positive integer
account_type(Choice)    string(Choice field)

{
    "field_name": "new data to replace old"
}
```

*Response*
```
Success
---------
Status Code     200

Data
{
    "first_name": "Foo",
    "last_name": "Bar",
    "location": "FooBar",
    "username": "FooBar",
    "no_of_users": 500,
    "account_type": (group, individual)
}

Error
--------------------------------------------
| Status Code  |   Message
--------------------------------------------
| 400          |   Bad Request
--------------------------------------------
| 403          |   Unauthorized
--------------------------------------------
| 404          |   Not Found
--------------------------------------------
```

#### DELETE 
*Endpoint*  `/v1/users/users/<user-id>`

*Description*  
Delete user specified by user-id

*Request Data*    
```
Field                   Type
--------                --------
first_name              string
last_name               string
location                string
username                string
no_of_users             positive integer
account_type(Choice)    string(Choice field)

{
    "field_name": "new data to replace old"
}
```

*Response*
```
Success
---------
Status Code     204


Error
--------------------------------------------
| Status Code  |   Message
--------------------------------------------
| 400          |   Bad Request
--------------------------------------------
| 403          |   Unauthorized
--------------------------------------------
| 404          |   Not Found
--------------------------------------------
```


## Web ##



### Modules (Categories)

POST `/v1/modules/categories/create`

Request 
```json
{
"name": "",
"description": "", 
"thumbnail_url": "",
"audio_url" : "",
"thumbnail_local": "thumbnail_local",
"audio_local": "",
"order" : "",
"lessons": []
}
```

Response 
```json
{
"name": "",
"description": "", 
"thumbnail_url": "",
"audio_url" : "",
"thumbnail_local": "thumbnail_local",
"audio_local": "",
"order" : 1,
"lessons": []
}
```

### Lessons & questions & activities 
List lessons with it's qestions and activities

#### CREATE LESSON

POST `/v1/modules/lessons/create`

Request
```json
{
"thumbnail_url"  : "",
"thumbnail_local": "",
"description" : "",
"audio_file_url": "",
"audio_file_location" : "",
"order": 1,
"questions": []
}
```

Response
```json
{
"thumbnail_url"  : "",
"thumbnail_local": "",
"description" : "",
"audio_file_url": "",
"audio_file_location" : "",
"order": 1,
"questions": []
}
```

### Questions

#### Create

POST ``

Request
```json
{
"text"  : "",
"description": "",
"questions" : [],
"question type": "",
"order" : "",
"answer": "",
"audio_url": "", 
"audio_local" : ""
}
```

Response
```json
{
"text"  : "",
"description": "",
"questions" : [],
"question type": "",
"order" : "",
"answer": "",
"audio_url": "", 
"audio_local" : ""
}
```

### Question Options

#### Create questions options

POST `/v1/modules/questions/questions-options/`

Request
```json
{
"text"  : "",
"thumbnail_url": "",
"thumbnail_local" : "",
"audio_url": "", 
"audio_local" : ""
}
```

Response
```json
{
"text"  : "",
"description": "",
"questions" : [],
"question type": "",
"order" : "",
"answer": "",
"audio_url": "", 
"audio_local" : ""
}
```

### Categorization/Sorting

POST: `api/v1/options/`

Description:  Create a new QuestionOption(sub-option). This is the way we usually add new options.

Request Data:
```
{
	"text": "irregular",
	"thumbnail": "/path",
	"audio_file": "/path"
}
```
PATCH: `api/v1/options/<options_id>/`

Description:  Add/update a QuestionOption's  sub-option

Request Data:
```
   {
	   "sub_options": ["eb687fb6-07f0-47bd-8dbf-9fb50154e4d7"]
   }
```
sub_options is a list of options ids

GET: `api/v1/options/<options_id>/`

Response Data:

```
        {
            "id": "c9582f96-aa4f-455f-b33c-9d3bf4c46c6d",
            "sub_options": [
                {
                    "created": "2020-07-27T10:54:01.536715Z",
                    "modified": "2020-07-27T10:54:01.536715Z",
                    "id": "eb687fb6-07f0-47bd-8dbf-9fb50154e4d7",
                    "text": "irregular",
                    "thumbnail": "/path",
                    "audio_file": "/path",
                    "is_answer": false
                },
                {
                    "created": "2020-07-27T10:19:55.532932Z",
                    "modified": "2020-07-27T10:19:55.532932Z",
                    "id": "4ec801d3-c205-477f-96c1-880b40d044c8",
                    "text": "regular",
                    "thumbnail": "/path",
                    "audio_file": "/path",
                    "is_answer": false
                }
            ],
            "created": "2020-06-18T13:00:21.129000Z",
            "modified": "2020-07-27T11:05:37.280916Z",
            "text": "Use your savings",
            "thumbnail": "/path",
            "audio_file": "/path",
            "is_answer": false
        }
```

DELETE: `api/v1/options/<options_id>/`

Description: Delete a collection of sub-options from a particular QuestionOption object

Request Data:

```
   {
	   "sub_options": ["eb687fb6-07f0-47bd-8dbf-9fb50154e4d7"]
   }
```
sub_options is a list of options ids

Pending: How to handle answers(from sub-options)?? Any ideas?

## Data exports ##
Data exports API spec and filters

### Users ###
GET [Base URL]/api/v1/exports/users/

Filters
name <string>: search first, last name & username. Case insensitive. Optional
location <int>: multiple location IDs. Optional
account type <string>. Optional
phone number <string>. Search case insensitive. Optional

Response
```json
{
  "fileurl": "<some file URL>"
}
```

### Category ###
GET [Base URL]/api/v1/exports/categories/

Filters
name <string>: search name. Case insensitive. Optional
start and end dates <date>. Dates between end_time and start_time. Optional
user <int>. List of users. Optional

Response
```json
{
  "fileurl": "<some file URL>"
}
```

### Lesson ###
GET [Base URL]/api/v1/exports/lessons/

Filters
name <string>: search name. Case insensitive. Optional
start and end dates <date>. Dates between end_time and start_time. Optional
user <int>. List of users. Optional
category <int>. List of categories. Optional

Response
```json
{
  "fileurl": "<some file URL>"
}
```

### Answers ###
GET [Base URL]/api/v1/exports/answers/

Filters
user <int>. List of users. Optional
category <int>. List of categories. Optional
lesson <int>. List of lessons. Optional
question <int>. List of questions. Optional
is_answer <boolean>. Correct or incorrect answers. Optional

Response
```json
{
  "fileurl": "<some file URL>"
}
```
## Media files

### Upload media files

Allow users to upload images or audio files to AWS bucket

POST `api/v1/learning/media/uploads/`

Response `200 OK`
```json
  [
    {
        "id": 33,
        "created": "2020-08-10T15:55:26.811211Z",
        "modified": "2020-08-10T15:55:26.811211Z",
        "file_name": "Screenshot_1588853977.png",
        "file_path": "https://busara-lenga.s3.amazonaws.com/Screenshot_1588853977.png/",
        "file_description": "Good file",
        "is_deleted": false
    },
    {
        "id": 34,
        "created": "2020-08-10T15:55:28.450162Z",
        "modified": "2020-08-10T15:55:28.450162Z",
        "file_name": "Screenshot_1588857858.png",
        "file_path": "https://busara-lenga.s3.amazonaws.com/Screenshot_1588857858.png/",
        "file_description": "Good file",
        "is_deleted": false
    }

  ]

```

### Update, Retrieve, Delete Media Files
POST `api/v1/learning/media/uploads/<id>/`

````
Field                   Type
--------                --------
id                       integer

````

Response `200 OK`
```json
{
    "id": 33,
    "created": "2020-08-10T15:55:26.811211Z",
    "modified": "2020-08-10T15:55:26.811211Z",
    "file_name": "Screenshot_1588853977.png",
    "file_path": "https://busara-lenga.s3.amazonaws.com/Screenshot_1588853977.png",
    "file_description": "Good file",
    "is_deleted": false
}
```
### List Media Files
POST `/api/v1/learning/media/uploads/?<id>/`

````
Field                   Type
--------                --------
id(optional)             integer

````

Response `200 OK`
```json
[
    {
        "id": 33,
        "created": "2020-08-10T15:55:26.811211Z",
        "modified": "2020-08-10T15:55:26.811211Z",
        "file_name": "Screenshot_1588853977.png",
        "file_path": "https://busara-lenga.s3.amazonaws.com/Screenshot_1588853977.png/",
        "file_description": "Good file",
        "is_deleted": false
    },
    {
        "id": 34,
        "created": "2020-08-10T15:55:28.450162Z",
        "modified": "2020-08-10T15:55:28.450162Z",
        "file_name": "Screenshot_1588857858.png",
        "file_path": "https://busara-lenga.s3.amazonaws.com/Screenshot_1588857858.png/",
        "file_description": "Good file",
        "is_deleted": false
    }

  ]

```

Based on admin/web user story
- Login 
- User/system controls 
  - Users
  - Modules/categories 
  - Lessons 
  - Questions 
  - Answers
- Data exports
  - Lesson tracking
  - Question tracking
  - Module tracking
- Dashboard
  - Add potential APIs later





