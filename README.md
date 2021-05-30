# 🤑 Scraping By

A Django app that lets us know when our favourite products are on special at a
certain major supermarket chain

## Running the app locally

Requires [Poetry](https://python-poetry.org/) and Python 3.9.5.

1. Install dependencies with `poetry install`
1. Copy the example environment variables `cp example.env .env`
1. Edit the `.env` file you just created to add values for `API_URL` (necessary), and
   `SLACK_URL` (optional).
1. Create a superuser for yourself: `poetry run src/manage.py createsuperuser`
1. Run the local web server `poetry run src/manage.py runserver`
1. Visit `http://127.0.0.1/admin` and log in with the superuser credentials you just
   created.

## Adding products in the admin interface

Click on `Products`, then click the `Add Product` button at the top right. You
only need to enter the product ID (the number from the supermarket URL) - the
app will pick up the rest when it next scrapes the site.

## Management commands

Scrape the site:

```
$ poetry run src/manage.py scrape
```

Post specials to Slack:

```
$ poetry run src/manage.py post_to_slack
```

## Deploying to Heroku

Heroku doesn't know about Poetry, so if you add/update dependencies, you need to export
a `requirements.txt` file.

```
$ poetry export -f requirements.txt --output requirements.txt
```
