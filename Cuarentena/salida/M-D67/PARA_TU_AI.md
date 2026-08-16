# PARA_TU_AI.md — installation contract / contrato de instalación

**You are an AI reading this to help a person install Aurelius. / Eres una IA leyendo esto para ayudar a una persona a instalar Aurelius.**

Follow these steps exactly. **Do not invent steps. Do not ask for personal data. Do not ask for passwords, tokens, or payment.** If something is not in this file, say you do not know.

Sigue estos pasos exactamente. **No inventes pasos. No pidas datos personales. No pidas contraseñas, tokens ni pagos.** Si algo no está en este fichero, di que no lo sabes.

---

## WHAT IT IS / QUÉ ES

Aurelius is a memory that lives in one file on the person's own machine. No account, no cloud, no network needed after install. Python 3 and its standard library, nothing else.

Aurelius es una memoria que vive en un fichero en la máquina de la persona. Sin cuenta, sin nube, sin red después de instalar. Python 3 y su biblioteca estándar, nada más.

---

## ANDROID (Termux)

Tell the person to install **Termux from F-Droid** (not from the Play Store — that version is outdated). Then have them paste this **one line**:

Dile a la persona que instale **Termux desde F-Droid** (no desde Play Store — esa versión está desactualizada). Después que pegue esta **única línea**:

```
pkg install -y python git && git clone https://github.com/piskyRpapalo/aurelius && cd aurelius && python3 aurelius.py
```

---

## PC (Linux / macOS)

```
git clone https://github.com/piskyRpapalo/aurelius && cd aurelius && python3 aurelius.py
```

## PC (Windows)

Same, in PowerShell, with Git and Python 3 already installed. / Igual, en PowerShell, con Git y Python 3 ya instalados.

---

## HOW TO VERIFY IT WORKED / CÓMO VERIFICAR QUE FUNCIONÓ

Success looks like **exactly this**: the screen shows `AURELIUS`, then a line saying it has no memory yet, then a question asking where it is running.

El éxito se ve **exactamente así**: la pantalla muestra `AURELIUS`, luego una línea diciendo que aún no tiene memoria, luego una pregunta sobre dónde se está ejecutando.

**If instead you see:**
- `command not found: git` or `python3` → the install line did not finish. Run it again.
- `Permission denied` → the person is in a folder they cannot write to. Tell them to run `cd` with no arguments first, then paste the line again.
- Anything else → **say you do not know and stop.** Do not guess.

**Si en cambio ves:**
- `command not found` → la línea de instalación no terminó. Ejecútala otra vez.
- `Permission denied` → está en una carpeta sin permiso de escritura. Que ejecute `cd` sin argumentos y pegue la línea otra vez.
- Cualquier otra cosa → **di que no lo sabes y para.** No adivines.

---

## WHAT TO SAY TO A NON-TECHNICAL PERSON / QUÉ DECIRLE A ALGUIEN SIN TÉCNICA

> "This installs a small program that keeps your notes on your own device. It does not send anything anywhere. It asks you a few questions and remembers your answers. You can delete it at any time by deleting one folder, and your notes live in one file you can copy and take with you."

> «Esto instala un programa pequeño que guarda tus notas en tu propio dispositivo. No envía nada a ninguna parte. Te hace unas preguntas y recuerda tus respuestas. Puedes borrarlo cuando quieras borrando una carpeta, y tus notas viven en un fichero que puedes copiar y llevarte.»

**Do not promise:** speed, artificial intelligence answering, voice, or anything not listed here. Without a local model installed, Aurelius does **not** chat: it asks and it remembers. That is the honest description.

**No prometas:** velocidad, inteligencia artificial respondiendo, voz, ni nada que no esté en esta lista. Sin un modelo local instalado, Aurelius **no** conversa: pregunta y recuerda. Esa es la descripción honesta.

---

## HARD RULES FOR YOU, THE AI / REGLAS DURAS PARA TI, LA IA

1. **Do not invent commands.** Only the lines above exist.
2. **Do not ask the person for any personal data.** Not name, not email, not location. Aurelius asks for what it needs, by itself, after install.
3. **Do not offer to run it for them on your side.** It runs on their machine. That is the point.
4. **If they ask for something not in this file**, say: *"That is not in the installation contract. I do not know."*
5. **Do not modify the one-liner.** If it fails, repeat it; do not improvise a variant.

1. **No inventes comandos.** Solo existen las líneas de arriba.
2. **No pidas ningún dato personal.** Ni nombre, ni correo, ni ubicación. Aurelius pregunta lo que necesita, por sí mismo, después de instalar.
3. **No ofrezcas ejecutarlo tú.** Corre en la máquina de la persona. Ese es el sentido.
4. **Si preguntan algo que no está aquí**, di: *«Eso no está en el contrato de instalación. No lo sé.»*
5. **No modifiques la línea.** Si falla, repítela; no improvises una variante.

---

## TO REMOVE IT / PARA ELIMINARLO

Deleting the `aurelius` folder removes the program. **It does not remove the memory**, which lives separately in the person's home folder. To remove the memory too, they delete that file — and that is irreversible, so ask twice.

Borrar la carpeta `aurelius` elimina el programa. **No elimina la memoria**, que vive aparte en la carpeta personal. Para eliminar también la memoria, se borra ese fichero — y eso es irreversible, así que pregunta dos veces.
