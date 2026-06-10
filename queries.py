from sqlmodel import Session, select, col
from sqlalchemy import func, case, text


from models import (
    Entrenador,
    Participacion,
    Pokemon,
    PokemonTipo,
    Region,
    Tipo,
)


def pokemon_alto_nivel(session: Session, umbral: int = 70) -> list[Pokemon]:
    """Retorna Pokémon con nivel mayor o igual al umbral, ordenados de mayor a menor."""
    statement = (
        select(Pokemon)
        .where(col(Pokemon.nivel) >= umbral)
        .order_by(col(Pokemon.nivel).desc())
    )
    return list(session.exec(statement).all())


def campeones_por_region(session: Session, nombre_region: str) -> list[Entrenador]:
    """Retorna entrenadores campeones de una región específica."""
    statement = (
        select(Entrenador)
        .join(Region)
        .where(col(Region.nombre) == nombre_region)
        .where(col(Entrenador.es_campeon).is_(True))
    )
    return list(session.exec(statement).all())


def shiny_con_apodo(session: Session) -> list[tuple[str, str | None, int, str]]:
    """Retorna datos de Pokémon shiny que tienen un apodo asignado."""
    statement = (
        select(Pokemon.nombre, Pokemon.apodo, Pokemon.nivel, Entrenador.nombre)
        .join(Entrenador)
        .where(col(Pokemon.es_shiny).is_(True))
        .where(col(Pokemon.apodo).is_not(None))
    )
    return list(session.exec(statement).all())


def promedio_nivel_por_entrenador(session: Session) -> list[tuple[str, float]]:
    """Retorna el promedio de nivel de los Pokémon por entrenador."""
    statement = (
        select(Entrenador.nombre, func.round(func.avg(col(Pokemon.nivel)), 2))
        .join(Pokemon)
        .group_by(col(Entrenador.id))
        .order_by(func.avg(col(Pokemon.nivel)).desc())
    )
    return list(session.exec(statement).all())


def conteo_pokemon_por_tipo(session: Session) -> list[tuple[str, int]]:
    """Retorna la cantidad de Pokémon asociados a cada tipo."""
    statement = (
        select(Tipo.nombre, func.count(col(PokemonTipo.pokemon_id)))
        .join(PokemonTipo)
        .group_by(col(Tipo.id))
        .order_by(func.count(col(PokemonTipo.pokemon_id)).desc())
    )
    return list(session.exec(statement).all())


def estadisticas_batallas(session: Session) -> list[tuple[str, int, int, int]]:
    """Retorna el total de batallas, victorias y derrotas por entrenador."""
    statement = (
        select(
            Entrenador.nombre,
            func.count(col(Participacion.batalla_id)),
            func.sum(case((col(Participacion.resultado) == "victoria", 1), else_=0)),
            func.sum(case((col(Participacion.resultado) == "derrota", 1), else_=0)),
        )
        .join(Participacion)
        .group_by(col(Entrenador.id))
        .order_by(func.count(col(Participacion.batalla_id)).desc())
    )
    return list(session.exec(statement).all())


def region_mas_insignias(session: Session) -> tuple[str, float]:
    """Retorna la región con el mayor promedio de insignias entre sus entrenadores."""
    statement = (
        select(Region.nombre, func.round(func.avg(col(Entrenador.insignias)), 2))
        .join(Entrenador)
        .group_by(col(Region.id))
        .order_by(func.avg(col(Entrenador.insignias)).desc(), col(Region.nombre).asc())
        .limit(1)
    )
    resultado = session.exec(statement).first()
    return resultado if resultado else ("Ninguna", 0.0)


def consulta_libre(session: Session) -> list[dict]:
    """
    Retorna el Pokémon de mayor nivel de cada entrenador.
    Se utiliza SQL crudo porque requiere una subconsulta correlacionada en el WHERE,
    lo cual es verboso y complejo de expresar de forma limpia con el ORM.
    """
    query = text("""
        SELECT e.nombre AS entrenador_nombre, p.nombre AS pokemon_nombre, p.nivel
        FROM Entrenador e
        JOIN Pokemon p ON e.id = p.entrenador_id
        WHERE p.nivel = (
            SELECT MAX(nivel) 
            FROM Pokemon 
            WHERE entrenador_id = e.id
        )
        ORDER BY p.nivel DESC
    """)
    # Usamos session.execute() en vez de session.exec() para compatibilidad con text()
    resultados = session.execute(query).mappings().all()
    return [dict(row) for row in resultados]
