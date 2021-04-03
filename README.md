## API Specification


##### Authentication

###### Login
Endpoint: auth/token/

Sample request
```text
Body:
"username": "<username>"
"password": "<password>"
```

Sample response
```text
{
"refresh":"<refresh token>",
"access":"<access token>",
"is_staff":false,
"first_name":"<first name>",
"last_name":"<last name>",
"user_id":"user id"
}
```
###### Refresh
Sample request
```text
Body:
"refresh": "<refresh code>"
```
Sample response
```text
{"access":"<access token>"}
```

##### Resource API

###### User
Endpoint: /api/user/

Fields
| Field            | Create           | Update           |
|------------------|------------------|------------------|
| user_id          | NO CHANGE        | NO CHANGE        |
| profile_pic      | Optional         | Optional         |
| username         | Required         | NO CHANGE        |
| password         | Required         | Optional         |
| email            | Required         | Optional         |
| first_name       | Optional         | Optional         |
| last_name        | Optional         | Optional         |
| is_staff         | Admin - Optional | Admin - Optional |
| is_superuser     | Admin - Optional | Admin - Optional |
| is_active        | Admin - Optional | Admin - Optional |
| date_joined      | NO CHANGE        | NO CHANGE        |
| groups           | Admin - Optional | Admin - Optional |
| user_permissions | Not used         | Not used         |


* Create user
    * Endpoint: /api/user/
    * Request method: POST
* List users
    * Endpoint: /api/user/
    * Request method: GET
* Retrieve user
    * Endpoint: /api/user/<user ID>
    * Request method: GET
* Update user
    * Endpoint: /api/user/<user ID>
    * Request method: PUT
* Delete user
    * Endpoint: /api/user/<user ID>
    * Request method: DELETE


###### Group
Endpoint: /api/group/

Fields
| Field            | Create           | Update           |        |
|------------------|------------------|------------------|--------|
| id               | NO CHANGE        | NO CHANGE        |        |
| name             | Admin - required | Admin - required | UNIQUE |



* Create group
    * Endpoint: /api/group/
    * Request method: POST
* List groups
    * Endpoint: /api/group/
    * Request method: GET
* Retrieve group
    * Endpoint: /api/group/<name>
    * Request method: GET
* Update group
    * Endpoint: /api/group/<name>
    * Request method: PUT
* Delete group
    * Endpoint: /api/group/<name>
    * Request method: DELETE

###### Post
Endpoint: /api/post/

Fields
| Field                | Create              | Update    |
|----------------------|---------------------|-----------|
| id                   | NO CHANGE           | NO CHANGE |
| title                | Required            | Required  |
| description          | Optional            | Optional  |
| body                 | Optional            | Optional  |
| video                | Optional            | Optional  |
| audio                | Optional            | Optional  |
| view                 | NO CHANGE           | NO CHANGE |
| is_public            | Optional Auto false | Optional  |
| like                 | NO CHANGE           | NO CHANGE |
| createdTimestamp     | NO CHANGE           | NO CHANGE |
| lastUpdatedTimestamp | NO CHANGE           | NO CHANGE |
| owner                | NO CHANGE           | NO CHANGE |
| category             | Optional            | Optional  |

* Create post
    * Endpoint: /api/post/
    * Request method: POST
* List posts
    * Endpoint: /api/post/
    * Request method: GET
* Retrieve post
    * Endpoint: /api/post/<id>
    * Request method: GET
* Update post
    * Endpoint: /api/post/<id>
    * Request method: PUT
* Delete post
    * Endpoint: /api/post/<id>
    * Request method: DELETE
* Parameters
    * author=<user_id> - contains
    * title=<title> - contains
    * category=<category_name> - match exactly
    * order_by=<any fields>
  
  
###### Category
Endpoint: /api/category/

Fields
| Field            | Create           | Update           |        |
|------------------|------------------|------------------|--------|
| name             | Admin - required | Admin - required | UNIQUE |
| created-by       | NO CHANGE        | NO CHANGE        |        |



* Create category
    * Endpoint: /api/category/
    * Request method: POST
* List categories
    * Endpoint: /api/category/
    * Request method: GET
* Retrieve category
    * Endpoint: /api/category/<name>
    * Request method: GET
* Update category
    * Endpoint: /api/category/<name>
    * Request method: PUT
* Delete category
    * Endpoint: /api/category/<name>
    * Request method: DELETE
* Parameters
    * parent=<parent category name> - get child categories by parent
    * parent=root - only root parents