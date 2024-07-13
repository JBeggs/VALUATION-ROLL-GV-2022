# django-webcrawler

#H1 VALUATION ROLL GV 2022

#h3

built with :

1. docker
2. docker compose
3. django (admin panel)
4. django rest framework (API access)
5. drf-yasg (documentation and schema)
6. selenium (webcrawler)
7. beautifulsoup4 (webcrawler)


#h3 Installation

Before we can get started make sure you have [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) installed

checkout the repository at : [test](link)

cd insto the folder and run 

docker build .
docker compose up -d --build
docker compose down



--platform="linux/amd64" 

docker run --platform="linux/amd64"  -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest