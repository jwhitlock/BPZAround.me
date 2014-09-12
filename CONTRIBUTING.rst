============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/codefortulsa/BPZAround.me/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

BPZAround.me could always use more documentation, whether as part of the
official BPZAround.me docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/codefortulsa/BPZAround.me/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

.. _get-started:

Get Started!
------------

Ready to contribute? Here's how to set up `BPZAround.me` for local development.

#. `Fork BPZAround.me`_ on GitHub.

#. `Clone`_ your fork locally::

    git clone git@github.com:your_name_here/BPZAround.me.git

#. Install requirements into a `virtualenv`_. This is easiest with
   `virtualenvwrapper`_::

    mkvirtualenv BPZAround.me
    cd BPZAround.me/
    pip install -r requirements.txt -r requirements.dev.txt

#. `Install PostGIS for GeoDjango`_.

#. Create a ``bpzaroundme`` PostGIS spatial database per the
   `Post-installation`_ instructions for your version of Postgres & PostGIS.::

#. Setup your local environment (Note: you can automate this with `autoenv`_)::

    source .env

#. Make sure tests work::

   $ ./manage.py test

#. Run it!::

   $ ./manage.py runserver

.. _`Fork BPZAround.me`: https://github.com/codefortulsa/BPZAround.me/fork
.. _Clone: http://git-scm.com/book/en/Git-Basics-Getting-a-Git-Repository#Cloning-an-Existing-Repository
.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation
.. _autoenv: https://github.com/kennethreitz/autoenv
.. _`Install PostGIS for GeoDjango`:
    https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis
.. _`Post-installation`: https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/#post-installation

Run on Heroku
-------------
Heroku will allow you to run BPZAround.me for free or cheaply.  However, the
free database plans currently do not support PostGIS, so there's more work to
do (and possible an expense) to get a working database.  Two options are given:
running a production Heroku database, or running an AWS RDS instance.

It assumes you've forked the repo and have cloned the fork locally.  See
`Getting Started with Python on Heroku`_ for friendly instructions.  It also
assumes you have the PostgreSQL command line tool `psql` installed.

#. `Install Heroku Toolbelt`_.

#. In the project directory, create the heroku app::

   $ heroku create

#. (Database option #1) Upgrade to `production PostgreSQL`_ for PostGIS::

   $ heroku addons:add pgbackups
   $ heroku addons:add heroku-postgresql:standard-0
   $ heroku pg:wait
   $ heroku maintenance:on
   $ heroku pg:info  # Get color name of old Hobby-dev and new Standard 0 databases
   $ heroku pg:promote HEROKU_POSTGRESQL_[NEW_COLOR]
   $ heroku maintenance:off
   $ heroku pg:psql -c "CREATE EXTENSION IF NOT EXISTS postgis"

#. (Database option #2) Add a AWS RDS database:

   You can sign up for AWS, give them your credit card, and then spin up a
   PostgreSQL database for free (in the first year) or cheap.  Create a public
   RDS server, and then update your security group to allow any IP to reach
   port 5432.

   If you have these RDS parameters:

   * DB Name: bpzaroundme
   * Username: bpzuser
   * Password: password
   * Endpoint: endpoint.rand0string.us-west-2.rds.amazonaws.com:5432

   Then use this to setup the database::

       $ POSTGRES_PLZ=1 DATABASE_URL="postgres://bpzuser@endpoint.rand0string.us-west-2.rds.amazonaws.com:5432/bpzaroundme" ./manage.py dbshell
       Password for user bpzuser:
       psql (9.3.5, server 9.3.3)
       SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)
       Type "help" for help.

       bpzaroundme=> CREATE EXTENSION postgis;
       CREATE EXTENSION
       bpzaroundme=> CREATE EXTENSION postgis_topology;
       CREATE EXTENSION
       bpzaroundme=> \q

   Drop the `POSTGRES_PLZ=1` to verify that the PostGIS extension was installed::

       $ DATABASE_URL="postgis://bpzuser@endpoint.rand0string.us-west-2.rds.amazonaws.com:5432/bpzaroundme" ./manage.py dbshell
       Password for user bpzuser:
       psql (9.3.5, server 9.3.3)
       SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)
       Type "help" for help.

       bpzaroundme=> SELECT PostGIS_Version();
                   postgis_version
       ---------------------------------------
       2.1 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
       (1 row)

       bpzaroundme=> \q

   Set the connection in heroku (be sure to add the password)::

       $ heroku config:set DATABASE_URL="postgis://bpzuser:password@endpoint.rand0string.us-west-2.rds.amazonaws.com:5432/bpzaroundme"

#. Configure the environment::

   $ heroku config:set BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
   $ heroku config:set DJANGO_DEBUG=1   # Alternatively, set ALLOWED_HOSTS

#. Deploy the code::

   $ git push heroku master  # Deploy current master, or
   $ git push heroku my_aweseome_branch:master  # Deploy a difference branch

#. Open app in browser::

   $ heroku open

#. Setup the database::

   $ heroku run ./manage.py syncdb  # Also setup your superuser account
   $ heroku run ./manage.py migrate

#. Load Tulsa data::

   $ heroku run ./manage.py load_cases data/boa-cases.json
   $ heroku run ./manage.py load_cases data/tmapc-cases.json
   $ heroku run ./manage.py load_home_owners_associations data/home-owners-associations.json

If you want to use your own domain, then see the Heroku article on `Custom Domains`_.

.. _`Install Heroku Toolbelt`: https://toolbelt.heroku.com
.. _`Getting Started with Python on Heroku`: https://devcenter.heroku.com/articles/getting-started-with-python#introduction
.. _`production PostgreSQL`: https://devcenter.heroku.com/articles/heroku-postgres-plans
.. _`Custom Domains`: https://devcenter.heroku.com/articles/custom-domains

Make Changes
------------
1. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

2. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ make qa-all

3. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

4. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, 3.3, and 3.4, and for PyPy. Check
   https://travis-ci.org/codefortulsa/BPZAround.me/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ python -m unittest tests.test_BPZAround.me
