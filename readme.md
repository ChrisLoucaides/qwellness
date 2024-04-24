# Q-Wellness

---

This is a repo for my final year project backend code. For the frontend see:
[https://github.com/ChrisLoucaides/qwellness-frontend](https://github.com/ChrisLoucaides/qwellness-frontend)

## Pre-requisites:
- A **code editor or IDE** (not required but recommended as it makes running the project locally far easier). For the development of this project I used PyCharm (for backend, however it can also run frontend projects) and WebStorm (for frontend)
  - **Recommendations**:
  - PyCharm (There is a paid and free version, can run both backend  and frontend apps)
  -  Visual Studio Code (Free, can run both backend  and frontend apps)
  - WebStorm (Paid version only, but there is a free trial, support for only frontend apps)

- **Installation of Node.js** and python 3.10 (If you use PyCharm a version of python will already come bundled with the IDE.
  - Node.js Installation Guide
  - Python Installation


## Getting Started with running locally

1. Install Requirements

```bash
pip install -r 'requirements.txt'
```

2. Make Database Migrations

```bash
python manage.py makemigrations
```

3. Migrate

```bash
python manage.py migrate
```

4. Run the development server
```bash
python manage.py runserver
```
