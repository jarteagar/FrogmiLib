python -m erwin_mart inspeccionar --ruta "Modelo DDV/CUBOWU" --objeto LFI_CODAGENCIAFIN --salida inspeccion.txt
Rebuilding cache of generated files for COM support...
Checking A058AF1E-0735-424C-A623-47C3D2E6567Ax0x9x0
Could not add module (IID('{A058AF1E-0735-424C-A623-47C3D2E6567A}'), 0, 9, 0) - <class 'AttributeError'>: module 'win32com.gen_py.A058AF1E-0735-424C-A623-47C3D2E6567Ax0x9x0' has no attribute 'CLSIDToClassMap'
Done.
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\T89486\dataSchema\erwin_mart\__main__.py", line 623, in <module>
    sys.exit(main())
             ^^^^^^
  File "C:\Users\T89486\dataSchema\erwin_mart\__main__.py", line 425, in main
    m = ctx.connect()
        ^^^^^^^^^^^^^
  File "C:\Users\T89486\dataSchema\erwin_mart\session.py", line 89, in connect
    self._conectar_una_vez()
  File "C:\Users\T89486\dataSchema\erwin_mart\session.py", line 107, in _conectar_una_vez
    self.api = self._fabrica_api(self.progid)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\T89486\dataSchema\erwin_mart\session.py", line 22, in _ensure_dispatch
    return win32com.client.gencache.EnsureDispatch(progid)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\T89486\AppData\Roaming\Python\Python312\site-packages\win32com\client\gencache.py", line 647, in EnsureDispatch
    mod = EnsureModule(tla[0], tla[1], tla[3], tla[4], bForDemand=bForDemand)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\T89486\AppData\Roaming\Python\Python312\site-packages\win32com\client\gencache.py", line 543, in EnsureModule
    module.MinorVersion != tlbAttributes[4]
    ^^^^^^^^^^^^^^^^^^^
AttributeError: module 'win32com.gen_py.A058AF1E-0735-424C-A623-47C3D2E6567Ax0x9x0' has no attribute 'MinorVersion'
