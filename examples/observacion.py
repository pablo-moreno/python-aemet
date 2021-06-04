from aemet import Aemet

aemet = Aemet('INSERT YOUR API KEY HERE')

observaciones = aemet.get_observacion_convencional('8416Y')  # Valencia station
assert type(observaciones) is list

for observacion in observaciones:
    print(observacion.__dict__)
