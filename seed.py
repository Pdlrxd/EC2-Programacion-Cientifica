from sqlmodel import Session, select
from models import (
    Batalla,
    Entrenador,
    Participacion,
    Pokemon,
    PokemonTipo,
    Region,
    Tipo,
)
from database import engine


def seed_data() -> None:
    """Puebla la base de datos con los datos iniciales requeridos."""
    with Session(engine) as session:
        # Check de idempotencia
        if session.exec(select(Region)).first():
            print("Los datos ya han sido sembrados anteriormente.")
            return

        # 1. REGIONES (Al menos 4 de generaciones distintas)
        kanto = Region(nombre="Kanto", generacion=1)
        johto = Region(nombre="Johto", generacion=2)
        hoenn = Region(nombre="Hoenn", generacion=3)
        sinnoh = Region(nombre="Sinnoh", generacion=4)

        session.add_all([kanto, johto, hoenn, sinnoh])
        session.commit()

        # 2. TIPOS ELEMENTALES (Al menos 8, incluyendo Fuego, Agua, Eléctrico)
        t_fuego = Tipo(nombre="Fuego", color_hex="#F08030")
        t_agua = Tipo(nombre="Agua", color_hex="#6890F0")
        t_electrico = Tipo(nombre="Eléctrico", color_hex="#F8D030")
        t_planta = Tipo(nombre="Planta", color_hex="#78C850")
        t_veneno = Tipo(nombre="Veneno", color_hex="#A040A0")
        t_volador = Tipo(nombre="Volador", color_hex="#A890F0")
        t_tierra = Tipo(nombre="Tierra", color_hex="#E0C068")
        t_normal = Tipo(nombre="Normal", color_hex="#A8A878")

        session.add_all(
            [
                t_fuego,
                t_agua,
                t_electrico,
                t_planta,
                t_veneno,
                t_volador,
                t_tierra,
                t_normal,
            ]
        )
        session.commit()

        # 3. ENTRENADORES (Al menos 8 | 2 campeones | 2 misma región)
        e1 = Entrenador(
            nombre="Ash", edad=10, insignias=8, es_campeon=True, region_id=kanto.id
        )
        e2 = Entrenador(
            nombre="Gary", edad=10, insignias=8, es_campeon=False, region_id=kanto.id
        )
        e3 = Entrenador(
            nombre="Cynthia", edad=25, insignias=8, es_campeon=True, region_id=sinnoh.id
        )
        e4 = Entrenador(
            nombre="Brock", edad=15, insignias=0, es_campeon=False, region_id=kanto.id
        )
        e5 = Entrenador(
            nombre="Misty", edad=12, insignias=2, es_campeon=False, region_id=johto.id
        )
        e6 = Entrenador(
            nombre="Norman", edad=35, insignias=5, es_campeon=False, region_id=hoenn.id
        )
        e7 = Entrenador(
            nombre="May", edad=11, insignias=3, es_campeon=False, region_id=hoenn.id
        )
        e8 = Entrenador(
            nombre="Dawn", edad=11, insignias=1, es_campeon=False, region_id=sinnoh.id
        )

        session.add_all([e1, e2, e3, e4, e5, e6, e7, e8])
        session.commit()

        # 4. POKÉMON (Al menos 20 | 3 shiny | 2 con apodo | lvl >= 80 y <= 20)
        pokemons = [
            # Nivel >= 80 y Apodos
            Pokemon(
                nombre="Pikachu",
                nivel=85,
                puntos_vida=200,
                entrenador_id=e1.id,
                apodo="Sparky",
            ),
            Pokemon(nombre="Blastoise", nivel=80, puntos_vida=280, entrenador_id=e2.id),
            # Shinys (3 requeridos) y le damos apodo a 2 de ellos para la Consulta 3
            Pokemon(
                nombre="Charizard",
                nivel=82,
                puntos_vida=250,
                entrenador_id=e1.id,
                es_shiny=True,
                apodo="Smaug",
            ),
            Pokemon(
                nombre="Garchomp",
                nivel=88,
                puntos_vida=300,
                entrenador_id=e3.id,
                es_shiny=True,
            ),
            Pokemon(
                nombre="Pachirisu",
                nivel=22,
                puntos_vida=85,
                entrenador_id=e8.id,
                es_shiny=True,
                apodo="Chispita",
            ),
            # Nivel <= 20
            Pokemon(nombre="Bulbasaur", nivel=15, puntos_vida=60, entrenador_id=e1.id),
            Pokemon(nombre="Eevee", nivel=10, puntos_vida=45, entrenador_id=e2.id),
            Pokemon(nombre="Geodude", nivel=18, puntos_vida=70, entrenador_id=e4.id),
            Pokemon(nombre="Piplup", nivel=12, puntos_vida=55, entrenador_id=e8.id),
            Pokemon(
                nombre="Togepi",
                nivel=5,
                puntos_vida=30,
                entrenador_id=e5.id,
                apodo="Huevito",
            ),
            # Resto para completar los 20
            Pokemon(nombre="Lucario", nivel=75, puntos_vida=220, entrenador_id=e3.id),
            Pokemon(nombre="Onix", nivel=40, puntos_vida=180, entrenador_id=e4.id),
            Pokemon(nombre="Starmie", nivel=50, puntos_vida=160, entrenador_id=e5.id),
            Pokemon(nombre="Slaking", nivel=60, puntos_vida=320, entrenador_id=e6.id),
            Pokemon(nombre="Vigoroth", nivel=35, puntos_vida=130, entrenador_id=e6.id),
            Pokemon(nombre="Blaziken", nivel=65, puntos_vida=210, entrenador_id=e7.id),
            Pokemon(nombre="Beautifly", nivel=25, puntos_vida=90, entrenador_id=e7.id),
            Pokemon(nombre="Snorlax", nivel=70, puntos_vida=400, entrenador_id=e1.id),
            Pokemon(nombre="Gyarados", nivel=55, puntos_vida=240, entrenador_id=e5.id),
            Pokemon(nombre="Crobat", nivel=58, puntos_vida=190, entrenador_id=e2.id),
        ]

        session.add_all(pokemons)
        session.commit()

        # 5. ASIGNACIÓN DE TIPOS (Mínimo 6 con tipos duales)
        asig_tipos = [
            PokemonTipo(pokemon_id=pokemons[0].id, tipo_id=t_electrico.id),
            PokemonTipo(pokemon_id=pokemons[1].id, tipo_id=t_agua.id),
            # Duales (6 requeridos)
            PokemonTipo(pokemon_id=pokemons[2].id, tipo_id=t_fuego.id),
            PokemonTipo(pokemon_id=pokemons[2].id, tipo_id=t_volador.id),  # Dual 1
            PokemonTipo(pokemon_id=pokemons[3].id, tipo_id=t_tierra.id),
            PokemonTipo(pokemon_id=pokemons[3].id, tipo_id=t_volador.id),  # Dual 2
            PokemonTipo(pokemon_id=pokemons[5].id, tipo_id=t_planta.id),
            PokemonTipo(pokemon_id=pokemons[5].id, tipo_id=t_veneno.id),  # Dual 3
            PokemonTipo(pokemon_id=pokemons[18].id, tipo_id=t_agua.id),
            PokemonTipo(pokemon_id=pokemons[18].id, tipo_id=t_volador.id),  # Dual 4
            PokemonTipo(pokemon_id=pokemons[19].id, tipo_id=t_veneno.id),
            PokemonTipo(pokemon_id=pokemons[19].id, tipo_id=t_volador.id),  # Dual 5
            PokemonTipo(pokemon_id=pokemons[10].id, tipo_id=t_veneno.id),
            PokemonTipo(pokemon_id=pokemons[10].id, tipo_id=t_tierra.id),  # Dual 6
            # Tipos simples restantes
            PokemonTipo(pokemon_id=pokemons[4].id, tipo_id=t_electrico.id),
            PokemonTipo(pokemon_id=pokemons[6].id, tipo_id=t_normal.id),
            PokemonTipo(pokemon_id=pokemons[7].id, tipo_id=t_tierra.id),
            PokemonTipo(pokemon_id=pokemons[8].id, tipo_id=t_agua.id),
            PokemonTipo(pokemon_id=pokemons[9].id, tipo_id=t_normal.id),
            PokemonTipo(pokemon_id=pokemons[11].id, tipo_id=t_tierra.id),
            PokemonTipo(pokemon_id=pokemons[12].id, tipo_id=t_agua.id),
            PokemonTipo(pokemon_id=pokemons[13].id, tipo_id=t_normal.id),
            PokemonTipo(pokemon_id=pokemons[14].id, tipo_id=t_normal.id),
            PokemonTipo(pokemon_id=pokemons[15].id, tipo_id=t_fuego.id),
            PokemonTipo(pokemon_id=pokemons[16].id, tipo_id=t_volador.id),
            PokemonTipo(pokemon_id=pokemons[17].id, tipo_id=t_normal.id),
        ]

        session.add_all(asig_tipos)
        session.commit()

        # 6. BATALLAS Y PARTICIPACIONES (Al menos 6 batallas, 1 empate)
        batallas = [
            Batalla(
                fecha="2026-01-10", lugar="Meseta Añil", rondas=3, ganador_id=e1.id
            ),
            Batalla(
                fecha="2026-02-14", lugar="Ciudad Plateada", rondas=1, ganador_id=e4.id
            ),
            Batalla(
                fecha="2026-03-20", lugar="Ciudad Celeste", rondas=5, ganador_id=e5.id
            ),
            Batalla(
                fecha="2026-04-05", lugar="Liga Sinnoh", rondas=6, ganador_id=e3.id
            ),
            Batalla(
                fecha="2026-05-12",
                lugar="Gimnasio Petalburgo",
                rondas=4,
                ganador_id=e6.id,
            ),
            Batalla(
                fecha="2026-06-01", lugar="Ruta 1", rondas=2, ganador_id=None
            ),  # Empate
        ]

        session.add_all(batallas)
        session.commit()

        participaciones = [
            # Batalla 1
            Participacion(
                entrenador_id=e1.id, batalla_id=batallas[0].id, resultado="victoria"
            ),
            Participacion(
                entrenador_id=e2.id, batalla_id=batallas[0].id, resultado="derrota"
            ),
            # Batalla 2
            Participacion(
                entrenador_id=e4.id, batalla_id=batallas[1].id, resultado="victoria"
            ),
            Participacion(
                entrenador_id=e1.id, batalla_id=batallas[1].id, resultado="derrota"
            ),
            # Batalla 3
            Participacion(
                entrenador_id=e5.id, batalla_id=batallas[2].id, resultado="victoria"
            ),
            Participacion(
                entrenador_id=e2.id, batalla_id=batallas[2].id, resultado="derrota"
            ),
            # Batalla 4
            Participacion(
                entrenador_id=e3.id, batalla_id=batallas[3].id, resultado="victoria"
            ),
            Participacion(
                entrenador_id=e1.id, batalla_id=batallas[3].id, resultado="derrota"
            ),
            # Batalla 5
            Participacion(
                entrenador_id=e6.id, batalla_id=batallas[4].id, resultado="victoria"
            ),
            Participacion(
                entrenador_id=e7.id, batalla_id=batallas[4].id, resultado="derrota"
            ),
            # Batalla 6 (Empate)
            Participacion(
                entrenador_id=e1.id, batalla_id=batallas[5].id, resultado="empate"
            ),
            Participacion(
                entrenador_id=e2.id, batalla_id=batallas[5].id, resultado="empate"
            ),
        ]

        session.add_all(participaciones)
        session.commit()
