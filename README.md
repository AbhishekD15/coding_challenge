# SL-101: Manage Courses and Intakes with API Endpoint

## Title
Manage Courses and Intakes with API Endpoint

## Description
As an Admin user, I want to have the ability to create and manage courses and their associated intakes within the Django Admin interface, so that I can efficiently organize and update course offerings.

Additionally, I need an API endpoint that provides a list of all available courses along with their respective intakes, so that this data can be accessed programmatically for integration with other systems or for front-end display.

## Acceptance Criteria
- [x] A course has a unique `id` and a `name`
- [x] An intake has a unique `id`, a `start_date`, and an `end_date`
- [x] A course can have multiple intakes associated with it
- [x] Ability to create/manage courses within the Django Admin interface
- [x] Ability to create/manage intakes within the Django Admin interface
- [x] `/api/admissions/courses/` API endpoint that provides a list of all available courses along with their respective intakes
- [x] Access to this endpoint has to be authenticated using [DRF token](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
- [x] Unit tests to make sure the endpoint behaves as intended

## Getting Started

### Prerequisites
- Python 3.12
- Pipenv
- Docker (optional)

### Installation

#### With Docker
1. Install Docker: https://docs.docker.com/engine/install/
2. Install Docker Compose: https://docs.docker.com/compose/install/
3. Build and run the Docker Compose services:
   ```bash
   docker-compose up --build
   ```
4. Run unit tests:
   ```bash
   docker-compose run --rm django pytest
   ```

#### Without Docker
1. Install Pipenv: https://pipenv.pypa.io/en/latest/installation.html
2. Install dependencies:
   ```bash
   pipenv install --deploy --dev
   ```
3. Run the application:
   ```bash
   pipenv run ./manage.py runserver 0.0.0.0:8000
   ```
4. Run unit tests:
   ```bash
   pipenv run pytest
   ```

### API Documentation
The API documentation is available at the following endpoints:
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **Redoc UI**: `http://localhost:8000/api/schema/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### Project Structure
- `apps/admission/`: Define the models and the associated Django admins.
- `apps/api/`: Define the DRF views, serializers, and relevant unit tests.
- `config/`: Project settings and URL configuration.

### Authentication
The API uses JWT for authentication. Obtain a token by making a POST request to `/api/token/` with your credentials. Use the token in the `Authorization` header for subsequent requests.



## Enhancements
If you have any ideas for enhancing your implementation but don't have the time or aren't sure how to achieve them in Django, don't worry. You're encouraged to note them as comments in the code or in a separate document.

These are my ideas:

- [ ] Add more detailed validation for course and intake fields, maybe checking for overlapping intake dates within the same course.
- [ ] Improve error handling and add custom error messages to provide more informative feedback to API consumers.
- [ ] Set up continuous integration (CI) for automated testing and deployment to ensure code quality and streamline the development process.
- [ ] Implement rate limiting to prevent abuse of the API endpoints.
- [ ] Add caching mechanisms to improve the performance of frequently accessed endpoints.
- [ ] Implement different user roles (e.g., Admin, Instructor, Student) with specific permissions for managing courses and intakes.
- [ ] Implement some sort of bulk update functionality for courses and intakes to allow batch processing of records.

## Submission
To submit your solution, push your code to a GitHub repository and share the link.

---

Feel free to customize this README to better fit your project and any additional details you want to include.