# Django REST Test Template
This template adds testing to the [Django REST Auth template](https://github.com/NerdPlayground/django-rest-auth-template). To implement this template, head over to the base [Django REST template](https://github.com/NerdPlayground/django-rest-template) for the relevant steps and then the [Django REST Auth template](https://github.com/NerdPlayground/django-rest-auth-template) for additional steps. It adds the following;
- Packages;
    - Factory Boy - used to generate dummy data for your models
    - Coverage - used to measure the code coverage of your application

## Points to consider
- Update the `ProfileFactory` to include your Profile fields, you can use the [Factory Boy](https://factoryboy.readthedocs.io/en/stable/) and [Faker](https://faker.readthedocs.io/en/latest/) documentations to help you out with that
- Update the user registration related method in the `test` module of the `appauth` app
- Use the following command to get code coverage; `coverage run manage.py test && coverage report && coverage html`
    - `coverage run manage.py test` - runs the available tests and gathers data
    - `coverage report` - generates the results report in tabular form on the console
    - `coverage html` - generates a html representation of the results in html (`htmlcov/index.html`)
