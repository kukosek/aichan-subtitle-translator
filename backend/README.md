# sub-translator/backend

Backend REST API made with the awesome python library cherrypy.

## Documentation of API

It has a rest endpoint /translate_sub, that accepts
POST requests with JSON request body (see data model)

### Request model

```ts
interface RequestModel {
	format: String = "ass"|"srt",
	src: String,
	src_lang: String,
	tgt_lang: String
}
```

### Response model

It has a property `data` that returns the same things you sent but translated.

```ts
interface ResponseModel {
	status: String = "success"|"fail"|"error",
	data: RequestModel
}
```

### Stats dashboard

It tracks requests and saves them into a postgres DB. You can view a 'dashboard' on
the endpoint /stats


## Build and run using docker

`docker build -t my-aichan-backend-release:latest .`
`docker run -p 9090:9090 my-aichan-backend-release`
Before the run command, specify the database related
environment variables, otherwise bad defaults
will be loaded from the .env file
