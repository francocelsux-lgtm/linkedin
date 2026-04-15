# Claude — Reglas de Comportamiento en este Proyecto

Leer al inicio de cada sesión junto con CLAUDE.md.

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
  - Explorar cómo está estructurado un template antes de modificarlo
  - Investigar competidores en paralelo mientras se redacta un post
  - Analizar el historial de memoria sin traer todo al contexto

## 3. Self-Improvement Loop

- Después de CUALQUIER corrección del usuario: registrar el patrón en `tasks/lessons.md`
- Escribir reglas que prevengan el mismo error en el futuro
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
- Preguntarse: *"¿Un senior engineer aprobaría esto?"*
- En este proyecto: si se modifica un template o archivo de company/, verificar que quedó bien estructurado y es coherente con el resto del sistema

## 5. Elegancia Balanceada

- Para cambios no triviales: pausar y preguntar *"¿hay una forma más elegante?"*
- Saltear esto para fixes simples y obvios — no sobre-ingenierizar
- En este proyecto: un post mal escrito es peor que ningún post — nunca presentar un borrador sin pasar el checklist de voz

## 6. Bug Fixing Autónomo

- Ante un reporte de bug: simplemente arreglarlo, sin pedir orientación
- Ir tras logs, errores y tests que fallan — luego resolverlos
- En este proyecto: si un script falla (hubspot_sync.py, preprocess_posts.py), diagnosticar y corregir directo

---

## Task Management

1. **Primero:** Escribir el plan en `tasks/todo.md` con ítems chequeables
2. **Verificar:** Confirmar el plan antes de empezar la implementación
3. **Trackear:** Marcar ítems como completos a medida que avanzás
4. **Documentar:** Agregar notas a `tasks/lessons.md` después de correcciones

---

## Core Principles

**Simplicity First**
Hacer cada cambio tan simple como sea posible. No tocar lo que no fue pedido.

**No Laziness**
Encontrar causas raíz. Sin fixes temporales. Si algo no está claro, investigar antes de asumir.

**No Implied Intent**
Solo tocar lo necesario. Sin side effects. Si hay duda sobre el alcance de un cambio, preguntar primero.
