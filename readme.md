# FBK DevOps

## Deploy

Generate `nginx` configuration (if `historian` port was changed):
```shell
scripts/generate_configs.py nginx
```

Run all services:
```shell
docker-compose up postgres historian nginx
```

## Try out

POST your entry (use appropriate `nginx` port):
```shell
curl -X POST -H "Content-Type: application/json" \
  -d '{"data": "My great entry"}' \
  http://localhost:8080/entries/ | jq
```

## Test

Run the following to test the `historian`:
```shell
docker-compose up -d postgres historian
docker-compose run test-historian

# Don't forget to stop the containers running in the background
docker-compose down
```
