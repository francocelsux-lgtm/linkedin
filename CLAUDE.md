# CLAUDE.md — LinkedIn Posts / Celsux

Instrucciones de comportamiento para Claude en este proyecto.
Leer al inicio de cada sesión antes de hacer cualquier cosa.

---

## 1. Plan Mode Default

- Entrar en plan mode para CUALQUIER tarea no trivial (3+ pasos o decisiones de arquitectura)
- Si algo sale mal, PARAR y re-planificar de inmediato — no improvisar
- Usar plan mode también para pasos de verificación, no solo para construir
- Escribir specs detallados antes de implementar para reducir ambigüedad
- En este proyecto: redactar un post, modificar un skill, integrar una fuente de datos → plan primero

## 2. Subagents Strategy

- Usar subagents liberalmente para mantener el contexto principal limpio
- Delegar a subagents: research, exploración del repo, análisis paralelo
- Para problemas complejos: más cómputo vía subagents, no más tokens en el contexto principal
- Una tarea por subagent para ejecución enfocada
- Ejemplos de cuándo usar subagents:
  - Explorar cómo está estructurado un skill antes de modificarlo
  - Investigar competidores en paralelo mientras se redacta un post
  - Analizar el historial de memoria sin traer todo al contexto

## 3. Self-Improvement Loop

- Después de CUALQUIER corrección del usuario: registrar el patrón en `tasks/lessons.md`
- Escribir reglas que prevengan el mismo error en el futuro
- Iterar sin piedad sobre esas lecciones hasta que los errores desaparezcan
- Revisar `tasks/lessons.md` al inicio de cada sesión para contexto relevante del proyecto
- Formato de lección:
  ```
  ## Lección — [fecha]
  Error: [qué salió mal]
  Causa: [por qué pasó]
  Regla: [qué hacer diferente siempre]
  ```

## 4. Verificación Antes de Declarar Listo

- Nunca marcar una tarea como completa sin demostrar que funciona
- Comparar comportamiento: entre antes y después del cambio cuando sea relevante
- Preguntarse: *"¿Un senior engineer aprobaría esto?"*
- Correr tests, revisar logs, demostrar conexiones
- En este proyecto: si se modifica un skill o comando, verificar que el archivo quedó bien estructurado y es coherente con el resto del sistema

## 5. Elegancia Balanceada

- Para cambios no triviales: pausar y preguntar *"¿hay una forma más elegante?"*
- Si se siente hacky: *"Sabiendo todo lo que sé ahora, implementar la solución elegante"*
- Saltear esto para fixes simples y obvios — no sobre-ingenierizar
- Desafiar el propio trabajo antes de presentarlo al usuario
- En este proyecto: un post de LinkedIn mal escrito es peor que ningún post — nunca presentar un borrador sin pasar el checklist de voz y formato

## 6. Bug Fixing Autónomo

- Ante un reporte de bug: simplemente arreglarlo, sin pedir orientación
- Apuntar a logs, errores y tests que fallan — luego resolverlos
- Zero context switching requerido del usuario
- Ir tras tests de CI que fallan sin que te lo pidan
- En este proyecto: si un script falla (hubspot_sync.py, preprocess_posts.py), diagnosticar y corregir directo

---

## Task Management

1. **Primero:** Escribir el plan en `tasks/todo.md` con ítems chequeables
2. **Verificar:** Confirmar el plan antes de empezar la implementación
3. **Trackear:** Marcar ítems como completos a medida que avanzás
4. **Explicar:** Resumen de alto nivel en cada paso importante
5. **Documentar:** Agregar notas a `tasks/lessons.md` después de correcciones
6. **Capturar:** Actualizar `tasks/lessons.md` después de cualquier corrección del usuario

---

## Core Principles

**Simplicity First**
Hacer cada cambio tan simple como sea posible. Impacto mínimo en el código/contenido.
No tocar lo que no fue pedido.

**No Laziness**
Encontrar causas raíz. Sin fixes temporales. Estándares de senior developer.
Si algo no está claro, investigar antes de asumir.

**No Implied Intent**
Solo tocar lo necesario. Sin side effects. Sin bugs nuevos como consecuencia de un fix.
Si hay duda sobre el alcance de un cambio, preguntar primero.

---

## Contexto del Proyecto

Este repo es el sistema de contenido de LinkedIn para **Luis Durruty, CEO de Celsux**.
- Audiencia objetivo: Directores de RRHH, People & Culture leads, CHROs en LATAM
- Idioma principal: Español (algunos posts en inglés)
- Voz: Ver `celsux-voice.md` — directa, opinionada, humana, sin corporativismo
- Workflow completo: Ver `content-research-writer.md`
- Memoria del sistema: Ver `supermemory-skill.md` y carpeta `memory/`
- Contexto CRM: Ver `data/hubspot/context.md` (si está sincronizado)

**Antes de redactar cualquier post:**
1. Leer `celsux-voice.md`
2. Consultar `data/hubspot/context.md` para contexto de clientes
3. Revisar `memory/hook-library.md` para patrones que han funcionado
4. Seguir el workflow de `content-research-writer.md` sin saltear fases

---

## Sistema Outbound Multi-Repo

Este repo forma parte de un workspace de dos repositorios que trabajan juntos:

```
~/celsux/
├── CLAUDE.md                ← workspace-level (copiar desde cold-b2b-emails/workspace/CLAUDE.md)
├── linkedin/                ← ESTE REPO — construye autoridad
└── cold-b2b-emails/         ← convierte autoridad en reuniones
```

**Cómo se conectan:**

| Este repo (LinkedIn) | cold-b2b-emails |
|----------------------|-----------------|
| Construye autoridad y marca | Convierte esa autoridad en reuniones |
| Posts virales → señales de tema | Esos temas → secuencias de email |
| `celsux-voice.md` → fuente de verdad de voz | Heredada por cold emails |
| `profile-analysis.md` → ICP | Mismo ICP, distinto canal |
| `data/hubspot/context.md` → CRM | Compartido con cold emails |

**Regla de dependencia:** Los cambios de voz o ICP van primero en este repo, luego se propagan a `cold-b2b-emails`.

**Coordinación de ramas:** Al trabajar en una feature cross-repo, usar el mismo nombre de rama en ambos:
```bash
git -C linkedin checkout -b feature/nombre
git -C cold-b2b-emails checkout -b feature/nombre

# Ver estado de todos los repos de un vistazo
bash cold-b2b-emails/workspace/status.sh
```
