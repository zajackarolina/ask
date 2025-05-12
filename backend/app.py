from flask import Flask, render_template, request, redirect, url_for
import csv
from logic import genetic_algorithm, load_coords_from_csv, total_distance, calculate_total_distance_and_time, create_distance_matrix

app = Flask(__name__)

# Funkcja wczytująca miejsca z CSV
def load_places_from_csv(filename):
    places = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            places.append(row['name'])
    return places

@app.route('/', methods=['GET'])
def index():
    # Wczytujemy listę zabytków z pliku CSV
    places = load_places_from_csv('data\data.csv')
    return render_template('index.html', places=places)

@app.route('/route', methods=['POST'])
def generate_route():
    selected_places = request.form.getlist('places')  # Pobieramy wybrane zabytki
    if not selected_places:
        return redirect(url_for('index'))  
    
    places = load_places_from_csv('data/data.csv')
    selected_indices = [places.index(place) for place in selected_places]
    
    best_path, best_history, avg, max_history = genetic_algorithm(
        n_cities=len(selected_places),
        mutation_rate=0.05,
        crossover_rate=0.98,
        population_size=50,
        generations=100,
        selection_method="roulette",  
        elite_size=0.1  
    )

    api=""

    coords = load_coords_from_csv('data\data.csv')
    distance_matrix, duration_matrix_min = create_distance_matrix(coords,api )

    route_length = total_distance(best_path)
    total_km, total_minutes = calculate_total_distance_and_time(best_path, distance_matrix, duration_matrix_min)

    # Generowanie URL do Google Maps
    ordered_path = "/".join([f"{coords[i][0]},{coords[i][1]}" for i in best_path + [best_path[0]]])
    base_url = "https://www.google.com/maps/dir/"
    url = base_url + ordered_path + "/data=!3m1!4b1!4m2!4m1!3e2"
    
    return render_template('result.html', best_path=best_path, places=places, url=url, route_length=route_length,     total_km=total_km,
    total_minutes=total_minutes
)

if __name__ == '__main__':
    print("Uruchamianie aplikacji Flask...")
    app.run(debug=True, port=5000)



