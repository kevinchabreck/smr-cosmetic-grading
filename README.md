## Getting started

Download and install **[Docker for Mac or Windows](https://www.docker.com/products/overview)**.

### Run a local instance of the Cosmetic Grading service

Run in this directory:

    $ docker-compose up

_note: the first time you run `docker-compose up` the web service may start up before the postgres service due to some database initialization steps that need to occur. If this happens, just bring the compose stack down (`docker-compose down`) and bring it back up again (`docker-compose up`) - the services should start in the correct order on subsequent runs._  

Once the service has successfully started up, you should see this message (or something similar):

    web_1       | You have 16 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, grading, sessions.
    web_1       | Run 'python manage.py migrate' to apply them.
    web_1       | February 16, 2018 - 19:15:19
    web_1       | Django version 2.0.2, using settings 'smrsite.settings'
    web_1       | Starting development server at http://0.0.0.0:8000/
    web_1       | Quit the server with CONTROL-C.

Apply the migrations in the running container with the following command:

    $ docker-compose exec web python3 manage.py migrate

Next, create a user who can login to the admin site:

    $ docker-compose exec web python3 manage.py createsuperuser

Login to the admin site with your new superuser at [http://localhost:8000/admin](http://localhost:8000/admin) and create a few Tests, Questions, and Choices.

Finally, navigate to [http://localhost:8000/grading](http://localhost:8000/grading) to demo the Cosmestic Grading service.

Optional: run the tests:

    $ docker-compose exec web python3 manage.py test grading
