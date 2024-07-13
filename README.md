# VALUATION ROLL GV 2022
---

### built with :

1. docker
2. docker compose
3. django (admin panel)
4. django rest framework (API access)
5. drf-yasg (documentation and schema)
6. selenium (webcrawler)
7. beautifulsoup4 (webcrawler)


# Installation
---

Before we can get started make sure you have [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) installed


### Step 1

checkout the repository at : [VALUATION-ROLL-GV-2022](https://github.com/JBeggs/VALUATION-ROLL-GV-2022)

`git clone https://github.com/JBeggs/VALUATION-ROLL-GV-2022.git`

cd insto the folder and run 

`cd VALUATION-ROLL-GV-2022`\
`docker build .`

then

`docker compose up -d --build`


But I think the mostly do the same thing

### Step 2

We need to migrate so use this command:

`docker exec -it valuation-roll-gv-2022-web-1 bash`

To get into a bash window

then run:

`python manage.py migrate`\
`python manage.py createsuperuser`

To create the super user...

And that's it.

# Urls for application
---

[Django Admin](http://127.0.0.1:8000/admin/)\
[Swagger Docs](http://127.0.0.1:8000/swagger/)\
[REST API](http://127.0.0.1:8000/)


# Useful docker and docker compose commands
---

Stop the docker containers

`docker compose down`

### Container names

`valuation-roll-gv-2022-chrome-1`\
`valuation-roll-gv-2022-framework-1`\
`valuation-roll-gv-2022-cronjobs-1`\
`valuation-roll-gv-2022-db-1`\
`valuation-roll-gv-2022-web-1`



# Strategy for webcrawler (NOT WORKING, hopefully by deadline)
---

I added a cronjob into the system that get's builtt with the application


> 0 * * * * root python manage.py get_full_title_deeds_town 0 100 > /dev/stdout\
> 20 * * * * root python manage.py get_full_title_suburb 0 100 > /dev/stdout\
> 40 * * * * root python manage.py sectional_title_scheme 0 100 > /dev/stdout


That run every hour for three scripts

`python manage.py get_full_title_deeds_town 0 100`\
`python manage.py get_full_title_suburb 0 100`\
`python manage.py sectional_title_scheme 0 100`

The scripts take two variables:

1. timeout for the requests, if they fail start with 1 and work up
2. the amount of suburbs, deeds towns or schemes to get at a time

With this rate 2400 x 3 (suburbs, deeds towns or schemes) will be collected in the first day

There is a basic que so that if anything happen's nothing happens...

---
---