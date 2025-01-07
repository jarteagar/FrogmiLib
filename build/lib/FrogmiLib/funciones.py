import requests
import json


#para datos que sean menor o iguala 1000 registros, si fuea de más usar la funcion que hace iteraciones (getDataV2)
def getData(urlApi,urlFilter,token,UUID):

    authHeader = {
        "Authorization": "Bearer %s" %token,
        "User-Agent": "API-CLIENT",
        "X-Company-UUID": UUID,
        "Content-Type": 'application/vnd.api+json',
        }
    queryURL = f'https://api.frogmi.com/api/v3/{urlApi}?filters{urlFilter}&per_page=1000'
    response = requests.get(queryURL,headers=authHeader)

    if response.status_code != 200:
        return ""
    else:
        rawdata = json.loads(response.text)
        return rawdata

def safe_get(data, *keys):
    for key in keys:
        data = data.get(key, None)
        if data is None:
            return None
    return data

def getStores(rawdata):
    extracted_data = []

    for item in rawdata.get("data", []):
        data_dic = {
            "id": safe_get(item, "id"),
            "name": safe_get(item, "attributes", "name"),
            "code": safe_get(item, "attributes", "code"),
            "active": 1 if safe_get(item, "attributes", "active") else 0,  # Cambiamos el true =1, false=0
            "full_address": safe_get(item, "attributes", "full_address"),
            "latitude": safe_get(item, "attributes", "coordinates", "latitude"),
            "longitude": safe_get(item, "attributes", "coordinates", "longitude"),
            "created_at": safe_get(item, "attributes", "created_at"),
            "brandId": safe_get(item, "relationships", "brands", "data", "id"),
            "zoneId": safe_get(item, "relationships", "zones", "data", "id")
        }
        extracted_data.append(data_dic)

    return extracted_data



'''
def getStores(rawdata):
    extracted_data =[]

    for item in rawdata.get("data",[]):
        data_dic ={
            "id":item.get("id",None),
            "name":item.get("attributes",{}).get("name",None),
            "code":item.get("attributes",{}).get("code",None),
            "active":1 if item.get("attributes",{}).get("active",None) else 0, #cambiamos el true =1, false=0
            "full_address":item.get("attributes",{}).get("full_address",None),
            "latitude":item.get("attributes",{}).get("coordinates",{}).get("latitude",None),
            "longitude":item.get("attributes",{}).get("coordinates",{}).get("longitude",None),
            "created_at":item.get("attributes",{}).get("created_at",None),
            "brandId":item.get("relationships",{}).get("brands",{}).get("data",{}).get("id",None),
            "zoneId":item.get("relationships",{}).get("zones",{}).get("data",{}).get("id",None)
        }
        extracted_data.append(data_dic)
    return extracted_data




rw = getData('stores?include=zones,brands','','e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0')
#print(rw)
dt = getStores(rw)
print(dt)
'''

def getStoresdddd(rawdata):
    extracted_data = []
   
    for item in rawdata:
        id_ = item["id"].get("entityId") #id para las subtablas competitors sites y groupings
        extracted_comp_sites =[]
        extracted_comp_groups =[]

        #id	name	code	active	full_address	latitude	longitude	create_at	brandId	zonesId
        data_dic = {
            "EntityId": item.get("id", {}).get("entityId", None),
            "Adress": item.get('data', {}).get('address', None),
            "Adress2": item.get('data', {}).get('address2', None),
            "Adress3": item.get('data', {}).get('address3', None),
            "Adress4": item.get('data', {}).get('address4', None),
            "networkId": item.get('data', {}).get('network', {}).get('entityId', None),  # Maneja el caso cuando 'network' no existe
            "Latitud": item.get('data', {}).get('latitude', None),
            "Longitud": item.get('data', {}).get('longitude', None),
            "name": item.get('data', {}).get('name', None),
            "achievedVolume": item.get('data', {}).get('achievedVolume', None),
            "areaEntityId": item.get('data', {}).get('area', {}).get('entityId', None),
            "brandEntityId": item.get('data', {}).get('brand', {}).get('entityId', None),
            "channelOfTradeEntityId": item.get('data', {}).get('channelOfTrade', {}).get('entityId', None),
            "distanceToNearestOwnSite": item.get('data', {}).get('distanceToNearestOwnSite', None),
            "SiteType2": item.get("id", {}).get("entityVariant", None)
        }

        #SITES DE COMPETIDORES
        rawdata2 = item['data'].get('competitorSites')
        if rawdata2:
            for item2 in rawdata2:
                data_dic2 ={
                    "EntityId":id_,
                    "competitorSitesId":item2.get('entityId')
                }
                extracted_comp_sites.append(data_dic2)

        #GRUPOS
        rawdata3 = item['data'].get('siteGroupings')
        if rawdata3:
            for item3 in rawdata3:
                data_dic3 ={
                    "EntityId":id_,
                    "siteGroupingValueId":item3.get('siteGroupingValueId'),
                    "name":item3.get('name'),
                    "type":item3.get('type'),
                    "optionName":item3.get('optionName')
                }
                extracted_comp_groups.append(data_dic3)

        record = {
            "SiteInfo": data_dic,
            "CompetitorSites": extracted_comp_sites,
            "SiteGroupings": extracted_comp_groups
        }

        extracted_data.append(record)
    return extracted_data

