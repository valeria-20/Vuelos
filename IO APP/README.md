# Viaja Seguro

Aplicación Streamlit de gestión y optimización de rutas aéreas del Ecuador.

## Flujo de la aplicación

1. **Portada** ("Bienvenidos") con el botón **Inicio**.
2. **Menú principal** ("VIAJA SEGURO") con las tarjetas:
   - Aeropuertos
   - Rutas
   - Optimización (mínimo simple)
   - Distancias
   - Tiempo
   - Costos (optimización por método Simplex usando `scipy.optimize.linprog`)
3. **Panel de Monitoreo (Dashboard)**: simulación de indicadores por ruta
   (Distancia total, Tiempo estimado, Consumo de combustible, Costo del
   recorrido, Número de escalas, Estado del vuelo).

## Cómo ejecutar en Visual Studio Code

1. Abre esta carpeta en VS Code.
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS / Linux
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```
5. Se abrirá automáticamente en el navegador (usualmente `http://localhost:8501`).
