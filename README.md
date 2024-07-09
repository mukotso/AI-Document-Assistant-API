# AI DOCUMENT ASSISTANT  API

This repository ( AI DOCUMENT ASSISTAN) contains a Django project set up with Docker, using MySQL as the database and Adminer for database management.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/mukotso/AI-Document-Assistant-API.git
    cd AI-Document-Assistant-API
    ```

2. **Build Docker Containers:**

    ```sh
    docker-compose build
    ```

3. **Create Django Project (if not already created):**

    ```sh
    docker-compose run web django-admin startproject src .
    ```

4. **Update Django Settings:**

   Modify `src/settings.py` to configure MySQL:

    ```python
    # src/settings.py

    import os

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DATABASE_NAME'),
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
            'HOST': os.environ.get('DATABASE_HOST'),
            'PORT': os.environ.get('DATABASE_PORT'),
        }
    }
    ```

5. **Start Docker Containers:**

    ```sh
    docker-compose up
    ```

6. **Apply Migrations and Create Superuser:**

    ```sh
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

### Access

- **Django Application:** `http://localhost:8022`
- **Adminer:** `http://localhost:8021`

Adminer allows you to manage the MySQL database via a web interface.

### Docker Configuration

- **Dockerfile:** Configures the Python environment and installs dependencies.
- **docker-compose.yml:** Defines the services for Django, MySQL, and Adminer.

### Troubleshooting

- **Build Errors:** Ensure all required system packages are installed in the Dockerfile.
- **Database Connection Issues:** Verify that the MySQL container is running and environment variables are correctly set.

### Contributing

Feel free to fork the repository and submit pull requests. For significant changes, please open an issue first to discuss the proposed changes.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
