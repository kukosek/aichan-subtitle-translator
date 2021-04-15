# sub-translator/frontend

Nuxt.js + Typescript project.

## Build nginx container using docker

`docker build -t my-aichan-release:latest . --build-arg api_endpoint="http://localhost:8080/"`
API endpoint variable is optional. Default is [https://dulik.net/aichan/api/translate_sub](https://rolld.ml/WXul3cy5B)
`docker run -p 8080:80 my-aichan-release:latest` will run the container and expose Nginx on
local port 8080

## Build Setup without docker

Install nodejs and npm

```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch node.js server
$ npm run build
$ npm run start

# generate static project to be served by your http server
$ npm run generate
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).
