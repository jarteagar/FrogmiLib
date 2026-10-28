Remove-Item -Recurse -Force "$env:LOCALAPPDATA\Temp\gen_py" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:USERPROFILE\AppData\Local\Temp\gen_py" -ErrorAction SilentlyContinue
python -c "import win32com; print(win32com.__gen_path__)"
