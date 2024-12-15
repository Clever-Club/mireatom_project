FROM node:21 AS build

RUN mkdir -p /app
WORKDIR /app
COPY package.json package-lock.json ./

RUN npm ci --cache .npm --prefer-offline

COPY . /app
RUN npm run build

FROM nginx:stable-alpine AS final

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
