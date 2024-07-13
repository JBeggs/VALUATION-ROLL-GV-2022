# django-webcrawler

# H1 VALUATION ROLL GV 2022

#h3

built with :

1. docker
2. docker compose
3. django (admin panel)
4. django rest framework (API access)
5. drf-yasg (documentation and schema)
6. selenium (webcrawler)
7. beautifulsoup4 (webcrawler)


# h3 Installation

Before we can get started make sure you have [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) installed


# h3 Step 1

checkout the repository at : [VALUATION-ROLL-GV-2022](https://github.com/JBeggs/VALUATION-ROLL-GV-2022)

`git clone https://github.com/JBeggs/VALUATION-ROLL-GV-2022.git`

cd insto the folder and run 

`cd VALUATION-ROLL-GV-2022`
`docker build .`

then

`docker compose up -d --build`


But I think the mostly do the same thing

# h3 Step 2

We need to migrate so use this command:

`docker exec -it valuation-roll-gv-2022-web-1 bash`

To get into a bash window

then run:

`python manage.py migrate`
`python manage.py createsuperuser`

To create the super user...

And that's it.

# H3 Url for application

[Django Admin](http://127.0.0.1:8000/admin/)
[Swagger Docs](http://127.0.0.1:8000/swagger/)
[REST API](http://127.0.0.1:8000/)

# H3 Useful docker and docker compose commands

Stop the docker containers

`docker compose down`

# H3 Container names


valuation-roll-gv-2022-chrome-1
valuation-roll-gv-2022-framework-1
valuation-roll-gv-2022-cronjobs-1
valuation-roll-gv-2022-db-1
valuation-roll-gv-2022-web-1