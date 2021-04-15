# Subtitle translator

A site that takes your subtitle files and translates them.
Supports English and some European languages. Can
be used to translate english anime subtitles into your language.

## Aren't the results shit?

No, the backend uses a [pretty good translating engine](https://lindat.mff.cuni.cz/services/translation/)
made at the Czech Matfyz. The results are much better than from
google translate. But surely it isn't perfect.

## Running it

### Option 1: Running it using docker compose

1. Install docker
2. Install docker-compose
3. See frontend/ and backend/ . Build each of them using `docker build`.
Remember the release names.
4. Change the image names in `docker-compose.yml` to your release names.
5. Change the ports if you want.
6. Run it -  `docker-compose up`. If you want to run it in background,
add the arg `-d`.

### Option 2: The old ways

You can of course install postgres and things right into your
system and run the backend, then build the frontend into static pages
and feed that into your web server.

### Option 999: Deploying to kubernetes

I myself deployed it to kubernetes.
If you wanna do that too, take
a look at deployment.yaml and edit it to your needs.
Also, you must build the docker images and push it to a docker
registry of choice.
The secrets
in the deployment file are base 64 encoded. You must write there the DB
adress, name, password etc in base64.

To deploy postgres to kubernetes, I've used the [postgres operator](https://access.crunchydata.com/documentation/postgres-operator/latest/architecture/provisioning/)
But you can do it without it.

Then I've applied the ingress config file, so my ingress controller
will proxy the domain hosts to the services.
