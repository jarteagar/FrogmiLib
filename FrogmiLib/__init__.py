#from .funciones import getToken

def OSVersion():
    det = """
    Version 2.4 =========================================================================
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
    rw = getData('stores','include=zones,brands',token,UUID,1000)
    dt = getStores(rw)
    print(dt)


    accountable_areas ***************
    rw = getData('accountable_areas','',token,UUID,30)
    dt = getAreas(rw)
    print(dt)

    USERS *********************
    rw = getData('users','',token,UUID,500)
    dt = getUsers(rw,token,UUID) #para obtener el  'accountable_areas' relacionado al USER
    print(dt)

    
    PRODUCTOS *****************
    NOTA: Regresa un arreglo con 2 valores, la DATA y el TOTAL REGISTROS(Records)

    PAGE = 1
    PER_PAGE = 50 #Cantidad de datos por pagina

    dt = getProducts('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',PAGE,PER_PAGE)
    print(dt)

    TAG ***********************
    rw = getData("tags",'','e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',1000)
    dt = getTags(rw,'e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0')
    print(dt)

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
            print(f"= NEXT EVENT {reco}======================================================================================!!!!")
            page_ = page_ + 1
            k = k + 1
        else:
            print("= FINALIZADO **************************************************************>>>>>>>>>>>>>>>>>>>>>>>>>>>!!!!")
            break
            
    ACTIVIES **************************
    page = 1
    k = 0
    while k <=4:
        dt = getActivites('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',"",page,5)
        print(dt)
        k = k + 1
        print(page)
        page = page + 1
            
    """
 
    
    return det

