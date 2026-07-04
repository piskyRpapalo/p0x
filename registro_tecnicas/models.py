"""
Registro de Tecnicas — P0X (motor de metodo)
Datos: /mnt/nvme/p0x/registro_tecnicas/tecnicas/{id}.json
Cuaderno de laboratorio (hipotesis de metodo + evidencia), SEPARADO del Codice (diario).

SUELO:
- Cada tecnica lleva su FUERZA DE EVIDENCIA honesta (meta-analisis / estudio / heuristica / n=1).
- n=1 produce heuristica personal, nunca "ciencia general".
- Cero juicio de la persona; se registra la tecnica y su evidencia.
- Es un registro de metodos de APRENDIZAJE. No de estrategias de trading.

ORDEN (no se viola): este modulo es el CONTENEDOR. La REGLA de actualizacion del score
Hebbiano y los umbrales de transicion de estado se DERIVAN del corpus de psicologia
(build siguiente), NO se decretan aqui. Los stubs lo marcan.
"""
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class EstadoTecnica(str, Enum):
    INCUBATING = "INCUBATING"
    MADURA = "MADURA"
    CANONIZADA = "CANONIZADA"
    DESCARTADA = "DESCARTADA"


class FuerzaEvidencia(str, Enum):
    META_ANALISIS = "meta_analisis"
    ESTUDIO_UNICO = "estudio_unico"
    HEURISTICA_CAMPO = "heuristica_campo"
    N1_PERSONAL = "n1_personal"


class Origen(str, Enum):
    PRECEPTOR = "preceptor"
    SINODO = "sinodo"
    GEMINI = "gemini"
    SOBERANO = "soberano"


class Evidencia(BaseModel):
    model_config = ConfigDict(extra="forbid")
    fuente: str
    fuerza: FuerzaEvidencia
    nota: Optional[str] = None
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ExperimentoN1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hipotesis: str                          # tecnica -> efecto esperado en retencion
    tema_intervencion: str
    tema_control: Optional[str] = None
    fecha_intervencion: date
    prediccion: str
    fecha_medicion: Optional[date] = None    # "explicaselo a tu yo pasado" diferido
    resultado: Optional[str] = None
    error_prediccion: Optional[float] = None
    notas: Optional[str] = None


class Tecnica(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id_tecnica: str = Field(..., pattern=r"^TEC_\d{3}$")
    nombre: str
    descripcion: str
    estado: EstadoTecnica = EstadoTecnica.INCUBATING
    score_hebbiano: float = Field(default=0.5, ge=0.0, le=1.0)  # REGLA derivada del corpus
    origen: Origen
    hipotesis: str
    evidencias: list[Evidencia] = Field(default_factory=list)
    experimentos: list[ExperimentoN1] = Field(default_factory=list)
    fecha_alta: date = Field(default_factory=date.today)
    fecha_revision: Optional[date] = None
    notas: Optional[str] = None

    # --- Mecanica derivada del corpus (NO decretada aqui) ---
    def actualizar_score(self, *a, **k) -> None:
        raise NotImplementedError(
            "La regla de actualizacion del score Hebbiano se deriva del corpus de "
            "psicologia (build siguiente). El contenedor existe; la mecanica no se decreta."
        )

    def evaluar_transicion(self) -> EstadoTecnica:
        raise NotImplementedError(
            "Los umbrales INCUBATING->MADURA->CANONIZADA/DESCARTADA se derivan del corpus."
        )


# --- Persistencia soberana (un JSON por tecnica, editable a mano) ---
RAIZ = Path("/mnt/nvme/p0x/registro_tecnicas/tecnicas")

def guardar(t: Tecnica, raiz: Path = RAIZ) -> Path:
    raiz.mkdir(parents=True, exist_ok=True)
    p = raiz / f"{t.id_tecnica}.json"
    p.write_text(t.model_dump_json(indent=2), encoding="utf-8")
    return p

def cargar(id_tecnica: str, raiz: Path = RAIZ) -> Tecnica:
    return Tecnica.model_validate_json((raiz / f"{id_tecnica}.json").read_text("utf-8"))

def listar(raiz: Path = RAIZ) -> list[Tecnica]:
    if not raiz.exists():
        return []
    return [Tecnica.model_validate_json(p.read_text("utf-8")) for p in sorted(raiz.glob("*.json"))]


if __name__ == "__main__":
    # Validacion con un ejemplo PEDAGOGICO (no trading).
    t = Tecnica(
        id_tecnica="TEC_001",
        nombre="Numeros grandes en el grafico",
        descripcion="Mostrar las cifras clave en tamano grande dentro de un diagrama.",
        origen=Origen.SOBERANO,
        hipotesis="Cifras grandes -> mejor retencion a 3 meses que cifras pequenas.",
        evidencias=[Evidencia(fuente="hipotesis del Soberano", fuerza=FuerzaEvidencia.N1_PERSONAL)],
    )
    print(t.model_dump_json(indent=2))
    assert t.estado is EstadoTecnica.INCUBATING and t.score_hebbiano == 0.5
    print("OK · contenedor valido · score = STUB (mecanica pendiente del corpus)")
