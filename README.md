python -c "
import json
from collections import Counter
# NDJSON
e=c=d=0
with open('modelos/UDV_Modelo_de_Datos_Logico_V0.640.ndjson',encoding='utf-8-sig') as f:
  for line in f:
    if not line.strip(): continue
    r=json.loads(line)
    if r['tipo']=='entidad':
      e+=1
      if r.get('descripcion'): c+=1
    if r['tipo']=='campo':
      d+=1
      if r.get('definicion'): pass
# contar campos con definicion
e2=c2=d2=0
with open('modelos/UDV_Modelo_de_Datos_Logico_V0.640.ndjson',encoding='utf-8-sig') as f:
  for line in f:
    if not line.strip(): continue
    r=json.loads(line)
    if r['tipo']=='campo':
      d2+=1
      if r.get('definicion'): c2+=1
print('NDJSON entidades con descripcion:', c,'/',e)
print('NDJSON campos con definicion:', c2,'/',d2)
# JSON
j=json.load(open('modelos/UDV_Modelo_de_Datos_Logico_V0.640.json',encoding='utf-8-sig'))
je=sum(1 for x in j['entidades'] if x.get('descripcion'))
ja=sum(1 for x in j['atributos'] if x.get('descripcion'))
print('JSON entidades con descripcion:', je,'/',len(j['entidades']))
print('JSON atributos con descripcion:', ja,'/',len(j['atributos']))
"
