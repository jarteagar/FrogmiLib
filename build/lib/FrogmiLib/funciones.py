import requests
import json

def getSubData(url,token,UUID):

    authHeader = {
        "Authorization": "Bearer %s" %token,
        "User-Agent": "API-CLIENT",
        "X-Company-UUID": UUID,
        "Content-Type": 'application/vnd.api+json',
        }
    queryURL = url
    response = requests.get(queryURL,headers=authHeader)

    if response.status_code != 200:
        return ""
    else:
        rawdata = json.loads(response.text)

        if isinstance(rawdata, dict):
            #si es un diccionaro de datos
            return rawdata
        else:
            return ""
    
#para datos que sean menor o iguala 1000 registros, si fuea de más usar la funcion que hace iteraciones (getDataV2)

#obtiene data de una cantidad definida de registros ==============================================
def getData(urlApi,urlFilter,token,UUID,records):

    authHeader = {
        "Authorization": "Bearer %s" %token,
        "User-Agent": "API-CLIENT",
        "X-Company-UUID": UUID,
        "Content-Type": 'application/vnd.api+json',
        }

    if urlFilter == '':
        queryURL = f'https://api.frogmi.com/api/v3/{urlApi}?per_page={records}'
    else:
        queryURL = f'https://api.frogmi.com/api/v3/{urlApi}?{urlFilter}&per_page={records}'


    response = requests.get(queryURL,headers=authHeader)

    if response.status_code != 200:
        return ""
    else:
        rawdata = json.loads(response.text)
        return rawdata

#obtiene data tomando en cuenta PAGINACION =======================================================
def getDataByPage(urlApi,urlFilter,token,UUID,page,records):

    authHeader = {
        "Authorization": "Bearer %s" %token,
        "User-Agent": "API-CLIENT",
        "X-Company-UUID": UUID,
        "Content-Type": 'application/vnd.api+json',
        }

    if urlFilter == '':
        queryURL = f'https://api.frogmi.com/api/v3/{urlApi}?page={page}&per_page={records}'
    else:
        queryURL = f'https://api.frogmi.com/api/v3/{urlApi}?{urlFilter}&page={page}&per_page={records}'
    print(queryURL)
    response = requests.get(queryURL,headers=authHeader)

    if response.status_code != 200:
        return ""
    else:
        rawdata = json.loads(response.text)
        return rawdata

#obtiene data tomando en cuenta SCROLL_ID =======================================================
#para este ENDPOINT debe pasarse el FILTER y RECORDS(per_page) en la primera consulta
#en la segunda consulta se pasa adiciona el SCROLL_ID y el orden dir=desc
def getDataById(urlApi,urlFilter,scroll_id,token,UUID,records):

    authHeader = {
        "Authorization": "Bearer %s" %token,
        "User-Agent": "API-CLIENT",
        "X-Company-UUID": UUID,
        "Content-Type": 'application/vnd.api+json',
        }

    if scroll_id == '':
        #url para la primera llamada
        queryURL = f'https://api.frogmi.com/api/v3/{urlApi}?{urlFilter}&per_page={records}'
    else:
        #ulr para la segunda llamada
        queryURL = f'https://api.frogmi.com/api/v3/{urlApi}?{urlFilter}&per_page={records}&scroll_id={scroll_id}&dir=desc'
    
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

#activites and questionary
def getActivites(token,UUID,urlFilter,page,records):
    urlApi ="store_beat/activities"
    rw = getDataByPage(urlApi,urlFilter,token,UUID,page,records)

    extracted_data = []

    extracted_act =[]
    extracted_qst =[]
    extracted_alt =[]
    extracted_tag =[]

    for item in rw.get("data",[]):
        id_ = item.get("id",None) #este es el id de la actividad que se usa para las alternativas y los tags

        data_dic ={
            "id":id_, 
            "type":item.get("type",None),
            "name":item.get("attributes",{}).get("name",None),
            "activity_type":item.get("attributes",{}).get("activity_type",None),
            "schedule_type":item.get("attributes",{}).get("schedule_type",None),
            "state":item.get("attributes",{}).get("state",None),
            "instructions":item.get("attributes",{}).get("instructions",None),
            "created_at":item.get("attributes",{}).get("created_at",None),
            "tag_uuid":"",
            "tag_name":""
        }
        
        #completando los tags edn data_dic
        tags = item.get("attributes",{}) .get("tags")
        if tags:
            for tag in tags:
                data_dic["tag_uuid"] = tag.get("uuid",None)
                data_dic["tag_name"] = tag.get("name",None)

        extracted_act.append(data_dic) #acumulando actividades

        #revisando el questionario asociado a la actividad
        #"related": "https://neo.frogmi.com/api/v3/store_beat/activities/faef1a81-93bf-4591-b5b8-9e7a9cb7b7be/questions"
        url_ = item.get("relationships",{}).get("questions",{}).get("links",{}).get("related")
        if url_:
            rw = getSubData(url_,token,UUID)

            if rw:
                #print(f'el RW es: {rw}')
                dt = rw.get("data",[])
                if dt:
                    for iteq in dt: #rw.get("data",[]):
                        data_qst ={
                            "activityid":id_,
                            "questionid":iteq.get("id",None),
                            "type":iteq.get("type",None),
                            "name":iteq.get("attributes",{}).get("name",None),
                            "question_type":iteq.get("attributes",{}).get("question_type",None),
                            "order":iteq.get("attributes",{}).get("order",None),
                            "order_tree":iteq.get("attributes",{}).get("order_tree",None),
                            "min_boundary":iteq.get("attributes",{}).get("min_boundary",None),
                            "max_boundary":iteq.get("attributes",{}).get("max_boundary",None),
                            "input_regex":iteq.get("attributes",{}).get("input_regex",None),
                            "expression":iteq.get("attributes",{}).get("expression",None)
                        }
                        extracted_qst.append(data_qst) #acumulando las preguntas

                        #recolectando las alternativas asociadas:
                        rw_alter = iteq.get("relationships",{}).get("alternatives")  #("alternatives",{})
                        for itm in rw_alter.get("data",[]):
                            dic_alt={
                                "activityid":id_,
                                "alternativeid":itm.get("id",None),
                                "type":itm.get("type",None),
                                "name":itm.get("attributes",{}).get("name",None),
                                "value":itm.get("attributes",{}).get("value",None),
                                "accomplishment":itm.get("attributes",{}).get("accomplishment",None),
                                "order":itm.get("attributes",{}).get("order",None)
                            }
                            extracted_alt.append(dic_alt) #acumulando alternativas
                        
                        #recolectando tag asociados:
                        rw_tags = iteq.get("relationships",{}).get("tags") #("tags",{})
                        for itm in rw_tags.get("data",[]):
                            dic_tag={
                                "activityid":id_,
                                "tagid":itm.get("id",None)
                            }
                            extracted_tag.append(dic_tag)

    dic_data ={
        "act":extracted_act,
        "qst":extracted_qst,
        "alt":extracted_alt,
        "tag":extracted_tag
    }

    extracted_data.append(dic_data)

    return extracted_data

def getEvents(token,UUID,urlFilter,page,records):
    urlApi ="store_beat/events"
    #urlFilter="filters[period][from]=2024-01-07&filters[period][to]=2024-01-07"
 
    #rw = getDataById(urlApi,urlFilter,scroll_id,token,UUID,records)
    rw = getDataByPage(urlApi,urlFilter,token,UUID,page,records)

    #extracted_data = []
    extracted_event =[]

    for item in rw.get("data",[]):
        data_dic={
            "id":item.get("id",None),
            "type":item.get("type",None),
            "store_beat":item.get("attributes",{}).get("store_beat",None),
            "activityId":item.get("attributes",{}).get("activity",{}).get("id",None),
            "storeId":item.get("attributes",{}).get("store",{}).get("id",None),
            "userId":item.get("attributes",{}).get("user",{}).get("id",None),
            "finished_at":item.get("attributes",{}).get("date",{}).get("finished_at",None),
            "uploaded_at":item.get("attributes",{}).get("date",{}).get("uploaded_at",None),
            "started_at":item.get("attributes",{}).get("date",{}).get("started_at",None),
            "created_at":item.get("attributes",{}).get("date",{}).get("created_at",None),
            "lat":item.get("attributes",{}).get("geolocation",{}).get("lat",None),
            "lon":item.get("attributes",{}).get("geolocation",{}).get("lon",None)
        }
        extracted_event.append(data_dic)

    #scroll_id_ = rw['links'].get('scroll_id', 0)
    #totpag = rw['meta']['pagination'].get('total', 0)
    
    #data_dic2 ={
     #   "data":extracted_event,
      #  "records":totpag
    #}

    #extracted_data.append(data_dic2)

    return extracted_event

def getResults(token,UUID,urlFilter,scroll_id,records):
    urlApi ="store_beat/results"
    #urlFilter="filters[period][from]=2024-01-07&filters[period][to]=2024-01-07"
 
    rw = getDataById(urlApi,urlFilter,scroll_id,token,UUID,records)
    extracted_data =[]  #pagina
    extracted_data2 =[] #acumulado_pagina

    extracted_resul = []
    extracted_answe =[]
    extracted_alter =[]

    for item in rw.get("data",[]):

        id_ = item.get("id",None)
        idq_ = item.get("attributes",{}).get("question_uuid",None)

        #DATOS DEL RESULT
        data_dic={
            "type":item.get("type",None),
            "id":id_,
            "name":item.get("attributes",{}).get("name",None),
            "question_type":item.get("attributes",{}).get("question_type",None),
            "question_uuid":idq_,
            "repetition_node":item.get("attributes",{}).get("repetition_node",None),
            "question_order":item.get("attributes",{}).get("question_order",None),
            "page_title":item.get("attributes",{}).get("page_title",None),
            "page_order":item.get("attributes",{}).get("page_order",None),
            "page_path_order":item.get("attributes",{}).get("page_path_order",None),
            "execution_date":item.get("attributes",{}).get("execution",{}).get("execution_date",None),
            "finished_at":item.get("attributes",{}).get("execution",{}).get("finished_at",None),
            "comment":item.get("attributes",{}).get("comment",None),
            "store_beat_events":item.get("relationships",{}).get("store_beat_events",{}).get("data",{}).get("id",None)
        }
        extracted_resul.append(data_dic)


        #RESPUESTAS DEL RESULT
        answers = item.get("attributes",{}).get("answer",[])
        if isinstance(answers, list):
            for rpta in answers:
                answer_dic ={
                    "storeBeatResultId":id_, #id del resultado
                    "question_uuid":idq_, #id de la pregunta
                    "alternativeid":rpta #id de la(s)  respuesta(s)(caso multiplechoice) --> este valor conincide con el ID de la ALTERNATIVA
                }
                extracted_answe.append(answer_dic)

        
        #ALTERNATIVAS DEL RESULT
        alter = item.get("attributes",{}).get("alternatives",{}).get("data",[])
        if isinstance(alter, list):
            for alte in alter:
                alter_dic={
                    "storeBeatResultId":id_, #id del resultado
                    "question_uuid":idq_, #id de la pregunta
                    "alternativeid":alte.get("id",None), #este es el "answerid"
                    "alternativeType":alte.get("type",None),
                    "alternativeName":alte.get("attributes",{}).get("name",None),
                    "alternativeValue":alte.get("attributes",{}).get("value",None),
                    "accomplishment":alte.get("attributes",{}).get("accomplishment",None)
                }
                extracted_alter.append(alter_dic)

        data_dic2 ={
            "resul":extracted_resul,
            "answe":extracted_answe,
            "alter":extracted_alter
        }

        extracted_data.append(data_dic2)

    scroll_id_ = rw['links'].get('scroll_id', 0)

    data_dic = {
        "data":extracted_data,
        "scroll_id": scroll_id_
    }
    extracted_data2.append(data_dic)

    return extracted_data2

def getProducts(token,UUID,nro_page,per_page):
    urlApi="products"

    rw = getDataByPage(urlApi,'',token,UUID,nro_page,per_page)

    extracted_data =[]
    #extracted_data_source =[]
    if rw:
        dt = rw.get("data",[])
        if dt:
            for item in dt:
                data_dic ={
                    "id":item.get("id",None),
                    "name":item.get("attributes",{}).get("name",None),
                    "sku":item.get("attributes",{}).get("sku",None),
                    "ean":item.get("attributes",{}).get("ean",None),
                    "created_at":item.get("attributes",{}).get("created_at",None),
                    "active":1 if item.get("attributes",{}).get("active",None) else 0,
                    "categoriasId":item.get("relationships",{}).get("categories",{}).get("data",{}).get("id",None)
                }
                extracted_data.append(data_dic)
            
            #totpag = rw['meta']['pagination'].get('total', 0)

            #actualizando el diccionario
            #data_dic["data"] = extracted_data
            #data_dic["records"] = totpag
            

    #extracted_data_source.append(data_dic)

    return extracted_data #_source

extracted_data = getProducts('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',5,300)
print(extracted_data)

def getTags(token,UUID,records):

    rawdata = getData("tags",'',token,UUID,records)
    extracted_data =[]

    for item in rawdata.get("data",[]):
        data_dic ={
            "id":item.get("id",None),
            "name":item.get("attributes").get("name",None),
            "active":1 if item.get("attributes").get("active",None) else 0,
            "tag_type": item.get("attributes").get("tag_type",None),
            "sub_kpi":"",
            "sub_name":"",
            "sub_tag_type":""
        }

        #complementando datos del KPI si fuera el caso:
        subkpi = item.get("relationships",{}) .get("tags")
        #print(f'el subkpi ===> {subkpi}')

        url_ =""
        if subkpi:
            for itm in subkpi:
                data_dic["sub_kpi"] = itm.get("id",None)  #el id
                url_ = itm.get("links",{}).get("related",None)

        if url_:
            rw = getSubData(url_,token,UUID)

            if rw:
                    data_dic["sub_name"] = rw.get("data",{}).get("attributes",{}).get("name",None) #nombre
                    data_dic["sub_tag_type"] = rw.get("data",{}).get("attributes",{}).get("tag_type",None) #tipo
        
        extracted_data.append(data_dic)
    
    return extracted_data

def getStores(token,UUID,records):
   
    rawdata = getData('stores','include=zones,brands',token,UUID,records)
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

def getAreas(token,UUID,records):

    rawdata = getData('accountable_areas','',token,UUID,records)


    extracted_data = []
    for item in rawdata.get("data",[]):
        data_dic ={
            "id": item.get("id",None),
            "name":item.get("attributes",{}).get("name",None),
            "code":item.get("attributes",{}).get("code",None),
            "cluster_definitionId":item.get("relationships",{}).get("cluster_definitions",{}).get("data",{}).get("id",None)
        }
        extracted_data.append(data_dic)
    
    return extracted_data

def getUsers(token,UUID,records):
    #records = 500
    rawdata = getData('users','',token,UUID,records)

    extracted_data = []
    for item in rawdata.get("data",[]):
        data_dic ={
            "id":item.get("id",None),
            "name":item.get("attributes",{}).get("name",None),
            "last_name":item.get("attributes",{}).get("last_name",None),
            "email":item.get("attributes",{}).get("email",None),
            "country":item.get("attributes",{}).get("country",None),
            "active":1 if item.get("attributes",{}).get("active",None) else 0,
            "accountable_areas":""
        }
        
        url_ = item.get("relationships",{}).get("accountable_areas",{}).get("links",{}).get("related",None)
        

        #relationships
        if url_:
            rw = getSubData(url_,token,UUID)
            if rw:
                #print(f'el RW es: {rw}')
                dt = rw.get("data",[])
                if dt:
                    for itm in dt:
                        data_dic["accountable_areas"] = itm.get("id",None)
            
        extracted_data.append(data_dic)

    return extracted_data

def help():
    det = """
    Version 2.5 =========================================================================
    Libreria para agilizar el uso de las api de frogmi 5.1.2025
    USO:
    Consultar con John Arteaga!!!
    
    Nota importante _____
    Para modificar las columnas que se retornan, se debe editar el archivo funciones.py
    agregar las columnas en la funcion correspondiente y volver a compilar el archivo WHL:

    --> python .\setup.py bdist_wheel

    Publicar en GITHUB para obtener la version linux del archivo WHL y cagar en el Lakehouse


    Ejemplos de invocacion de API via la libreria ======================================

    STORES **************
    dt = getStores('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',1000)
    print(dt)

    accountable_areas ***************
    dt = getAreas('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',30)
    print(dt)

    USERS *********************
    dt = getUsers('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',500)
    print(dt)

    
    PRODUCTOS *****************
    NOTA: Regresa un arreglo con 2 valores, la DATA y el TOTAL REGISTROS(Records)

    PAGE = 1
    PER_PAGE = 50 #Cantidad de datos por pagina
    rw = getProducts('e8c7821908563ac1101c977fbd80f385', 'ddcd1b2f-e468-481e-8720-7cd386bec5a0', PAGE,PER_PAGE)
    
   
    dt = rw[0].get("data",[])
    if dt:
        for itm in dt:
            print(itm.get("sku",None))
    else:
        print("ya no hay datos")


    TAG ***********************
    rw = getTags('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',1000)
    print(rw)

    RESULTS *********************
    sid =''
    k = 0
    while k <=4:
        dt = getResults('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',"filters[period][from]=2024-01-05&filters[period][to]=2024-01-05",sid,100)
        print(dt)
        sid = dt[0].get("scroll_id",None)
        print(sid)
        k = k + 1

        
    EVENTS *******************************
    sid =''
    k = 0
    page_ = 1
    per_page_ = 1000
    while k <=5:
        print(page_)
        dt = getEvents('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',"filters[period][from]=2025-01-05&filters[period][to]=2025-01-05",page_,per_page_)

        data = dt[0].get("data", [])
        reco = dt[0].get("records",None)
        if data:

            print(data)
            print(f"= NEXT EVENT ======================================================================================!!!!")
            page_ = page_ + 1
            k = k + 1
        else:
            print("= FINALIZADO **************************************************************>>>>>>>>>>>>>>>>>>>>>>>>>>>!!!!")
            break
            
    ACTIVIES **************************
    page = 1
    k = 0
    while k <=1:
        dt = getActivites('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',"",page,2)
        print(dt)
        k = k + 1
        print(page)
        page = page + 1

            
    """
 
    
    return det