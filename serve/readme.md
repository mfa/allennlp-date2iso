# date2iso api

## about

Convert dates to iso8601 using FastAPI and AllenNLP

deployed:



## development

```
docker-compose up main
```

url is http://localhost:8021/


### run test-suite

```
docker-compose run --rm main pytest
```


## run on google cloud run

```
gcloud builds submit --config cloudbuild.yaml .
gcloud run deploy date2iso --image gcr.io/<PROJECT_ID>/date2iso --allow-unauthenticated --memory=1G
```
