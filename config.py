def mapper(input_values, mapper_dict):
    ret = []
    for i in input_values:
        ret.append(mapper_dict[str(i)])
    return ret


emotion_id_to_emotion = {
    '2': 'Beslutsamhet',
    '5': 'Beundran',
    '7': 'Tacksamhet',
    '8': 'Upphöjdhet',
    '9': 'Positiv förvåning',
    '13': 'Nöje',
    '16': 'Tillfredsställelse/Belåtenhet',
    '18': 'Vördnad',
    '19': 'Inspiration',
    '20': 'Triumf/Prestation',
    '21': 'Hopp',
    '22': 'Neutral',
    '23': 'Sinnlig njutning',
    '24': 'Sexuell lust',
    '25': 'Lugn/Frid',
    '27': 'Koncentration',
    '28': 'Ömsinthet',
    '29': 'Intresse/Nyfikenhet',
    '33': 'Glädje',
    '36': 'Exalterad/Förväntansfull',
    '38': 'Lättnad',
    '41': 'Stolthet',
    '42': 'Att bli rörd',
    '0': 'Ånger',
    '1': 'Förvirring',
    '3': 'Tvivel',
    '4': 'Avund',
    '6': 'Sorg',
    '10': 'Rädsla',
    '11': 'Negativ förvåning',
    '12': 'Ilska',
    '14': 'Att bli avvisad',
    '15': 'Skadeglädje',
    '17': 'Nöd/Smärta',
    '26': 'Uttråkad',
    '30': 'Nostalgi',
    '31': 'Sarkasm',
    '32': 'Förakt',
    '34': 'Oro/Ängslan',
    '35': 'Äckel',
    '37': 'Besvikelse',
    '39': 'Genans',
    '40': 'Skuld',
    '43': 'Skam'
}