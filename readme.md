This project is a lite management web service, based on Django, mysql and redis.

## Get the project

This project is dockerised and is ready to be deployed on a Ubuntu server.

The following instruction is based on **Ubuntu 18**

Step 1: update apt:

```
sudo apt-get update
```

Step 2: install required packages and Docker ce.

```
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common apt-utils docker-ce -y
```

Step 3: download docker-compose

```
sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

Step 4: give permission to docker-compose

```
sudo chmod +x /usr/local/bin/docker-compose
```

Step 5: pull this project:

You can find a released build >>here<<

Step 6: Unzip the file

```
```

Step 7: build

```
cd saas_project_compose/
sudo docker-compose build
```

Step 8:

```
sudo docker-compose up
```

