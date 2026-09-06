#!/usr/bin/env python3
"""El gate de la capa Alejandria. No existia ninguno.

POR QUE HACE FALTA UN GATE PROPIO
---------------------------------
Los dos gates del proyecto no miran aqui, y no por descuido: el del MVP tiene su
raiz en `preceptor/` y `Alejandria/` es su hermano, no su hijo; el de la web
solo escanea `public/` de otro repositorio.

Asi que hasta hoy esta capa -- la que MIDE el rack y la que el Soberano lee para
decidir -- no tenia quien la midiera a ella. El instrumento sin instrumento.

    python3 ~/p0x/Alejandria/test_alejandria.py
"""
from __future__ import annotations

import json
import os
import inspect
import re
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "mensajes"))
import mensajes as M  # noqa: E402

# El tope de la capa Alejandria: 32 KB por fichero.
#
# CORRIGE a la D1-bis de 10 KB que se firmo antes: `plan_v5.md` -- el contrato
# visual y de prioridades vigente -- abre con «Capa Alejandria: tope 32 KB/
# fichero», y ese contrato manda sobre una regla mia anterior.
#
# El motivo del cambio es el Ojo-Vivo: la topologia, los estados y el
# mobiliario que vienen en V1-V4 no caben en 10 KB por fichero sin trocear la
# consola en una docena de modulos, y una docena de ficheros de 800 bytes no se
# lee mejor que cuatro de 8 KB -- se lee peor.
#
# Lo que NO cambia es por que hay tope: el Ojo se sirve en loopback y no paga
# latencia de red, asi que esto no protege una descarga; protege que el fichero
# se pueda leer entero. `dashboard.js` con 25 KB es la prueba de a donde lleva
# no tener ninguno.
TOPE = 32 * 1024
CONSOLA = RAIZ / "ojo"


class PesoDeLaConsola(unittest.TestCase):

    def test_cada_fichero_de_la_consola_bajo_10_kb(self):
        for p in sorted(CONSOLA.rglob("*")):
            if p.is_file() and p.suffix in (".html", ".css", ".js"):
                with self.subTest(fichero=p.name):
                    self.assertLess(
                        p.stat().st_size, TOPE,
                        f"{p.name} pesa {p.stat().st_size} B · D1-bis son "
                        f"{TOPE}. Partelo en modulos, no lo recortes: los "
                        "comentarios de esta capa son su razonamiento.")

    def test_la_consola_solo_escucha_en_loopback(self):
        """Que nadie la ate a 0.0.0.0 «temporalmente».

        La auditoria del 2026-08-30 encontro un `http.server` en 0.0.0.0:8080
        sin auth ni logs, seis horas expuesto. El Ojo ensena el rack ENTERO: si
        se ata a todas las interfaces, lo reparte.
        """
        codigo = (CONSOLA / "ojo.py").read_text(encoding="utf-8")
        self.assertIn('("127.0.0.1", a.puerto)', codigo,
                      "el Ojo ya no fija 127.0.0.1 al abrir el socket")
        self.assertNotIn('"0.0.0.0"', codigo, "el Ojo escucha fuera de loopback")


class ElActa(unittest.TestCase):
    """Los tres candados del acta. Cada uno se prueba ensuciandola de verdad."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.ruta = Path(self.dir) / "mensajes.jsonl"

    def _uno(self, humano="Dos hallazgos y 3 commits.", maquina=None, fuente=None):
        return M.escribir(
            de="enlace", para=["soberano"], tipo="digesto",
            humano=humano,
            maquina=maquina if maquina is not None else
            {"hechos": ["2 hallazgos", "3 commits"], "acciones": []},
            fuente=fuente if fuente is not None else ["loops.db:latidos"],
            ruta=self.ruta)

    def test_la_cadena_sana_se_verifica(self):
        for _ in range(3):
            self._uno()
        self.assertEqual(M.verificar(self.ruta), [])

    def test_un_mensaje_sin_fuente_no_se_escribe(self):
        with self.assertRaises(ValueError) as e:
            self._uno(fuente=[])
        self.assertIn("fuente", str(e.exception))

    def test_una_linea_modificada_rompe_la_cadena(self):
        self._uno(); self._uno(); self._uno()
        lineas = self.ruta.read_text(encoding="utf-8").splitlines()
        m = json.loads(lineas[1])
        m["humano"] = "esto lo cambio alguien despues"      # sin recalcular hash
        lineas[1] = json.dumps(m, ensure_ascii=False)
        self.ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

        rotos = M.verificar(self.ruta)
        self.assertTrue(rotos, "el acta se dejo modificar sin protestar")
        self.assertTrue(any("cambió después de escribirse" in r for r in rotos),
                        f"no senala la edicion: {rotos}")
        # Y la siguiente tambien cae: la cadena propaga.
        self.assertTrue(any("se insertó, se borró o se reordenó" in r for r in rotos),
                        f"la cadena no propago el fallo: {rotos}")

    def test_una_linea_borrada_rompe_la_cadena(self):
        self._uno(); self._uno(); self._uno()
        lineas = self.ruta.read_text(encoding="utf-8").splitlines()
        del lineas[1]
        self.ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        self.assertTrue(M.verificar(self.ruta),
                        "borrar una linea del medio no rompio nada")

    def test_no_se_escribe_encima_de_un_acta_rota(self):
        self._uno(); self._uno()
        lineas = self.ruta.read_text(encoding="utf-8").splitlines()
        m = json.loads(lineas[0]); m["humano"] = "manipulado"
        lineas[0] = json.dumps(m, ensure_ascii=False)
        self.ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        with self.assertRaises(M.ActaRota):
            self._uno()

    def test_las_dos_caras_tienen_que_contar_lo_mismo(self):
        """Criterio B5 del Medallon, aplicado a lo comprobable.

        No se juzga la prosa -- eso es justo lo que el Medallon dice que no
        cuenta. Se comprueba que toda cifra de la cara humana este respaldada
        por la de maquina: un numero que solo existe en el texto no lo midio
        nadie.
        """
        with self.assertRaises(ValueError) as e:
            self._uno(humano="Se cerraron 47 hallazgos.",
                      maquina={"hechos": ["2 hallazgos"], "acciones": []})
        self.assertIn("47", str(e.exception))

    def test_el_acta_viva_del_nodo_esta_sana(self):
        """La de verdad, no una de mentira."""
        viva = RAIZ / "mensajes" / "mensajes.jsonl"
        if not viva.exists():
            self.skipTest("todavia no hay acta en este nodo")
        self.assertEqual(M.verificar(viva), [])


class GateDelEnlace(unittest.TestCase):
    """B1-B5 del Medallon, comprobados sin llamar al modelo.

    Se le pasa prosa sintetica a `gate()` y se mira que veredicto da. No hace
    falta Ollama: el gate es codigo determinista, y una prueba que necesitara
    el modelo para comprobar el gate del modelo seria su propia contradiccion.
    """

    def setUp(self):
        sys.path.insert(0, str(RAIZ / "digesto"))
        import digesto
        self.D = digesto
        self.lista = [
            {"clave": "bucle guardian", "valor": "ok · 77 ficheros mirados",
             "fuente": "loops.db:latidos/guardian"},
            {"clave": "mvp_gate", "valor": "436 pruebas en verde",
             "fuente": "estado.json:mvp_gate"},
        ]
        # Un hueco cualquiera sirve de ejemplo; se usa uno REAL para que el
        # fixture no documente un concepto retirado.
        self.huecos = [("bandeja_firmas.md", "no existe",
                        "revisar director.py")]

    def _prosa(self, firma="¿Firmas la F1?", extra=""):
        return ("## Qué pasó\n- El guardián miró 77 ficheros. "
                "[loops.db:latidos/guardian]\n" + extra +
                "\n## Qué piensa cada agente\n- guardian: 77 ficheros. "
                "[loops.db:latidos/guardian]\n"
                "\n## Qué necesita tu firma\n" + firma +
                "\n\n## NO_DATA\n- no existe [bandeja_firmas.md]\n")

    def test_una_parafrasis_limpia_pasa(self):
        self.assertEqual(self.D.gate(self._prosa(), self.lista, self.huecos), [])

    def test_B3_muerde_con_una_fuente_inventada(self):
        mala = self._prosa(extra="- Segun el informe. [informe_secreto.md]\n")
        fallos = self.D.gate(mala, self.lista, self.huecos)
        self.assertTrue(any(f.startswith("B3") for f in fallos), fallos)
        self.assertIn("informe_secreto.md", " ".join(fallos))

    def test_B3_admite_varias_fuentes_en_un_corchete(self):
        """Una viñeta que resume dos hechos cita los dos. Es legitimo.

        El gate leia el corchete entero como UNA fuente y tumbaba parafrasis
        correctas. Este caso existe para que no vuelva a pasar.
        """
        buena = self._prosa(extra="- Todo verde. "
                            "[loops.db:latidos/guardian, estado.json:mvp_gate]\n")
        self.assertEqual([f for f in self.D.gate(buena, self.lista, self.huecos)
                          if f.startswith("B3")], [])

    def test_B3_admite_citar_algo_que_venia_DENTRO_de_un_hecho(self):
        """El material entregado incluye el TEXTO de los huecos, no solo su clave.

        La primera corrida real tumbo una parafrasis correcta porque el modelo
        cito un trozo de texto que estaba dentro de la causa de un hueco que se
        le habia dado. Citar lo que se leyo es lo que B3 pide, no lo que
        prohibe. El ejemplo sigue al fixture: cita el REMEDIO del hueco, que
        viaja en el material y no es una clave de fuente.
        """
        buena = self._prosa(extra="- Falta revisar. [revisar director.py]\n")
        self.assertEqual([f for f in self.D.gate(buena, self.lista, self.huecos)
                          if f.startswith("B3")], [])

    def test_un_corchete_sin_cerrar_no_inventa_una_cita(self):
        """Medido en una corrida real del cierre.

        El modelo dejo `[loops.db:latidos/afinador` sin cerrar, y el patron se
        trago texto hasta el `]` de otro parrafo: B3 denuncio como fuente
        inventada un trozo de prosa («37 suites confirmadas,
        docs/bandeja_firmas»). No se puede exigir la fuente de algo que el
        modelo no llego a declarar como cita.
        """
        rota = ("## Qué pasó\n- El afinador certificó. [loops.db:latidos/afinador\n"
                "- 37 suites confirmadas. [estado.json:mvp_gate]\n"
                "\n## Qué piensa cada agente\n- guardian: 77. "
                "[loops.db:latidos/guardian]\n"
                "\n## Qué necesita tu firma\n¿Firmas?\n"
                "\n## NO_DATA\n- no existe [bandeja_firmas.md]\n")
        self.assertEqual([f for f in self.D.gate(rota, self.lista, self.huecos)
                          if f.startswith("B3")], [])

    def test_B2_muerde_si_hay_huecos_y_no_se_declaran(self):
        sin = self._prosa().replace("## NO_DATA\n- no existe [bandeja_firmas.md]\n", "")
        self.assertTrue(any(f.startswith("B2")
                            for f in self.D.gate(sin, self.lista, self.huecos)))

    def test_B4_muerde_con_dos_preguntas(self):
        dos = self._prosa(firma="¿Firmas la F1? ¿Y el puerto?")
        self.assertTrue(any(f.startswith("B4")
                            for f in self.D.gate(dos, self.lista, self.huecos)))

    def test_sin_prosa_no_hay_nada_que_juzgar(self):
        """Si el modelo no respondio, el digesto sale con los hechos y ya.
        Juzgar la ausencia como fallo perderia la medida por culpa del adorno."""
        self.assertEqual(self.D.gate(None, self.lista, self.huecos), [])


class ElOjoVivo(unittest.TestCase):
    """V1 del Ojo-Vivo: la topologia y sus fuentes.

    Lo que se prueba aqui NO es que el refugio «se vea bien» -- eso no lo
    puede decir un test. Es que ninguna cifra visible este escrita a mano, que
    ninguna direccion del rack viaje dentro de la pagina y que cada icono que
    se usa exista. Los tres son defectos que se ven identicos a lo correcto
    cuando el rack esta sano, y solo se notan el dia que deja de estarlo.
    """

    VIVO = ("vivo.html", "vivo.css", "vivo.js")
    IPV4 = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
    # Emoji y pictogramas. Un emoji lo dibuja la fuente del sistema: cambia de
    # forma entre maquinas y no obedece a `currentColor`, asi que no puede
    # llevar el color de una tribu. El contrato pide <symbol> del sprite.
    EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2190-\u21FF\u2300-\u27BF"
                       "\uFE0F\u2B00-\u2BFF]")

    def piezas(self):
        for n in self.VIVO:
            yield n, (CONSOLA / n).read_text(encoding="utf-8")

    def test_las_piezas_del_ojo_vivo_estan_servidas(self):
        codigo = (CONSOLA / "ojo.py").read_text(encoding="utf-8")
        for ruta in ("/vivo", "/vivo.html", "/vivo.css", "/vivo.js"):
            with self.subTest(ruta=ruta):
                self.assertIn(f'"{ruta}"', codigo,
                              f"{ruta} no esta en ESTATICOS: el navegador la "
                              "pedira y el Ojo devolvera 404")
        for n in self.VIVO:
            self.assertTrue((CONSOLA / n).exists(), f"falta {n}")

    def test_las_fuentes_del_ojo_vivo_estan_cableadas(self):
        """Cada panel del margen y del centro necesita su endpoint."""
        codigo = (CONSOLA / "ojo.py").read_text(encoding="utf-8")
        js = (CONSOLA / "vivo.js").read_text(encoding="utf-8")
        for api in ("/api/rack", "/api/acta", "/api/fases",
                    "/api/identidad", "/api/companero"):
            with self.subTest(api=api):
                self.assertIn(f'"{api}"', js, f"{api} no se pide desde vivo.js")
                self.assertIn(f'"{api}"', codigo, f"{api} no lo sirve ojo.py")

    def test_el_ojo_vivo_no_escribe_ninguna_cifra_a_mano(self):
        """«Todo numero o fase escrita a mano es defecto del render».

        Tres cosas quedan fuera del barrido, y por motivos distintos:
        el SPRITE (sus coordenadas son geometria, no medidas), los
        COMENTARIOS (no se pintan) y lo marcado como `class="cita"` (una
        referencia a un registro firmado -- «decision 16» -- sigue apuntando
        a lo mismo pase lo que pase en el rack, que es justo lo contrario de
        una medida a mano).
        """
        html = (CONSOLA / "vivo.html").read_text(encoding="utf-8")
        html = re.sub(r"<svg id=\"sprite\".*?</svg>", "", html, flags=re.S)
        html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
        html = re.sub(r'<span class="cita".*?</span>', "", html, flags=re.S)
        sobran = [c for c in re.findall(r"\d{2,}", html) if c != "127"]
        self.assertEqual(
            [], sobran,
            f"vivo.html trae cifras en el marcado: {sobran}. Toda cifra sale "
            "de estado.json, fases.json o identidad_publica.json; una escrita "
            "aqui sigue en verde cuando el rack ya no lo esta.")

    def test_el_ojo_vivo_no_incrusta_direcciones_del_rack(self):
        """D8_JAMAS: la tabla de direcciones de la tailnet no viaja en la pagina.

        Que el Ojo escuche en loopback no basta: una direccion escrita en el
        HTML se copia con un ctrl-C, viaja en una captura de pantalla y acaba
        en un repo publico. La unica direccion admitida es el propio loopback.
        """
        for n, t in self.piezas():
            with self.subTest(fichero=n):
                ajenas = [i for i in self.IPV4.findall(t) if i != "127.0.0.1"]
                self.assertEqual([], ajenas,
                                 f"{n} lleva direcciones del rack: {ajenas}")

    def test_el_ojo_vivo_no_usa_emojis(self):
        for n, t in self.piezas():
            with self.subTest(fichero=n):
                self.assertEqual(
                    [], sorted(set(self.EMOJI.findall(t))),
                    f"{n} usa emojis; el contrato pide <symbol> del sprite")

    def test_cada_icono_usado_existe_en_el_sprite(self):
        """Un <use> a un id que no existe no falla: no pinta nada.

        Ese es el problema. El cuarto sale sin icono, nadie ve un error en la
        consola del navegador y el fallo puede vivir meses en la pantalla.
        """
        html = (CONSOLA / "vivo.html").read_text(encoding="utf-8")
        js = (CONSOLA / "vivo.js").read_text(encoding="utf-8")
        definidos = set(re.findall(r'<symbol id="(i-[\w-]+)"', html))
        usados = set(re.findall(r'href="#(i-[\w-]+)"', html))
        usados |= set(re.findall(r'icono\("(i-[\w-]+)"\)', js))
        usados |= set(re.findall(r'ic: "(i-[\w-]+)"', js))
        self.assertTrue(definidos, "el sprite quedo vacio")
        self.assertEqual(set(), usados - definidos,
                         f"iconos usados y no definidos: {usados - definidos}")

    def test_fases_json_es_salida_y_no_un_fichero_a_mano(self):
        """La tabla `fases` de continuidad.db es la fuente; el JSON, su copia.

        Si el JSON existe tiene que decir de donde salio. Un fases.json sin
        `fuente` es un fichero que alguien escribio a mano, y entonces hay dos
        verdades sobre las fases del proyecto -- que es justo lo que el
        exportador existe para impedir.
        """
        self.assertTrue((RAIZ / "fases.py").exists(),
                        "falta el exportador fases.py")
        j = RAIZ / "fases.json"
        if not j.exists():
            self.skipTest("fases.json es salida; se regenera con fases.py")
        d = json.loads(j.read_text(encoding="utf-8"))
        self.assertIn("continuidad.db", d.get("fuente", ""),
                      "fases.json no declara continuidad.db como fuente")
        self.assertIsInstance(d.get("fases"), list)

    def test_la_identidad_publica_solo_lleva_lo_publico(self):
        """El unico fichero de esta capa pensado para salir a la calle.

        Por eso se comprueba al reves que los demas: no que tenga lo que hace
        falta, sino que NO tenga lo que no debe -- claves, tokens, correos ni
        direcciones del rack.
        """
        j = RAIZ / "identidad_publica.json"
        if not j.exists():
            self.skipTest("identidad_publica.json todavia no existe")
        crudo = j.read_text(encoding="utf-8")
        d = json.loads(crudo)
        self.assertIsInstance(d, dict)
        for prohibido in ("BEGIN ", "PRIVATE KEY", "ssh-ed25519", "token",
                          "password", "secret", "api_key"):
            with self.subTest(prohibido=prohibido):
                self.assertNotIn(prohibido.lower(), crudo.lower(),
                                 f"identidad_publica.json lleva «{prohibido}»")
        ips = [i for i in self.IPV4.findall(crudo) if i != "127.0.0.1"]
        self.assertEqual([], ips, f"lleva direcciones del rack: {ips}")


class OjoVivoV2(unittest.TestCase):
    """V2 · los estados humanos: la MASCARA es el estado, el BORDE la tribu.

    V1 dejo el borde hecho (`.tribu-*`). V2 pone la otra mitad: que se lea de
    un vistazo COMO esta cada agente sin leer una palabra, que es lo que un
    refugio 2D hace y una tabla no.
    """

    def setUp(self):
        self.css = (CONSOLA / "vivo.css").read_text(encoding="utf-8")
        self.js = (CONSOLA / "vivo.js").read_text(encoding="utf-8")
        self.html = (CONSOLA / "vivo.html").read_text(encoding="utf-8")

    def test_las_mascaras_del_sprite_se_usan_de_verdad(self):
        """Estaban dibujadas en el sprite desde V1 y no las pintaba nadie.

        Un `<symbol>` que nadie referencia es peso muerto que ademas MIENTE:
        quien lee el fichero cree que esa pieza esta viva.
        """
        for sym in ("i-mascara-ok", "i-mascara-mal"):
            with self.subTest(symbol=sym):
                self.assertIn(sym, self.html, "el sprite perdio " + sym)
                self.assertIn(sym, self.js, sym + " sigue sin usarse")

    def test_sin_dato_es_sin_mascara_y_en_gris(self):
        """La ausencia de mascara ES el dato: no sabemos como esta.

        Pintar una mascara verde cuando no hay medida seria fabricar salud, y
        una roja seria fabricar averia. La cara vacia y gris no afirma nada.
        """
        self.assertIn("sin-mascara", self.css)
        self.assertIn("grayscale", self.css)
        self.assertIn("sin-mascara", self.js)

    def test_el_anillo_de_seleccion_usa_su_variable(self):
        """`outline 2px var(--sol)` del contrato visual, y `--sol` definida."""
        plano = self.css.replace(" ", "").replace("\n", "")
        self.assertIn("--sol:", plano, "`--sol` no esta definida")
        self.assertIn("outline:2pxsolidvar(--sol)", plano)

    def test_el_bocadillo_de_log_sale_del_latido_medido(self):
        """El bocadillo lleva `nota_latido`, que es lo que el bucle DIJO.

        No se compone una frase a partir del estado: eso seria prosa generada
        sobre un dato, y el Ojo pinta el dato.
        """
        self.assertIn("nota_latido", self.js)
        self.assertIn("bocadillo", self.js)
        self.assertIn("bocadillo", self.css)

    def test_el_borde_de_tribu_sobrevive_a_v2(self):
        """V2 no puede pisar V1: las cuatro tribus siguen en el borde."""
        for t in ("tribu-preceptor", "tribu-hexelion", "tribu-core", "tribu-ojo"):
            with self.subTest(tribu=t):
                self.assertIn("." + t, self.css)

    def test_no_se_pinta_is_active_ni_en_v2(self):
        """Decision 2 del Soberano, y V2 es donde mas facil seria romperla.

        Un agente `Type=oneshot` esta `inactive` entre disparos y ESE es su
        estado sano. Colgar la mascara de la actividad del timer fabricaria un
        rojo cada vez que el bucle NO esta corriendo, que es casi siempre.
        """
        # Cuarta vez en dos sesiones que un test se tropieza con la cita de
        # un comentario: `vivo.js` EXPLICA por que no pinta `is-active`, y esa
        # explicacion lo nombra. Se mide el codigo.
        codigo = re.sub(r"/\*.*?\*/", "", self.js, flags=re.S)
        codigo = re.sub(r"(?m)//.*$", "", codigo)
        self.assertNotIn("is-active", codigo)


class OjoVivoV3(unittest.TestCase):
    """V3 · el MOBILIARIO es la ubicacion: cada bucle se pinta donde esta.

    V1 puso el borde (tribu), V2 la mascara (estado). V3 mueve: un bucle que
    espera su cita se dibuja en la cama; uno que se paso la hora, congelado.
    """

    def setUp(self):
        self.css = (CONSOLA / "vivo.css").read_text(encoding="utf-8")
        self.js = (CONSOLA / "vivo.js").read_text(encoding="utf-8")
        self.html = (CONSOLA / "vivo.html").read_text(encoding="utf-8")
        self.codigo = re.sub(r"/\*.*?\*/", "", self.js, flags=re.S)
        self.codigo = re.sub(r"(?m)//.*$", "", self.codigo)

    def test_la_cita_se_juzga_contra_la_MEDIDA_y_no_contra_el_reloj(self):
        """El error de los cuatro rojos que no existian, otra vez a la puerta.

        `estado.json` puede tener horas de antiguedad --ahora mismo 35-- y sus
        `proxima` quedan atras solo porque nadie ha vuelto a medir. Comparar
        contra `Date.now()` marcaria TODOS los bucles como congelados y la
        averia seria de la medicion, no del rack. Se compara contra `epoch`,
        que es el instante en que se midio.
        """
        self.assertIn("epoch", self.codigo,
                      "V3 no usa el instante de la medida")
        self.assertNotIn("Date.now()", self.codigo,
                         "V3 juzga contra el reloj de pared: fabricara "
                         "congelados que son antiguedad del snapshot")

    def test_las_dos_anclas_observables_existen_y_se_usan(self):
        for sym in ("i-cama", "i-hielo"):
            with self.subTest(symbol=sym):
                self.assertIn(sym, self.html, "el sprite no trae " + sym)
                self.assertIn(sym, self.codigo, sym + " esta dibujado y no se usa")

    def test_trabajando_no_se_finge(self):
        """`busy` no es observable con lo que la API da hoy.

        Un bucle `Type=oneshot` corre en segundos y la consola sondea cada
        pocos: no hay campo que diga «esta corriendo ahora». Inventar esa
        ubicacion seria pintar un movimiento que nadie midio. El ancla se
        declara y se deja vacia, con su causa.
        """
        self.assertIn("NO_OBSERVABLE", self.js,
                      "el ancla de trabajo no se declara como no observable")

    def test_el_movimiento_respeta_a_quien_pide_quietud(self):
        """Mover sprites es movimiento, y hay quien no puede con el."""
        self.assertIn("prefers-reduced-motion", self.css)

    def test_ninguna_ubicacion_esta_escrita_a_mano(self):
        """Cero hardcodeo: la ubicacion sale del dato o no sale."""
        for nombre in ("guardian", "curador", "afinador"):
            with self.subTest(bucle=nombre):
                self.assertNotIn('"' + nombre + '"', self.codigo,
                                 "hay un bucle nombrado en el codigo: la "
                                 "ubicacion tiene que salir del JSON")


class ElOjoSeComprueba(unittest.TestCase):
    """`ojo.py --check`: decir si el Ojo puede servir, SIN levantarlo.

    Hasta el 2026-08-31 la unica forma de saber si el Ojo estaba entero era
    arrancarlo y pedirle rutas a mano. Eso mezcla dos preguntas --¿estan los
    ficheros? y ¿arranca el servidor?-- y cuando falla no distingue cual de las
    dos fallo. `--check` responde solo la primera, y por eso puede correr en un
    gate sin abrir un puerto.
    """

    def setUp(self):
        self.ojo = CONSOLA / "ojo.py"
        if not self.ojo.exists():
            self.skipTest("no hay ojo.py")

    def _check(self):
        import subprocess
        return subprocess.run([sys.executable, str(self.ojo), "--check"],
                              capture_output=True, text=True, timeout=60)

    def test_check_existe_y_no_abre_puerto(self):
        r = self._check()
        self.assertNotEqual(2, r.returncode,
                            "argparse no conoce --check: " + r.stderr[-200:])

    def test_declara_cada_pieza_de_la_topologia_v1(self):
        """Las tres filas del contrato visual, nombradas una a una.

        Si manana alguien borra `vivo.css`, el Ojo servira un esqueleto sin
        estilo y con 200 en todas las rutas. El unico sitio donde eso se nota
        antes de verlo con los ojos es aqui.
        """
        r = self._check()
        for pieza in ("vivo.html", "vivo.css", "vivo.js"):
            with self.subTest(pieza=pieza):
                self.assertIn(pieza, r.stdout)

    def test_lo_que_falta_sale_declarado_y_el_codigo_lo_dice(self):
        """Sin fuentes, NO_DATA con causa; y el codigo de salida lo repite."""
        r = self._check()
        self.assertRegex(r.stdout, r"MEDIDO|NO_DATA")
        self.assertIn(r.returncode, (0, 1),
                      "un --check solo puede decir sirve (0) o no sirve (1)")


class ElGlosario(unittest.TestCase):

    def test_cada_entrada_declara_su_fuente(self):
        ruta = CONSOLA / "glosario.json"
        if not ruta.exists():
            self.skipTest("todavia no hay glosario")
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        for e in datos["entradas"]:
            with self.subTest(termino=e.get("termino")):
                for campo in ("termino", "que_hace", "donde_verlo", "fuente"):
                    self.assertTrue(e.get(campo),
                                    f"falta `{campo}`: sin fuente es prosa inventada")

    def test_dead_path_esta_retirado_y_no_se_busca(self):
        """Retirado por el Soberano el 2026-08-31. F1 no se construye.

        Mientras `digesto.py` lo tuviera en su lista de fuentes, el hueco se
        reportaba en CADA digesto -- once veces en el historial de un solo dia--
        con el mismo remedio: «construir F1, o retirarlo de la lista». Se
        eligio retirarlo. Un hueco que se declara para siempre y que nadie va a
        tapar deja de ser un sensor honesto y pasa a ser ruido: entrena a quien
        lee el informe a saltarse la seccion NO_DATA, que es justo la que
        importa.

        Este test existe para que no vuelva por la puerta de atras: si alguien
        reintroduce la constante, el gate lo dice antes que el digesto numero
        doce.
        """
        # Se mide el CODIGO, no los comentarios: el propio digesto.py explica
        # en prosa por que se retiro, y esa explicacion nombra lo retirado.
        # Es la tercera vez en esta sesion que un test se tropieza con la cita
        # que hay dentro de un comentario; la cura ya esta establecida.
        crudo = (RAIZ / "digesto" / "digesto.py").read_text(encoding="utf-8")
        codigo = re.sub(r'\"\"\".*?\"\"\"', "", crudo, flags=re.S)
        codigo = re.sub(r"(?m)#.*$", "", codigo)
        self.assertNotIn("DEAD_PATH", codigo,
                         "digesto.py vuelve a buscar dead_path.jsonl")
        self.assertNotIn("dead_path", codigo,
                         "queda una referencia viva a dead_path en digesto.py")
        glos = json.loads((CONSOLA / "glosario.json").read_text(encoding="utf-8"))
        terminos = {e.get("termino") for e in glos["entradas"]}
        self.assertNotIn("dead_path", terminos,
                         "el glosario sigue declarando un concepto retirado")
        # Y la retirada no puede vaciar la seccion: si se queda sin NO_DATA,
        # el test de al lado dejaria de vigilar nada.
        sin_dato = [e for e in glos["entradas"] if e.get("estado") == "NO_DATA"]
        self.assertGreaterEqual(len(sin_dato), 2,
                                "al retirar dead_path el glosario se queda sin "
                                "huecos declarados que vigilar")

    def test_lo_que_no_existe_se_declara_no_data(self):
        """El glosario incluye conceptos NO construidos a proposito.

        El director cronificado y S0 estan especificados y no existen. Un glosario que solo cuenta lo que hay deja creer que lo demas
        funciona -- y son justo las piezas que vigilan a las otras.
        """
        ruta = CONSOLA / "glosario.json"
        if not ruta.exists():
            self.skipTest("todavia no hay glosario")
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        sin_dato = [e for e in datos["entradas"] if e.get("estado") == "NO_DATA"]
        self.assertTrue(sin_dato,
                        "ninguna entrada declara NO_DATA: sospechoso, porque "
                        "hay piezas medidas como no construidas")


class CargarPartida(unittest.TestCase):
    """El save game: los cuatro pilares que una sesion fria da por supuestos.

    Existe por una averia concreta y medida: la Doctrina Caza-Nido llego a
    estar escrita TRES VECES en glosario.json con tres redacciones distintas, y
    nadie lo vio porque el glosario vive plegado al final de la consola. Tres
    verdades sobre el mismo hecho es lo que esta capa entera existe para
    impedir, y se colo en la capa misma.
    """

    def setUp(self):
        self.arranque = json.loads((CONSOLA / "arranque.json").read_text(encoding="utf-8"))
        self.glosario = json.loads((CONSOLA / "glosario.json").read_text(encoding="utf-8"))
        self.plan = self.arranque.get("cargar_partida")

    def _nombres(self):
        p = self.plan
        return (list(p.get("los_cuatro_pilares", []))
                + list(p.get("lo_que_te_va_a_morder", []))
                + list(p.get("y_para_eso_lee", []))
                + [p.get("de_donde_vienes"), p.get("a_donde_vas")])

    def test_el_arranque_declara_la_partida(self):
        self.assertIsInstance(self.plan, dict,
                              "arranque.json no declara `cargar_partida`")
        self.assertEqual(4, len(self.plan.get("los_cuatro_pilares", [])),
                         "los pilares no son cuatro")

    def test_cada_termino_de_la_partida_existe_en_el_glosario(self):
        """Un nombre que no resuelve deja un hueco en la puerta de entrada.

        Y el hueco es silencioso si nadie lo comprueba: la API devuelve
        `{falta: ...}` en su sitio, que se ve -- pero solo si alguien abre la
        pagina. Esto lo cae en el commit que renombra la entrada.
        """
        tiene = {e.get("termino") for e in self.glosario["entradas"]}
        for nombre in self._nombres():
            with self.subTest(termino=nombre):
                self.assertIn(nombre, tiene,
                              f"`{nombre}` esta en arranque.json y no en el glosario")

    def test_el_glosario_no_repite_ningun_termino(self):
        """La averia que origina esta clase, convertida en gate."""
        import collections
        c = collections.Counter(e.get("termino") for e in self.glosario["entradas"])
        repetidos = sorted(k for k, v in c.items() if v > 1)
        self.assertEqual([], repetidos,
                         f"terminos repetidos en el glosario: {repetidos}. "
                         "Dos redacciones del mismo hecho divergen; fundelas.")

    def test_cada_entrada_de_la_partida_ensena_como_verse(self):
        """La regla de esta consola, aplicada a lo que mas se lee.

        «Si no hay comando que lo enseñe, no es conocimiento, es una creencia»
        -- lo dice la entrada del propio glosario. Los pilares son justo lo que
        una sesion va a creerse sin comprobar, asi que aqui no es opcional.
        """
        por_termino = {e.get("termino"): e for e in self.glosario["entradas"]}
        for nombre in self._nombres():
            e = por_termino.get(nombre)
            if e is None:
                continue          # ya lo cae el test de arriba
            with self.subTest(termino=nombre):
                self.assertTrue((e.get("donde_verlo") or "").strip(),
                                f"`{nombre}` no dice donde verlo")
                self.assertTrue((e.get("fuente") or "").strip(),
                                f"`{nombre}` no declara su fuente")

    def test_la_partida_va_la_primera_en_el_arranque(self):
        """Lo que va detras de tres bloques se lee cuando ya se ha decidido."""
        sys.path.insert(0, str(CONSOLA))
        import importlib
        ojo = importlib.import_module("ojo")
        d = ojo.Ojo._arranque()
        claves = [k for k in d if k != "esquema"]
        self.assertEqual("cargar_partida", claves[0],
                         f"la partida no es lo primero: {claves}")

    def test_un_pilar_que_falta_sale_como_hueco_y_no_se_filtra(self):
        """El sabotaje: si se filtrara, quedarian tres pilares con cara de cuatro."""
        sys.path.insert(0, str(CONSOLA))
        import importlib
        ojo = importlib.import_module("ojo")
        roto = {"cargar_partida": {"los_cuatro_pilares": ["no existe esta entrada"],
                                   "de_donde_vienes": None, "a_donde_vas": None,
                                   "lo_que_te_va_a_morder": []}}
        p = ojo.Ojo._partida(roto, self.glosario)
        self.assertEqual(1, len(p["los_cuatro_pilares"]),
                         "el pilar que falta desaparecio de la lista")
        hueco = p["los_cuatro_pilares"][0]
        self.assertEqual("no existe esta entrada", hueco.get("falta"))
        self.assertTrue(hueco.get("causa"), "el hueco no dice por que")
        self.assertTrue(hueco.get("remedio"), "el hueco no dice como arreglarlo")

    def test_la_partida_no_escribe_doctrina_a_mano(self):
        """Ni el render ni el HTML pueden repetir el texto del glosario.

        Si lo repitieran serian la cuarta copia de la Doctrina Caza-Nido, y la
        que nadie mira cuando cambia. Se comprueba buscando trozos LARGOS y
        caracteristicos de los pilares dentro de los ficheros que los pintan.
        """
        por_termino = {e.get("termino"): e for e in self.glosario["entradas"]}
        fuentes = {n: (CONSOLA / n).read_text(encoding="utf-8")
                   for n in ("partida.js", "ojo.html")}
        for nombre in self.plan.get("los_cuatro_pilares", []):
            e = por_termino.get(nombre) or {}
            trozo = (e.get("que_hace") or "")[:60].strip()
            if not trozo:
                continue
            for fichero, texto in fuentes.items():
                with self.subTest(termino=nombre, fichero=fichero):
                    self.assertNotIn(trozo, texto,
                                     f"{fichero} copia el texto de `{nombre}`")

    def test_la_pagina_carga_el_render_de_la_partida(self):
        """Un <section> sin su script es un hueco que dice «…» para siempre."""
        html = (CONSOLA / "ojo.html").read_text(encoding="utf-8")
        self.assertIn('id="partida-cuerpo"', html, "falta el hueco de la partida")
        self.assertIn('src="/partida.js"', html, "la pagina no carga partida.js")
        self.assertTrue((CONSOLA / "partida.js").is_file(), "falta partida.js")
        ojo_py = (CONSOLA / "ojo.py").read_text(encoding="utf-8")
        self.assertIn('"/partida.js"', ojo_py, "el servidor no sirve partida.js")


class ElOjoNoSirveDatoRancioComoActual(unittest.TestCase):
    """El fallo del 2026-09-01, convertido en gate.

    `estado.json` declaraba ocho modelos y `ollama list` daba dos: la lectura
    tenia 37 horas y se servia como si fuera de ahora. Sobre ese dato viejo, la
    web publica llego a declarar servido un adaptador que ya no existia. Un
    dato viejo presentado como actual es peor que un hueco declarado.
    """

    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent / "ojo"))
        import ojo
        self.ojo = ojo

    def test_los_modelos_se_leen_en_vivo_y_por_loopback(self):
        """En vivo, y sin salir de la maquina."""
        self.assertTrue(hasattr(self.ojo.Ojo, "_modelos_vivos"),
                        "el Ojo no sabe leer los modelos en vivo")
        self.assertTrue(self.ojo.OLLAMA.startswith("http://127.0.0.1"),
                        "la consola pregunta por la red en vez de por loopback")
        fuente = inspect.getsource(self.ojo.Ojo._modelos_vivos)
        # Un timeout corto es lo que separa «leer un servicio local» de
        # «colgar la consola justo cuando el rack cae», que es lo que la regla
        # «no mide, pinta» existe para impedir.
        self.assertIn("timeout=", fuente, "sonda sin timeout: puede colgar la consola")
        self.assertIn("NO_DATA", fuente, "no declara la causa cuando no puede leer")

    def test_un_snapshot_viejo_se_declara_rancio(self):
        """La edad se dice con una palabra, no solo con un entero de seis cifras."""
        self.assertLessEqual(self.ojo.RANCIO_S, 3600,
                             "el umbral de rancio es demasiado generoso")
        fuente = inspect.getsource(self.ojo.Ojo.do_GET)
        self.assertIn("RANCIO", fuente, "la respuesta no etiqueta la frescura")
        self.assertIn("ollama_vivo", fuente,
                      "los modelos en vivo no llegan a /api/rack")

    def test_el_vivo_no_pisa_el_snapshot(self):
        """Dos hechos distintos, dos claves distintas.

        Escribir los modelos de ahora dentro de `componentes.ollama` borraria
        la prueba de que el snapshot esta viejo, que es justo el dato que hace
        falta para no volver a fiarse de el.
        """
        fuente = inspect.getsource(self.ojo.Ojo.do_GET)
        self.assertNotIn('componentes"]["ollama', fuente,
                         "el dato en vivo pisa el snapshot")


class ElVectorDeEstadoSoberano(unittest.TestCase):
    """El vector que se inyecta antes del prompt: que no pueda mentir por forma.

    Casi todo se prueba con `sin_red=True`. No es por ir deprisa: un gate que
    sale a la LAN mide la LAN, no el codigo, y se pone rojo el dia que un
    enchufe esta apagado -- que es justo el dia en que el vector funciona BIEN,
    declarando el hueco. El camino con red se cubre con `vector_ejemplo.json`,
    que se genero contra el rack de verdad y viaja en el repo.
    """

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(Path(__file__).resolve().parent / "ojo"))
        import vector
        cls.V = vector
        cls.v = vector.construir(sin_red=True)
        cls.ejemplo = json.loads(
            (RAIZ / "ojo" / "vector_ejemplo.json").read_text(encoding="utf-8"))

    def _lecturas(self, v):
        """Toda hoja del vector, con su ruta. Una hoja es lo que tiene `clave`."""
        fuera = []
        def anda(d, ruta=""):
            if isinstance(d, dict) and "clave" in d and "estado" in d:
                fuera.append((ruta, d))
            elif isinstance(d, dict):
                for k, x in d.items():
                    anda(x, f"{ruta}.{k}" if ruta else k)
        for k in ("salud_hardware", "instantanea_ambiental", "estado_ecosistema",
                  "contexto_usuario"):
            anda(v[k], k)
        return fuera

    def test_valida_contra_su_esquema(self):
        self.assertEqual(self.V.validar(self.v), [])

    def test_el_ejemplo_que_viaja_en_el_repo_tambien_valida(self):
        """Si el ejemplo se queda viejo respecto al esquema, se entera el gate."""
        self.assertEqual(self.V.validar(self.ejemplo), [])

    def test_valor_nulo_si_y_solo_si_no_data(self):
        """La invariante entera, en las dos direcciones y sobre datos reales."""
        for ruta, d in self._lecturas(self.v) + self._lecturas(self.ejemplo):
            with self.subTest(lectura=ruta):
                if d["estado"] == "NO_DATA":
                    self.assertIsNone(d["valor"], "un hueco con valor no es un hueco")
                else:
                    self.assertIsNotNone(d["valor"], "un dato sin valor no es un dato")

    def test_el_esquema_caza_el_cero_decorativo(self):
        """Un validador que nunca dijo que no, no prueba nada."""
        import copy
        malo = copy.deepcopy(self.v)
        malo["instantanea_ambiental"]["co2_ppm"]["valor"] = 0
        self.assertTrue(self.V.validar(malo),
                        "el esquema deja colar un 0 donde no hay dato")

    def test_todo_hueco_trae_causa_y_toda_lectura_su_procedencia(self):
        for ruta, d in self._lecturas(self.v) + self._lecturas(self.ejemplo):
            with self.subTest(lectura=ruta):
                self.assertTrue(d["fuente"], "un dato sin procedencia no se audita")
                self.assertTrue(d["medido"], "una cifra sin su hora es un rumor")
                if d["estado"] == "NO_DATA":
                    self.assertTrue(d.get("causa"), "un hueco sin causa es una excusa")

    def test_ninguna_causa_dice_desconocido(self):
        """La misma metrica de honestidad que el Nexo, aplicada aqui.

        `detalle` SI puede traer el nombre de la excepcion: para eso existe.
        """
        for ruta, d in self._lecturas(self.v) + self._lecturas(self.ejemplo):
            causa = (d.get("causa") or "").lower()
            with self.subTest(lectura=ruta):
                for vacia in ("unknown", "desconocido", "n/a", "error", "???"):
                    self.assertNotIn(vacia, causa)

    def test_sin_red_no_deja_ni_una_sonda(self):
        """La bandera no es un adorno: si se cuela una salida, aqui se ve."""
        self.assertEqual(self.v["presupuesto"]["sondas"], [])
        self.assertTrue(self.v["presupuesto"]["sin_red"])

    def test_la_generacion_solar_jamas_se_alimenta_del_vatimetro(self):
        """El invariante doctrinal del vector, y el motivo de que exista.

        El enchufe mide lo que se GASTA. Si algun dia alguien conecta esa cifra
        a `generacion_solar_w`, una declaracion se habra convertido en una
        medida y la regla «si solar > consumo, lanza tarea pesada» empezara a
        contestar con un numero inventado.
        """
        gen = self.ejemplo["instantanea_ambiental"]["generacion_solar_w"]
        self.assertEqual(gen["estado"], "NO_DATA")
        self.assertIn("gasta", gen["causa"].lower())
        fuente = inspect.getsource(self.V._ambiental)
        self.assertNotIn("_consumo_w()", fuente.split("generacion_solar_w")[1],
                         "el vatimetro esta alimentando la generacion")

    def test_el_mapa_entre_las_dos_lenguas_es_total(self):
        """Ningun estado del vector puede quedarse sin palabra en el Alfabeto."""
        esquema = json.loads(
            (RAIZ / "ojo" / "esquema_vector.json").read_text(encoding="utf-8"))
        estados = set(esquema["$defs"]["lectura"]["properties"]["estado"]["enum"])
        self.assertEqual(estados, set(self.V.A_ALFABETO),
                         "el esquema y la tabla de traduccion se han bifurcado")
        self.assertEqual(set(self.V.A_ALFABETO.values()) - {"ok"},
                         {"sin_dato", "stale"},
                         "una palabra que no esta en el lexico canonico §2")

    def test_norma_no_se_confunde_con_medido_al_cruzar_al_alfabeto(self):
        """`NORMA` traduce a `ok` porque el lexico §2 no tiene palabra para
        «declarado pero no medido». La distincion se conserva en `norma: true`
        en vez de perderse en la traduccion."""
        sobre = self.V.a_alfabeto(self.v)
        idioma = sobre["in"]["contexto_usuario"]["idioma"]
        self.assertEqual(idioma["e"], "ok")
        self.assertTrue(idioma.get("norma"), "la distincion se perdio en el cable")

    def test_el_cable_pesa_bastante_menos_que_la_prosa(self):
        """Alfabeto §6 exige >=30% de ahorro. El A/B en tokens medidos vive en
        `mente/telemetria/lengua.jsonl`; aqui se vigila que no se degrade."""
        prosa = json.dumps(self.ejemplo, ensure_ascii=False, indent=1)
        cable = json.dumps(self.V.a_alfabeto(self.ejemplo), ensure_ascii=False,
                           separators=(",", ":"))
        self.assertLess(len(cable), len(prosa) * 0.7)

    def test_construir_el_vector_no_llama_a_github(self):
        """La lista de repos sale de cache. Preguntarle a la nube en el arranque
        de cada consulta seria pagar latencia y dependencia en el sistema que
        existe para no tenerlas."""
        for fn in (self.V.construir, self.V._ecosistema):
            self.assertNotIn("subprocess", inspect.getsource(fn))
        self.assertIn("subprocess", inspect.getsource(self.V.refrescar_repos))


if __name__ == "__main__":
    unittest.main(verbosity=1)
