# Django API Project

This project is a Django-based API service. 


### Prerequisites

- Python 3.8+
- pip (Python package installer)
- virtualenv (recommended)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Mohamed-code-marvel/django-api.git
   cd django-api

### Create and activate a virtual environment:
- virtualenv venv
- source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

### Install the dependencies:
 - pip install -r requirements.txt

### Apply migrations:
 - python manage.py makemigrations
 - python manage.py migrate

### Run the development server:
 - python manage.py runserver

### Usage
 - Once the server is running, you can access the API at http://127.0.0.1:8000/. 
 - You can also access the Django admin interface at http://127.0.0.1:8000/admin/ using the superuser credentials you created.

## API Endpoints
 ## POST: User Registration
 - 127.0.0.1:8000/api/register/
   - 
 ## POST User Login
 - 127.0.0.1:8000/api/login/

 ## GET List Posts
 - 127.0.0.1:8000/api/posts/

 ## POST Create Post
 - 127.0.0.1:8000/api/posts/

 ## PUT Update Post
 - 127.0.0.1:8000/api/posts/<post_id>/

 ## GET Get Post Details
 - 127.0.0.1:8000/api/posts/<post_id>/

 ## DELETE Delete Post
 - 127.0.0.1:8000/api/posts/<post_id>/

 ## POST Create Comment
 - 127.0.0.1:8000/api/comments/

 ## PUT Update Comment
 - 127.0.0.1:8000/api/comments/<comment_id>/

 ## GET Get Comment Details
 - 127.0.0.1:8000/api/comments/<comment_id>/

 ## DELETE Delete Comment
 - 127.0.0.1:8000/api/comments/<comment_id>/