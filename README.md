**SL-101**

**Title:** Manage Courses and Intakes with API Endpoint

**Description:**

As an Admin user,
I want to have the ability to create and manage courses and their associated intakes within the Django Admin interface,
so that I can efficiently organize and update course offerings.

Additionally, I need an API endpoint that provides a list of all available courses along with their respective intakes,
so that this data can be accessed programmatically for integration with other systems or for front-end display.

**Acceptance Criteria:**

- [ ] A course has a unique `id` and a `name`
- [ ] An intake has a unique `id`, a `start_date`, and an `end_date`
- [ ] A course can have multiple intakes associated with it
- [ ] Ability to create/manage courses within the Django Admin interface
- [ ] Ability to create/manage intakes within the Django Admin interface
- [ ] `/api/admissions/courses/` API endpoint that provides a list of all available courses along with their respective intakes
- [ ] Access to this endpoint has to be authenticated using [DRF token](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
- [ ] Unit tests to make sure the endpoint behaves as intended

If you have any ideas for enhancing your implementation but don't have the time or aren't sure how to achieve them in Django, don't worry.
You're encouraged to note them as comments in the code or in a separate document.

**Getting Started**

Please use the boilerplate code provided as a starting point. The code has 3 parts:
- `apps/admission/` - this is where you'll define the models and the associated Django admins
- `apps/api/` - this is where you'll define the DRF view, serializers, and relevant unit tests
- `config/` - this is where you'll find the project's settings and URL conf

**With Docker**

- Install docker https://docs.docker.com/engine/install/
- Install docker compose https://docs.docker.com/compose/install/
- Build docker image and start the container:
```shell
docker compose up
```
- Run unit tests:
```shell
docker compose run --rm django pytest
```

**Without Docker**

- Install pipenv https://pipenv.pypa.io/en/latest/installation.html
- Install dependencies:
```shell
pipenv install --deploy --dev
```
- Run the application:
```shell
pipenv run ./manage.py runserver 0.0.0.0:8000
```
- Run unit tests:
```shell
pipenv run pytest
```
