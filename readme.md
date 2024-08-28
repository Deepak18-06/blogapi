# Blogs

## Setup and Installation

1. Clone repository

2. Install Dependancies
``
pip install -r requirements.txt
``

3. Install mongodb using this https://www.mongodb.com/docs/manual/installation/

4. Run the app
``
uvicorn main:app --reload
``



## To test  API endpoints using curl 

Below are the curl commands for testing each endpoint.

1. Register a New User (/api/register)

```bash

curl -X POST "http://127.0.0.1:8000/api/register" \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "password123"}'
```

2. Login and Obtain a JWT Token (/api/login)

```bash

curl -X POST "http://127.0.0.1:8000/api/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=testuser&password=password123"
```

The response will include an access_token. Note the token, as you will use it for authorization in subsequent requests.

3. Retrieve All Blog Posts (/api/blogs)

```bash

curl -X GET "http://127.0.0.1:8000/api/blogs" \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Replace YOUR_JWT_TOKEN with the actual token obtained from the login step.


4. Retrieve a Specific Blog Post (/api/blogs/{id})

   ```bash

      curl -X GET "http://127.0.0.1:8000/api/blogs/ID" \
      -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

Replace ID with the specific blog post ID and YOUR_JWT_TOKEN with the JWT token.


5. Create a New Blog Post (/api/blogs)

```bash

curl -X POST "http://127.0.0.1:8000/api/blogs" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{"title": "New Blog Post", "content": "This is the content of the blog post."}'
```

6. Update an Existing Blog Post (/api/blogs/{id})

```bash

curl -X PUT "http://127.0.0.1:8000/api/blogs/ID" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{"title": "Updated Blog Post Title", "content": "Updated content of the blog post."}'
```

Replace ID with the blog post ID and YOUR_JWT_TOKEN with the JWT token.


7. Delete a Blog Post (/api/blogs/{id})

```bash

curl -X DELETE "http://127.0.0.1:8000/api/blogs/ID" \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```
Replace ID with the specific blog post ID and YOUR_JWT_TOKEN with the JWT token.

Notes:
Testing Order: Start by registering a user and logging in to get the JWT token. Then, use the token to test the CRUD operations on blog posts.
