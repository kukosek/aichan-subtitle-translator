FROM node:15.14.0-alpine3.10 as NODE

WORKDIR /nuxt-app/
COPY package*.json ./
RUN npm install
COPY . ./

ARG api_endpoint="https://dulik.net/aichan/api/translate_sub"

ENV API_ENDPOINT=$api_endpoint

RUN npm run generate

FROM nginx:alpine
RUN mkdir /usr/share/nginx/html/aichan/
COPY --from=NODE /nuxt-app/dist/ /usr/share/nginx/html/aichan
EXPOSE 80
