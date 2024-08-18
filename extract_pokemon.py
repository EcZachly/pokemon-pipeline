import requests
import csv

start_url = 'https://pokeapi.co/api/v2/pokemon-species'

def write_file(rows, header, filename, is_first_call):
    # Write data to the CSV file
    mode = 'w' if is_first_call else 'a'
    with open(filename, mode=mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        # Write the rows
        if is_first_call:
            writer.writeheader()
        writer.writerows(rows)

def get_pokemon_list(url):
    return requests.get(url).json()


def scrape_pokemon_list():
    response = get_pokemon_list(start_url)
    all_results = response['results']
    while response['next'] is not None:
        response = get_pokemon_list(response['next'])
        all_results.extend(response['results'])
        print(len(all_results))
    write_file(all_results, ['name', 'url'],
               'data/pokemon_list.csv', True)


def get_pokemon_details(url, is_first_run):
    keys = [
            'base_happiness',
            'capture_rate',
            'color',
            'egg_groups',
            'evolution_chain',
            'evolves_from_species',
            'flavor_text_entries',
            'form_descriptions',
            'forms_switchable',
            'gender_rate',
            'genera',
            'generation',
            'growth_rate',
            'habitat',
            'has_gender_differences',
            'hatch_counter',
            'id',
            'is_baby',
            'is_legendary',
            'is_mythical',
            'name',
            'names',
            'order',
            'shape',
            'varieties'
    ]
    response = requests.get(url).json()
    print('we are currently getting data for', response['name'], url)
    response['evolution_chain'] = response['evolution_chain']['url']
    response['color'] = response['color']['name']
    response['habitat'] = response['habitat']['name'] if response['habitat'] and 'name' in response['habitat'] else ''
    response['growth_rate'] = response['growth_rate']['name']
    response['generation'] = response['generation']['name']
    response['shape'] = response['shape']['name'] if response['shape'] and 'name' in response['shape'] else ''
    del response['pal_park_encounters']
    del response['pokedex_numbers']
    response['egg_groups'] = list(map(lambda group: group['name'], response['egg_groups']))
    response['flavor_text_entries'] = list(map(lambda flavor: flavor['flavor_text'], response['flavor_text_entries']))
    response['names'] = list(map(lambda flavor: flavor['name'], response['names']))
    response['varieties'] = list(map(lambda variety: variety['pokemon']['url'], response['varieties']))
    write_file([response], keys, 'data/pokemon_details.csv', is_first_run)
    return response


def scrape_all_pokemon_details():
    data = []
    with open('data/pokemon_list.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    is_first_run = True
    for pokemon in data:
        get_pokemon_details(pokemon['url'], is_first_run)
        is_first_run = False