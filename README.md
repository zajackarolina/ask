# Kraków Tourist Route Planner (Dockerized)

## Overview

This web application helps users plan their tourist routes in Kraków by selecting points of interest they want to visit. It utilizes a genetic algorithm to find a near-optimal order of visiting these locations, minimizing the total walking distance. The application leverages the Google Maps API to calculate distances and durations between selected locations and displays the route on an interactive map and a static map.

This version of the application is containerized using Docker, making it easier to set up and run consistently across different environments.

## Features

* **Selectable Points of Interest:** Users can choose from a list of popular landmarks in Kraków.
* **Optimized Route:** A genetic algorithm determines an efficient sequence for visiting the selected locations.
* **Distance and Time Estimation:** The application calculates the total walking distance and estimated travel time for the generated route using the Google Maps API.
* **Interactive Google Maps Display:** The optimized route is displayed on an interactive map, allowing users to explore the path.
* **Static Map Image:** A static image of the route with labeled markers for each point of interest is also provided.
* **Dockerized Application:** Easy setup and deployment using Docker.

## Technologies Used

* **Python:** The backend logic and Flask web framework.
* **Flask:** A micro web framework for Python.
* **Genetic Algorithm:** An optimization algorithm implemented to find the best route.
* **Google Maps API:** Used for calculating distances, durations, and displaying maps.
* **dotenv:** For managing environment variables (API key).
* **CSV:** Used to store and load the list of points of interest and their coordinates.
* **HTML/CSS:** For the user interface.
* **Jinja:** Templating engine for rendering HTML.
* **Docker:** For containerization.

## Prerequisites

* **Docker:** Ensure you have Docker installed on your system. You can find installation instructions for your operating system on the [official Docker website](https://docs.docker.com/get-docker/).
* **Google Maps API Key:** You will need a Google Maps API key with the Directions API and Maps Static API enabled.

## Setup and Installation (using Docker)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/zajackarolina/ask
    cd ask
    ```

2.  **Set up environment variables:**
    * Create a `.env` file in the root directory of the project.
    * Add your Google Maps API key to the `.env` file:
        ```
        GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_MAPS_API_KEY
        ```
        *(Ensure you have enabled the Directions API and Maps Static API in your Google Cloud Console.)*

3.  **Build the Docker image:**
    ```bash
    docker-compose build flask-app
    ```
    This command Builds the Docker image for the `flask-app` service based on the `Dockerfile-flask`.

4.  **Run the Docker container:**
    ```bash
    docker-compose up flask-app -d
    ```
    Creates and starts the container(s) for the `flask-app` service. The `-d` flag runs the container in detached mode (in the background).

5.  **Access the application:**
    Open your web browser and navigate to `http://localhost:5000`.

## Data Source

The list of points of interest and their coordinates are stored in the `models/data.csv` file. The CSV file should have the following columns:

```csv
name,lat,lng
```
### Docker
- `docker compose build` - build docker (image)
- `docker compose build --no-cache` - build docker from 0
- `docker compose up` - create and start container
- `docker compose down` - stop and remove container