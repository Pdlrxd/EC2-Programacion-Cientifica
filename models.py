from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# --- Tablas Asociativas ---


class PokemonTipo(SQLModel, table=True):
    """Tabla puente N-a-M entre Pokemon y Tipo."""

    pokemon_id: Optional[int] = Field(
        default=None, foreign_key="pokemon.id", primary_key=True
    )
    tipo_id: Optional[int] = Field(
        default=None, foreign_key="tipo.id", primary_key=True
    )


class Participacion(SQLModel, table=True):
    """Tabla puente N-a-M entre Entrenador y Batalla."""

    entrenador_id: Optional[int] = Field(
        default=None, foreign_key="entrenador.id", primary_key=True
    )
    batalla_id: Optional[int] = Field(
        default=None, foreign_key="batalla.id", primary_key=True
    )
    resultado: str


# --- Entidades Principales ---


class Region(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    generacion: int
    descripcion: Optional[str] = None

    # Relación 1-a-N con Entrenador
    entrenadores: List["Entrenador"] = Relationship(back_populates="region")


class Tipo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    color_hex: Optional[str] = None

    # Relación N-a-M con Pokemon
    pokemons: List["Pokemon"] = Relationship(
        back_populates="tipos", link_model=PokemonTipo
    )


class Batalla(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: str
    lugar: str
    rondas: int
    ganador_id: Optional[int] = Field(default=None, foreign_key="entrenador.id")

    # Relación N-a-M con Entrenador
    entrenadores: List["Entrenador"] = Relationship(
        back_populates="batallas", link_model=Participacion
    )


class Entrenador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    edad: int
    insignias: int
    es_campeon: Optional[bool] = Field(default=False)
    region_id: int = Field(foreign_key="region.id")

    # Relaciones
    region: Optional[Region] = Relationship(back_populates="entrenadores")
    pokemons: List["Pokemon"] = Relationship(back_populates="entrenador")
    batallas: List[Batalla] = Relationship(
        back_populates="entrenadores", link_model=Participacion
    )


class Pokemon(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    nivel: int
    puntos_vida: int
    es_shiny: Optional[bool] = Field(default=False)
    apodo: Optional[str] = None
    entrenador_id: int = Field(foreign_key="entrenador.id")

    # Relaciones
    entrenador: Optional[Entrenador] = Relationship(back_populates="pokemons")
    tipos: List[Tipo] = Relationship(back_populates="pokemons", link_model=PokemonTipo)
