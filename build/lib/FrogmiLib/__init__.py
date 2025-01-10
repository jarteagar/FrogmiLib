# Importamos las funciones de 'funciones.py' 
from .funciones import (
    getStores,
    getAreas,
    getUsers,
    getProducts,
    getTags,
    getResults,
    getEvents,
    getActivites
)

def help():
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

    dt = getProducts('e8c7821908563ac1101c977fbd80f385','ddcd1b2f-e468-481e-8720-7cd386bec5a0',PAGE,PER_PAGE)
    print(dt)

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

