# Swagger API

Run swagger on linux/macos

```sh
docker run -e SWAGGER_JSON=/foo/swagger.yaml -v "$(pwd)":/foo -p 8080:8080 swaggerapi/swagger-ui
```

Run swagger on windows with bash

```bash
MSYS_NO_PATHCONV=1 docker run -e SWAGGER_JSON=/foo/swagger.yaml -v "$(pwd)":/foo -p 8080:8080 swaggerapi/swagger-ui
```
