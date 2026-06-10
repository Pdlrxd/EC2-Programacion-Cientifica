from database import create_db_and_tables, get_session
from seed import seed_data
from queries import (
    campeones_por_region,
    consulta_libre,
    conteo_pokemon_por_tipo,
    estadisticas_batallas,
    pokemon_alto_nivel,
    promedio_nivel_por_entrenador,
    region_mas_insignias,
    shiny_con_apodo,
)


def main() -> None:
    # 1. Crear la base de datos y las tablas
    print("Inicializando base de datos")
    create_db_and_tables()

    # 2. Poblar la base de datos (Idempotente)
    print("Sembrando datos iniciales")
    seed_data()

    # 3. Ejecutar las consultas y mostrar los resultados
    print("\n" + "=" * 50)
    print("EJECUTANDO CONSULTAS POKÉMON")
    print("=" * 50 + "\n")

    with get_session() as session:
        # Consulta 1
        print("Consulta 1: Pokémon de alto nivel (>= 70)")
        pokemons_fuertes = pokemon_alto_nivel(session)
        for p in pokemons_fuertes:
            apodo_str = f" ('{p.apodo}')" if p.apodo else ""
            print(f"- Nv.{p.nivel} {p.nombre}{apodo_str}")
        print()

        # Consulta 2
        print("Consulta 2: Campeones de la región Kanto")
        campeones_kanto = campeones_por_region(session, "Kanto")
        for c in campeones_kanto:
            print(f"- {c.nombre} ({c.insignias} insignias)")
        print()

        # Consulta 3
        print("Consulta 3: Pokémon Shiny con apodo")
        shinys = shiny_con_apodo(session)
        for nombre, apodo, nivel, entrenador in shinys:
            print(f"- {nombre} ('{apodo}') - Nv.{nivel} (Entrenador: {entrenador})")
        print()

        # Consulta 4
        print("Consulta 4: Promedio de nivel por entrenador")
        promedios = promedio_nivel_por_entrenador(session)
        for entrenador, promedio in promedios:
            print(f"- {entrenador}: {promedio} promedio de nivel")
        print()

        # Consulta 5
        print("Consulta 5: Conteo de Pokémon por tipo")
        conteo_tipos = conteo_pokemon_por_tipo(session)
        for tipo, cantidad in conteo_tipos:
            print(f"- Tipo {tipo}: {cantidad} Pokémon")
        print()

        # Consulta 6
        print("Consulta 6: Estadísticas de batallas")
        estadisticas = estadisticas_batallas(session)
        for nombre, total, victorias, derrotas in estadisticas:
            print(f"- {nombre}: {total} batallas ({victorias}V - {derrotas}D)")
        print()

        # Consulta 7
        print("Consulta 7: Región con mayor promedio de insignias")
        region, prom_insignias = region_mas_insignias(session)
        print(
            f"- La región líder es {region} con un promedio de {prom_insignias} insignias."
        )
        print()

        # Consulta 8
        print("Consulta 8: El Pokémon más fuerte de cada entrenador (SQL Crudo)")
        mas_fuertes = consulta_libre(session)
        for fila in mas_fuertes:
            print(
                f"- {fila['entrenador_nombre']} -> {fila['pokemon_nombre']}"
                f" (Nv. {fila['nivel']})"
            )
        print()


if __name__ == "__main__":
    main()
