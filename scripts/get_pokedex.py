import urllib.request
import os
pokedex_url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/'
total_gen_pokemon = 152
os.chdir('../app/static/images/profile')

for idx in range(1, total_gen_pokemon):
    pokemon_id = str(idx).zfill(3)
    filename = pokemon_id + '.png'
    url = pokedex_url + filename
    try:
        print('downloading... ' + filename)
        urllib.request.urlretrieve(url, filename)
    except:
        print('error occured')
