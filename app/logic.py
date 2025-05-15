import googlemaps
import numpy as np
import random
import matplotlib.pyplot as plt
import csv
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

distance_matrix = []

def load_coords_from_csv(filename):
    coords = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            coords.append((float(row['lat']), float(row['lng'])))
    return coords

def load_places_from_csv(filename):
    places = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            places.append(row['name'])
    return places

filename = r'./models/data.csv'

places = load_places_from_csv(filename)
coords = load_coords_from_csv(filename)




def create_distance_matrix(coords, api_key):
    gmaps = googlemaps.Client(key=api_key)
    n = len(coords)
    distance_matrix_km = [[0] * n for _ in range(n)]
    duration_matrix_min = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                try:
                    result = gmaps.distance_matrix(
                        origins=[coords[i]],
                        destinations=[coords[j]],
                        mode='walking'
                    )
                    element = result['rows'][0]['elements'][0]
                    distance_km = element['distance']['value'] / 1000
                    duration_min = element['duration']['value'] / 60

                    distance_matrix_km[i][j] = distance_km
                    duration_matrix_min[i][j] = duration_min
                except Exception as e:
                    print(f"Błąd między {i} a {j}: {e}")
                    distance_matrix_km[i][j] = float('inf')
                    duration_matrix_min[i][j] = float('inf')

    return distance_matrix_km, duration_matrix_min


distance_matrix, duration_matrix_min = create_distance_matrix(coords, api_key)

def initialize_path(size, n_cities):
    population = []
    for _ in range(size):
        path = list(range(n_cities))
        random.shuffle(path)
        population.append(path)
    return population

# Długość trasy
def total_distance(path):
    distance = 0
    for i in range(len(path)):
        from_idx = path[i]
        to_idx = path[(i+1) % len(path)]  
        distance += distance_matrix[from_idx][to_idx] 
    return distance
    
# Selekcja ruletki
def roulette(population, distance):
    fitnesses = [1/d for d in distance]
    total = sum(fitnesses)
    pick = random.uniform(0, total)
    current = 0
    for i, fitness in enumerate(fitnesses):
        current += fitness
        if current >= pick:
            return population[i]

# Selekcja rankingowa
def ranking(population, distance):
    ranked_population = sorted(zip(distance, population), key=lambda x: x[0])
    ranks = [len(population) - i for i in range(len(population))]
    total_ranks = sum(ranks)
    pick = random.uniform(0, total_ranks)
    current = 0
    for i, (_, p) in enumerate(ranked_population):
        current += ranks[i]
        if current >= pick:
            return p

# Krzyżowanie
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end + 1] = parent1[start:end + 1]

    current_pos = 0
    for city in parent2:
        if city not in child:
            while child[current_pos] != -1:
                current_pos += 1
            child[current_pos] = city

    return child

# Mutacja
def mutate(path, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]

# Algorytm genetyczny z elitarnymi osobnikami
def genetic_algorithm(n_cities, mutation_rate, crossover_rate, population_size, generations, selection_method, elite_size=0.1):
    population = initialize_path(population_size, n_cities)
    best_history = []
    avg=[]
    max_history=[]
    for gen in range(generations):
        distances = [total_distance(p) for p in population]
        best = min(distances)
        best_history.append(best)
        avg.append(np.mean(distances))
        max_history.append(max(distances))
        sorted_population = [x for _, x in sorted(zip(distances, population))]
        #print(f" Pokolenie {gen} ")
        #for i, path in enumerate(population):
         #   print(f"Osobnik {i}: {[places[i] for i in path]}")

        elite_count = int(elite_size * population_size)
        elite_population = sorted_population[:elite_count]
        new_population = elite_population[:]  # Zachowujemy elite

        select = ranking if selection_method == "ranking" else roulette

        while len(new_population) < population_size:
            p1 = select(population, distances)
            p2 = select(population, distances)

            if random.random() < crossover_rate:
                child = crossover(p1, p2)
            else:
                child = p1[:]

            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
    
    final_distances = [total_distance(p) for p in population]
    best_index = final_distances.index(min(final_distances))
    best_path = population[best_index]
    
    return best_path, best_history, avg, max_history


def calculate_total_distance_and_time(path, distance_matrix, duration_matrix):
    total_km = 0
    total_minutes = 0
    for i in range(len(path)):
        from_idx = path[i]
        to_idx = path[(i + 1) % len(path)]  # zamknięta pętla
        total_km += distance_matrix[from_idx][to_idx]
        total_minutes += duration_matrix[from_idx][to_idx]
    return total_km, total_minutes

def format_duration(minutes):
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours} h {mins} min" if hours else f"{mins} min"



