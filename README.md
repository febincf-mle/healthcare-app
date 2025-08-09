# For development
export DJANGO_SETTINGS_MODULE=config.settings.dev

# For production
export DJANGO_SETTINGS_MODULE=config.settings.prod

# Docker build image
docker build -t health-care-app-image .

# Docker run container
docker run -d --name health-care-app-container -p 8000:8000 health-care-app-image