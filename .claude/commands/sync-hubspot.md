# /sync-hubspot

Sincroniza el CRM de HubSpot con el repositorio. Actualiza deals, companies, contactos y genera el archivo `data/hubspot/context.md` que Claude lee en cada sesión.

## Cuándo usar

- Al inicio de cada semana (o antes de redactar posts sobre clientes)
- Después de cerrar un evento importante (Closed Won)
- Cuando hay un prospecto nuevo en pipeline relevante para contenido

## Uso

```
/sync-hubspot
/sync-hubspot --days 90   ← solo últimos 90 días
```

---

## Qué hace

1. **Verifica** que `HUBSPOT_API_KEY` esté configurada
2. **Trae** de HubSpot:
   - Todos los deals (negocios) del período
   - Todas las empresas del CRM
   - Contactos clave (RRHH y decisores)
3. **Enriquece** cada deal con empresa y contacto asociado
4. **Genera** `data/hubspot/context.md` — resumen legible con:
   - Pipeline activo (eventos en cotización/negociación)
   - Closed Won (eventos realizados, con tipo y participantes)
   - Lista de clientes
5. **Guarda** los JSON crudos en `data/hubspot/`

## Ejecutar

```bash
python scripts/hubspot_sync.py
```

Si no tenés el token configurado todavía:

```
Crear Private App en HubSpot:
  Configuración → Integraciones → Private Apps → Crear
  Scopes: crm.objects.deals.read, crm.objects.companies.read,
          crm.objects.contacts.read, crm.schemas.deals.read

Luego:
  export HUBSPOT_API_KEY="pat-na1-..."
```

Ver instrucciones completas en `data/hubspot/context.md`.

---

## Después de sincronizar

El archivo `data/hubspot/context.md` se actualiza automáticamente.
El session-start hook lo leerá en la próxima sesión.

Para que quede disponible también en el repositorio remoto:
```bash
git add data/hubspot/context.md
git commit -m "sync: actualizar contexto HubSpot"
git push
```

> Los archivos `deals.json`, `companies.json` y `contacts.json` están en `.gitignore`
> por privacidad. Solo `context.md` (el resumen sin datos sensibles) se commitea.
