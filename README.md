# ⬡ Hockey Tracker — Flask Web App

## Instalación

1. Instala Flask (solo la primera vez):
```
pip install flask
```

2. Ejecuta la app:
```
python app.py
```

3. Abre tu navegador en:
```
http://localhost:5000
```

## Estructura de archivos

```
hockey_app/
├── app.py              ← servidor Flask (backend)
├── templates/
│   └── index.html      ← interfaz web (frontend)
└── saves/              ← aquí se guardan los partidos (se crea automáticamente)
```

## Funcionalidades

- Registra goles, tiros, PCs, corners y tarjetas por equipo
- Cambia los nombres de los equipos antes del partido
- Guarda las estadísticas en un archivo JSON en la carpeta `saves/`
- Reinicia el marcador para un nuevo partido

## Compartir con otros (red local)

Para que otros en tu red WiFi puedan acceder:

Cambia la última línea de `app.py` por:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

Luego comparte tu IP local (ej: `http://192.168.1.X:5000`)
