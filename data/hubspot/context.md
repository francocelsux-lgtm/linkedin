# Contexto HubSpot — Celsux

_Sin sincronizar aún. Correr `python scripts/hubspot_sync.py` para poblar este archivo._

---

## Cómo configurar la integración

### 1. Crear un Private App en HubSpot

1. Entrar a HubSpot → **Configuración** (ícono de tuerca)
2. Ir a **Integraciones → Private Apps**
3. Clic en **Crear Private App**
4. Nombre: `LinkedIn Posts — Claude`
5. En la pestaña **Scopes**, activar:
   - `crm.objects.deals.read`
   - `crm.objects.companies.read`
   - `crm.objects.contacts.read`
   - `crm.schemas.deals.read`
6. Clic en **Crear app** → copiar el token `pat-na1-...`

### 2. Configurar el token

Opción A — variable de entorno (recomendado):
```bash
export HUBSPOT_API_KEY="pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

Opción B — archivo `.env` en la raíz del repo:
```
HUBSPOT_API_KEY=pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

> El `.env` ya está en `.gitignore` — nunca se sube al repositorio.

### 3. Personalizar etapas del pipeline

Abrir `scripts/hubspot_sync.py` y editar el diccionario `STAGE_LABELS` con los
nombres exactos de las etapas de tu pipeline de Negocios en HubSpot.

Para ver los IDs: HubSpot → CRM → Negocios → Acciones → Editar pipeline.

### 4. Agregar propiedades custom de Celsux

Si usás propiedades custom en tus deals (ej: tipo de evento, cantidad de personas,
nombre de la actividad), agregarlas al array `DEAL_PROPERTIES` en el script.

### 5. Sincronizar

```bash
pip install requests
python scripts/hubspot_sync.py
```

Para sincronizar solo los últimos 90 días:
```bash
python scripts/hubspot_sync.py --days 90
```

---

## Cómo usar este contexto al redactar posts

- Al usar `/draft-post`, el contexto de HubSpot está disponible automáticamente
- Podés referenciar clientes del pipeline como "una empresa que estamos cotizando"  
  (sin nombrarla) para crear contenido más relevante al momento
- Los Closed Won son historias reales: pedir permiso al cliente antes de nombrarlo
- Nunca incluir montos, etapas internas ni datos confidenciales en posts públicos
