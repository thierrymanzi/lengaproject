
## Mobile APIs ##
Based on mobile user story
- Participant sign up 
- Participant/group login 
- Profile 
- Feedback
- Send notifications 
- Lesson tracking 
- Question tracking 


### User

#### Sign Up 

##### Single User
Sign up single user

POST `/v1/users/user/signup/`

Request
```json
{
"username" : "user-name@example.com", 
"first_name" : "Jane", 
"last_name" : "Doe", 
"location" : ""
}
```

Response
```json
{
"username": "user-name@example.com",
"message" : "Account created"
}
```

##### Group

Sign up group account

POST `/v1/users/group/signup/`

Request

```json
{
"group_name" : "Group One",
"username": "group-name@example.com",
"location" : "", 
"number_of_users" : 12
}
```

Response
```json
{
"username": "group-name@example.com",
"message" : "Group account created"
}
```

#### Sign In

##### POST `/v1/users/user/login/`

Request
```json
{
"username" : "user@example.com", 
"password" : "hashh", 
"location" : ""
}
```

Response
```json
{
"first_name": "",
"last_name": "",
"location": "",
"number_of_users": "",
"username": "",
"account_type": "",
"current_lesson":  3
}
```

#### Sign Out
Logout 


POST `/v1/users/user/logout/`

Request

```json
{
"username" : "user@example.com"
}
```

Response
```json
{
"message": "user logged out"
}
```

### Modules (Categories) 

#### List Modules 

GET `/v1/categories/categories/`

Response
```json
{
  "modules": [
    {
        "name": "Track your money",
        "description": "Track your money",
        "order": 1, 
        "audio_file": "",
        "thumbnail" : "",
        "lessons" : [
           {
            "description": "Track your money",
            "thumbnail": "",
            "audio_file": "",
            "created": "2020-05-27 13:22:05.354824",
            "modified": "2020-05-27 13:22:05.354824",
            "order": 1,
            "module": 1
        }
       ]
    }, 
    {
        "name": "Make a budget",
        "order": 2, 
        "audio_file": "",
        "thumbnail" : "",
        "lessons" : [{
            "description": "Make a budget",
            "thumbnail": "",
            "audio_file": "",
            "created": "2020-05-27 13:22:05.354824",
            "modified": "2020-05-27 13:22:05.354824",
            "order": 1,
            "module": 1
        }]
    }   
]
}
```

### Feedback 

#### Send Feedback

POST `v1\users\user\feedback\<user-id>/`

Request
```json
{
"comment" : "good app",
"rating" : 5
}
```

Response
```json
{
  "message" : "feedback saved"
}
```

### Data tracking 

#### Send Data

POST `/v1/analytics/data/create/`

Request
```json
{
"lesson"  : 2,
"data": {}
}
```

Response
```json
{
"message"  : "data saved"
}
```

### Question tracking

#### Send Question Data

POST `/v1/analytics/question/create/`

Request
```json
{
"lesson"  : 2,
"data": {
      "id" : 2,
      "lesson" : 2,
      "startTime" : "",
      "endTime" : "",
      "question_id" : 2,
      "local_id" : 2,
      "elapsed_time" : "",
      "buffered_position" : "",
      "duration" : "",
      "volume" : "",
      "eventType" : "",
      "finished" : "",
      "videoStartTime" : "",
      "videoEndTime" : ""
    } 
}
```

Response
```json
{
"message"  : "question data saved"
}
```

### Notifications

#### List notifications 

GET `v1\users\users\notifications\list\<user-id>/`

Response 
```json
[
    {
      "id": 8327,
      "message":{
        "token":"bk3RNwTe3H0:CI2k_HHwgIpoDKCIZvvDMExUdFQ3P1...",
        "data":{
          "title" : "Mario",
          "body" : "great match!",
          "message" : "Portugal VS Denmark"
        }
      }
    }
]
```

#### Receive notification

GET `v1\users\users\notifications\<user-id>/`

Response
```json
{
      "message":{
        "token":"bk3RNwTe3H0:CI2k_HHwgIpoDKCIZvvDMExUdFQ3P1...",
        "data":{
          "title" : "Mario",
          "body" : "great match!",
          "message" : "Portugal VS Denmark"
        }
      }
}
```
