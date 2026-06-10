# Pokédex DB 🎮

Base de datos relacional del universo Pokémon construida con **SQLModel** + **SQLite**.  
Proyecto EC2 — Programación Científica con Python, UCN 2026.

---

## Requisitos

- Python 3.11+
- pip

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd pokedex_db
```

### 2. Crear y activar el entorno virtual

```bash
# Crear
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en macOS/Linux
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Uso

### Ejecutar el proyecto

```bash
python main.py
```

Esto realizará automáticamente tres pasos:
1. Crea la base de datos `pokedex.db` y todas las tablas
2. Puebla la base de datos con datos iniciales (idempotente: se puede ejecutar varias veces sin duplicar datos)
3. Ejecuta y muestra los resultados de las 8 consultas

### Verificar calidad de código

```bash
# Linter
ruff check .

# Formato
ruff format --check .

# Aplicar formato automáticamente
ruff format .
```

---

## Estructura del proyecto

```
pokedex_db/
├── models.py        # Entidades SQLModel (Region, Entrenador, Pokemon, Tipo, Batalla)
├── database.py      # Engine, creación de tablas y get_session()
├── seed.py          # Poblado inicial de la base de datos
├── queries.py       # Las 8 consultas requeridas
├── main.py          # Punto de entrada
├── requirements.txt # Dependencias del proyecto
└── .gitignore       # Excluye pokedex.db y .venv
```

> `pokedex.db` se genera al correr el proyecto y **no se sube al repositorio**.

---

## Dependencias principales

| Paquete | Uso |
|---|---|
| `sqlmodel` | ORM principal (modelos + consultas) |
| `sqlalchemy` | Motor subyacente (funciones de agregación) |
| `ruff` | Linter y formateador de código |