COMPOSE = docker compose

# Build images
build:
	$(COMPOSE) build

# Start services in the background
up:
	$(COMPOSE) up --build -d

# Stop and remove containers, networks, and volumes
down:
	$(COMPOSE) down -v

# Clean up everything: stop containers and remove the output directory
clean: down
	rm -rf out && mkdir -p out

# Default command: clean and then start everything
all: clean up