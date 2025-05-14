from flask import Flask, render_template, request, redirect, url_for
import csv
from logic import genetic_algorithm, load_coords_from_csv, total_distance, calculate_total_distance_and_time, create_distance_matrix, format_duration
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

app = Flask(__name__,
            static_folder="static",
            template_folder="templates")
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
    places = load_places_from_csv('./models/data.csv')
    return render_template('index.html', places=places)

@app.route('/route', methods=['POST'])
def generate_route():
    selected_places = request.form.getlist('places')  # Pobieramy wybrane zabytki
    if not selected_places:
        return redirect(url_for('index'))  
    
    places = load_places_from_csv('./models/data.csv')
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


    coords = load_coords_from_csv('./models/data.csv')
    distance_matrix, duration_matrix_min = create_distance_matrix(coords, api_key)

    total_km, total_minutes = calculate_total_distance_and_time(best_path, distance_matrix, duration_matrix_min)
    formatted_time = format_duration(total_minutes)

    # Generowanie URL do Google Maps
    ordered_path = "/".join([f"{coords[i][0]},{coords[i][1]}" for i in best_path + [best_path[0]]])
    base_url = "https://www.google.com/maps/dir/"
    url = base_url + ordered_path + "/data=!3m1!4b1!4m2!4m1!3e2"
    
    # Build Static Maps API URL with path and markers
    path = "color:0x0000ff|weight:5"
    marker_params = []

    for i, idx in enumerate(best_path):
        lat, lng = coords[idx]
        path += f"|{lat},{lng}"
        
        # Add marker label (A-Z)
        label = chr(65 + (i % 26))  # wraps around after Z
        marker_params.append(f"markers=label:{label}|{lat},{lng}")

    # Construct the full URL
    marker_str = "&".join(marker_params)
    static_map_url = (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"size=600x400&scale=2&{marker_str}&path={path}&key={api_key}"
    )


    return render_template(
        'result.html',
        best_path=best_path,
        places=places,
        url=url,
        total_km=total_km,
        total_minutes=formatted_time,
        coords=coords,
        api_key=api_key,
        static_map_url=static_map_url
    )

if __name__ == '__main__':
    print("Uruchamianie aplikacji Flask...")
    app.run(debug=True, port=5000)



# from flask import Flask, render_template, request, redirect, url_for
# import csv
# from logic import genetic_algorithm, load_coords_from_csv, total_distance, calculate_total_distance_and_time, create_distance_matrix, format_duration
# import os
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("GOOGLE_MAPS_API_KEY")

# app = Flask(__name__,
#             static_folder="static",
#             template_folder="templates")
# # Funkcja wczytująca miejsca z CSV
# def load_places_from_csv(filename):
#     places = []
#     with open(filename, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             places.append(row['name'])
#     return places

# @app.route('/', methods=['GET'])
# def index():
#     # Wczytujemy listę zabytków z pliku CSV
#     places = load_places_from_csv('./models/data.csv')
#     return render_template('index.html', places=places)

# @app.route('/route', methods=['POST'])
# def generate_route():
#     selected_places = request.form.getlist('places')  # Pobieramy wybrane zabytki
#     if not selected_places:
#         return redirect(url_for('index'))

#     places = load_places_from_csv('./models/data.csv')
#     selected_indices = [places.index(place) for place in selected_places]

#     best_path, best_history, avg, max_history = genetic_algorithm(
#         n_cities=len(selected_places),
#         mutation_rate=0.05,
#         crossover_rate=0.98,
#         population_size=50,
#         generations=100,
#         selection_method="roulette",
#         elite_size=0.1
#     )

#     coords = load_coords_from_csv('./models/data.csv')

#     # --- Static data for frontend testing ---
#     static_best_path = list(range(len(selected_places))) # Example path: [0, 1, 2, ...]
#     static_total_km = 15.7
#     static_total_minutes = "25 minut"
#     static_coords = [coords[i] for i in selected_indices] # Corresponding coordinates
#     static_url = "https://example.com/mocked_google_maps_url"
#     static_static_map_url = "https://example.com/mocked_static_map_url"
#     # ---------------------------------------

#     return render_template(
#         'result.html',
#         best_path=static_best_path,
#         places=selected_places,
#         url=static_url,
#         total_km=static_total_km,
#         total_minutes=static_total_minutes,
#         coords=static_coords,
#         api_key="DUMMY_API_KEY", # Provide a dummy key for the template if needed
#         static_map_url=static_static_map_url
#     )

# if __name__ == '__main__':
#     print("Uruchamianie aplikacji Flask...")
#     app.run(debug=True, port=5000)