import os
import json
import re
import random

#Ignorar este codigo, su unico objetivo fue arreglar algunos numeros que fueron escritos con +53 u otros valores.
def clean_json_files(directory, keys, verb=False):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if verb: print(f'Archivo: {filepath}:')
                    for key, func in keys.items():
                        if key in data:
                            old_value = data[key]
                            data[key] = func(data[key])
                            if old_value != data[key]:
                                print(f"---- Cambiado : {old_value} -> {data[key]}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"Error en '{filepath}': {e}")

def clean_phone_number(value):
    if 'phone' in value:
        phone_str = str(value['phone'])
        cleaned_phone = re.sub(r'\D', '', phone_str)
        if len(cleaned_phone) > 8:
            cleaned_phone = cleaned_phone[-8:]
    value['phone'] = cleaned_phone if len(cleaned_phone) else None
    return value
    
def repair_location(value):
    if value['coords_x'] == 0.0 or value['coords_y'] == 0.0:
        value['coords_x'] = None
        value['coords_y'] = None
        print(f'----Cambiado: x & y por None')
    return value
    
def repair_municipality(value):
    nombre_municipe = {
        'Arroyo Naranjo': 'Arroyo Naranjo',
        'arroyo naranjo': 'Arroyo Naranjo',
        'Boyeros': 'Boyeros',
        'boyeros': 'Boyeros',
        'Centro Habana': 'Centro Habana',
        'Cerro': 'Cerro',
        'cerro': 'Cerro',
        'Cotorro': 'Cotorro',
        'Diez de Octubre': 'Diez de Octubre',
        'Guanabacoa': 'Guanabacoa',
        'Habana Del Este': 'Habana del Este',
        'Habana Vieja': 'Habana Vieja',
        'Habana del Este': 'Habana del Este',
        'La Habana Vieja': 'Habana Vieja',
        'La Lisa': 'La Lisa',
        'Marianano': 'Marianao',
        'Marianao': 'Marianao',
        'Playa': 'Playa',
        'Plaza de la Revolucion': 'Plaza de la Revolucion',
        'Plaza de la revolucion': 'Plaza de la Revolucion',
        'Regla': 'Regla',
        'San Miguel del Padro': 'San Miguel del Padron',
        'San Miguel del Padron': 'San Miguel del Padron',
        'la habana del este': 'Habana del Este',
        'regla': 'Regla',
        'lisa': 'La Lisa',
        'san miguel del padron': 'San Miguel del Padron',
        'habana vieja': 'Habana Vieja',
        'habana del este': 'Habana del Este',
    }
    for k,v in nombre_municipe.items():
        if value == k:
            value = v
            print(f'----{k} Cambiado \'municipality\'a {v}')
    return value

def repair_type(value):
    type_dict = {
        'restaurant': 'restaurant',
        'bar': 'bar',
        'Restaurante': 'restaurant',
        'restaurante': 'restaurant',
        'cafeteria': 'restaurant',
        'bar': 'bar',
        'Restaurant': 'restaurant',
        'BarRestaurante': 'restaurant',
        'Bar': 'bar',
        'barcafeteriarestaurante': 'restaurant',
        'bar-restaurante': 'restaurant',
        'bar-restaurant': 'restaurant',
        'Bar-Restaurante': 'restaurant',
        'Bar/Restaurante': 'restaurant',
        'Pizzeria': 'restaurant',
        'Cafeteria': 'restaurant',
        'Cafe': 'restaurant',
        'Internacional': 'restaurant',
        'Criolla': 'restaurant',
        'cocteleria': 'restaurant',
        'familiar': 'restaurant',
        'Dulceria': 'restaurant',
        'Pizza': 'restaurant',
        'Mediterranea': 'restaurant',
        'Europea': 'restaurant',
        'Caribena': 'restaurant',
        'Latina': 'restaurant',
        'Cubana': 'restaurant',
        'Centroamericana': 'restaurant',
        'Indio': 'restaurant',
        'Grill': 'restaurant',
        'Saludable': 'restaurant',
        'Americana': 'restaurant',
        'Comida rapida': 'restaurant',
        'Pub': 'restaurant',
        'Hotel': 'restaurant',
        'Pizzas': 'restaurant',
        'Pastas': 'restaurant',
        'hamburguesas': 'restaurant',
        'Parrillada': 'restaurant',
    }
    
    new_list = []
    for i,v in enumerate(value):
        if v in type_dict and type_dict[v] not in new_list and type_dict[v] != '':
            new_list.append(type_dict[v])

    
    if len(new_list) <=0:
        new_list = ['restaurant']
    print(f'----{value} Cambiado \'type\' a {new_list}')
    return new_list

def repair_plates(value):
    for k,v in enumerate(value):
        if v['type'] in ['non-alcoholic_drinks', 'juices', 'smoothie', 'ice_cream_shake']:
            value[k]['type'] = 'non_alcoholic_drinks'
        if v['type'] == 'sushi':
            value[k]['type'] = 'seafood'
        if v['type'] == 'risotto':
            value[k]['type'] = 'mains'
        if v['type'] == 'coffee':
            value[k]['type'] = 'infusions'
        if v['type'] == 'alcoholic_drinks':
            value[k]['type'] = 'alcoholic_drinks'
    return value

def repair_prices(value):
    for k,v in enumerate(value):
        if isinstance(v['price'], str):
            try:
                value[k]['price'] = float(v['price'].replace(',', '.').replace('€', '').replace('$', '').replace('CUP', '').replace('CUC', '').replace('USD', '').strip())
            except:
                print(f"Error al convertir el precio: {v['price']} en el archivo.")
                value[k]['price'] = None
    return value
if __name__ == "__main__":
    clean_json_files('jsons',{
        'contact': clean_phone_number,
        'municipality': repair_municipality,
        'type': repair_type,
    },
    verb=True
    )
