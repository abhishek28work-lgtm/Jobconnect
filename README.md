# JobConnect — Full-Stack Job Portal

JobConnect is a web-based job portal built with Django that connects job seekers with employers. Employers can publish job openings and manage applications, while job seekers can explore opportunities and apply for suitable positions.

## Features

### Authentication and User Roles
- User registration and login
- Separate dashboards for job seekers and employers
- Job seeker and employer profiles

### Job Management
- Post, view, edit, and delete job listings
- Browse available jobs
- Search jobs by title or required skills
- Filter jobs by location and job type
- Paginated job listings

### Application Management
- Apply for jobs as a job seeker
- Prevent duplicate applications for the same job
- Allow employers to review applications
- Update application status to Pending, Accepted, or Rejected

### REST API
- Retrieve job listings and individual job details
- Create, update, and delete job listings
- Submit and retrieve job applications
- Manage application statuses
- Test API requests with Postman

## Technologies Used

- **Backend:** Python, Django
- **REST API:** Django REST Framework
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite
- **API Testing:** Postman
- **Version Control:** Git and GitHub

## Project Structure

```text
jobconnect/
├── accounts/
├── jobs/
├── applications/
├── templates/
├── jobconnect/
├── manage.py
├── db.sqlite3
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd jobconnect
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

Install the project's dependencies using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/jobs/api/jobs/` | Retrieve job listings |
| GET | `/jobs/api/jobs/<job_id>/` | Retrieve a job |
| POST | `/jobs/api/jobs/create/` | Create a job |
| PUT | `/jobs/api/jobs/<job_id>/update/` | Update a job |
| DELETE | `/jobs/api/jobs/<job_id>/delete/` | Delete a job |

Application endpoints are available under `/applications/`. Refer to the project's URL configuration for the exact routes.

**Note:** API access depends on authentication, permissions, and user role.

## Future Improvements

- Add automated tests for views and API endpoints
- Improve deployment and production configuration
- Add email notifications for application updates
- Introduce advanced job recommendations

## Author

**Abhishek Kumar**

- LinkedIn: https://linkedin.com/in/abhishek-kumar-4ba098356/
- GitHub: https://github.com/abhishek28work-lgtm

---

This project was developed to practice full-stack web development, Django, database operations, REST API development, and API testing.