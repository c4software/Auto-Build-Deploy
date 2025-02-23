# Auto Build Deploy

This project simplifies the automation of deploying an application via a webhook. The prupose is to automate the redeployment of a web application when a new commit is pushed to the repository.

The server listens for a POST request on a specified path. When the request is received, the server pulls the repository, builds a Docker image, and restarts the application to serve the new image for clients.

## Features

- Automated deployment triggering via a webhook
- Automatic repository update
- Docker image build on demand
- Nearly instantaneous redeployment (the new image is renamed at the last moment)

## Prerequisites

- Docker
- Docker Compose

## Installation & Configuration

1. Clone the repository:
   ```bash
   git clone https://github.com/c4software/Auto-Build-Deploy.git
   ```
2. Configure the environment variables in `docker-compose.yml`:
   - Modify `REPO_URL` to point to your repository.
   - Set `RANDOM_PATH_FOR_WEBHOOK` to customize the webhook path.
3. Start the service:
   ```bash
   docker compose up
   ```

## Usage

The server listens on port 8888.  
To trigger deployment, send a POST request to:
```
http://localhost:8888/<RANDOM_PATH_FOR_WEBHOOK>
```
(Replace `<RANDOM_PATH_FOR_WEBHOOK>` with the configured value.)

For example, with curl you can use:

```bash
curl -X POST http://localhost:8888/<RANDOM_PATH_FOR_WEBHOOK>
```

## Deployment example

The deployment process consists of pulling the repository, building a Docker image, and redeploying the application.

To do that, the target repo must have a Dockerfile that builds the application. Here is an example of a Dockerfile:

```Dockerfile
# Build stage
FROM oven/bun:latest AS build
WORKDIR /app
COPY package*.json ./
RUN bun install
COPY . .
RUN apt update && apt install -y git
RUN bun run docs:build

# Production stage
FROM nginx:alpine
COPY --from=build /app/.vitepress/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

This Dockerfile is an example from another repo of mine ([see here](https://github.com/c4software/bts-sio)).

## Logs & Deployment

Deployment logs can be accessed using the command:

```bash
docker-compose logs
```

## Contributing

Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.