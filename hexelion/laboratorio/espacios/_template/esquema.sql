-- Esquema de un espacio aislado. Se copia, no se inventa.
--
-- POR QUE UN .sql Y NO UN .db VACIO EN GIT. Una base de datos es DATO, y el dato
-- soberano no se versiona (es la misma regla que puso `*.db` en el .gitignore de
-- `preceptor` el 2026-09-12). Un .db en la historia ademas no se audita leyendolo.
-- El esquema si es codigo: se lee, se revisa en un diff, y `init.sh` lo aplica.

-- El canal del espacio. Espeja `~/.preceptoros/conversaciones.db` a proposito:
-- los datos se COPIAN desde ahi, y una columna que no case rompe la copia.
CREATE TABLE IF NOT EXISTS conversaciones (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp       TEXT NOT NULL,
  model_used      TEXT NOT NULL,
  user_prompt     TEXT NOT NULL,
  model_response  TEXT NOT NULL,
  -- Firma Ed25519 de quien hablo. MEDIDO 2026-09-12: las 6 conversaciones del
  -- canal global lo tienen VACIO. El flujo promete que todo se firma y hoy no se
  -- firma nada: la columna se reserva y el gate PUBLICA el recuento de huecos.
  -- Un dato incomodo no se borra, se ensena.
  user_hash       TEXT,
  session_id      TEXT,
  revisada        INTEGER NOT NULL DEFAULT 0,
  -- De donde vino el turno. Hoy 'web'; manana 'shelly', 'esp32', 'sdr'.
  -- Existe desde el dia uno para que una fila de telemetria entre por el mismo
  -- canal sin tocar el bucle: cambia el `fuente`, no el harness.
  fuente          TEXT,
  -- El Arnes Doble. 5 tok/s locales y 100 de frontera en la misma tabla no son
  -- una media: son dos poblaciones, y mezclarlas contamina las dos.
  arnes           TEXT CHECK (arnes IN ('web','app','externo') OR arnes IS NULL)
);

CREATE VIRTUAL TABLE IF NOT EXISTS conversaciones_fts
  USING fts5(user_prompt, model_response, content='conversaciones', content_rowid='id');

CREATE TRIGGER IF NOT EXISTS conversaciones_fts_ai AFTER INSERT ON conversaciones BEGIN
  INSERT INTO conversaciones_fts(rowid, user_prompt, model_response)
  VALUES (new.id, new.user_prompt, new.model_response);
END;
CREATE TRIGGER IF NOT EXISTS conversaciones_fts_ad AFTER DELETE ON conversaciones BEGIN
  INSERT INTO conversaciones_fts(conversaciones_fts, rowid, user_prompt, model_response)
  VALUES ('delete', old.id, old.user_prompt, old.model_response);
END;

-- Los veredictos del juez-ensamble. Uno por vuelta, no solo el ultimo: una nota
-- que sube de 5 a 9 en tres vueltas cuenta una historia que el 9 solo no cuenta.
CREATE TABLE IF NOT EXISTS veredictos (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  conversacion_id INTEGER NOT NULL,
  vuelta          INTEGER NOT NULL,
  capa1_pasa      INTEGER NOT NULL,      -- critico determinista
  capa2_nota      INTEGER,               -- critico MoE; NULL si la capa 1 corto
  detalle         TEXT NOT NULL,         -- JSON del veredicto
  estado          TEXT NOT NULL CHECK (estado IN ('NO_DATA','rechazado','propuesto')),
  cuando          REAL NOT NULL
);
