import csv
import os
import os.path as op
from app import static_path
# Maps Pokemon Name to static filename


def create_pokemon_dict():
    file_path = op.join(static_path, 'csv')
    pokedex = dict()
    os.chdir(file_path)
    with open('pokemon-gen1.csv', newline='') as csvfile:
        pokereader = csv.DictReader(csvfile)
        for row in pokereader:
            name = row['Name']
            number = row['Number']
            pokedex[name] = '/static/images/profile/' + \
                str(number).zfill(3) + '.png'
    return pokedex
