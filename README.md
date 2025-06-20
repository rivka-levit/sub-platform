# 📰 Subscription Platform

### Overview

This is a Django-based subscription platform that allows two types of users — 
writers and clients — to register and interact within the system. Writers 
can create and publish articles, while clients can subscribe to different 
plans to access those articles.

The platform supports standard and premium subscription tiers, offering 
varying levels of access to content. It is designed for scalability and ease 
of deployment using Docker.

### 🚀 Features

- 🔐 User Registration & Authentication
    - Separate registration flow for writers and clients
    - Login/logout functionality

- ✍️ Writer Dashboard
    - Create, edit, and delete articles
    - View own published content

- 📖 Client Features
    - Subscribe to standard or premium plans - 
    - View articles based on subscription level

- 📦 Subscription Management
    - Access control to articles depending on plan
    - Easily extendable for payment integration

- 🐳 Dockerized Deployment

### 🏗️ Tech Stack

- Backend: Django 4.x
- Database: PostgreSQL (via Docker)
- Authentication: Custom model based on Django built-in auth system
- Containerization: Docker & Docker Compose

### 🐳 Getting Started with Docker

1. Clone the Repository
    ```
    git clone https://github.com/rivka-levit/sub-platform.git
    cd sub-platform
   ```
   
2. Configure Environment
    ```
    cp .env.example .env
   ```
    
    Copy .env.example to .env and configure settings like database 
    credentials, Django secret key, etc.


3. Build and Run the Containers
    The app will be available at: http://localhost:8000
    ```
    docker-compose up --build
   ```

### 🧪 Running Tests

```
docker compose run --rm app sh -c "pytest"
```

### 💡 Subscription Plans

| Plan       | Access Level           |
|------------|------------------------|
| Standard   | Limited article access |
| Premium    | Full article access    |

Access logic is enforced in views and templates based on the client's current 
subscription status.

### 🔐 Authentication

- Users can register as either writer or client.
- The role determines the dashboard and available features.
- Permissions and access control are managed via Django’s CustomUser model and custom decorators/mixins.

### 🙌 Acknowledgments

This project was built as a learning exercise to deepen understanding of Django, user role management, and Dockerized 
development workflows.
