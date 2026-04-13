"""
hubspot_sync.py
---------------
Sincroniza datos de HubSpot CRM al repositorio para que el sistema
de LinkedIn posts siempre tenga contexto actualizado sobre:

  - deals/          → eventos cotizados, confirmados y realizados
  - companies/      → clientes y prospectos
  - contacts/       → contactos clave (RRHH leads, decisores)
  - context.md      → resumen legible por Claude en cada sesión

Configuración:
  Crear un Private App en HubSpot:
  HubSpot → Configuración → Integraciones → Private Apps → Crear
  Scopes requeridos: crm.objects.deals.read, crm.objects.companies.read,
                     crm.objects.contacts.read, crm.schemas.deals.read

  Luego setear la variable de entorno:
    export HUBSPOT_API_KEY="pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

  O crear el archivo .env en la raíz del repo:
    HUBSPOT_API_KEY=pat-na1-...

Uso:
    python scripts/hubspot_sync.py
    python scripts/hubspot_sync.py --days 90   # solo deals de los últimos 90 días
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "hubspot"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HUBSPOT_API_BASE = "https://api.hubapi.com"

# Deal stages — personalizar según el pipeline de Celsux en HubSpot
# Ir a HubSpot → CRM → Negocios → editar pipeline para ver los IDs exactos
STAGE_LABELS = {
    "appointmentscheduled": "Reunión agendada",
    "qualifiedtobuy":       "Calificado",
    "presentationscheduled": "Cotización enviada",
    "decisionmakerboughtin": "En negociación",
    "contractsent":          "Propuesta firmada",
    "closedwon":             "Evento confirmado / realizado",
    "closedlost":            "Perdido",
}

# Propiedades a traer de cada objeto
DEAL_PROPERTIES = [
    "dealname", "dealstage", "amount", "closedate", "createdate",
    "description", "hs_deal_stage_probability",
    # Propiedades custom de Celsux — agregar las que uses en HubSpot:
    "tipo_de_evento",        # ej: Team Building, Outdoor, Gala, etc.
    "cantidad_participantes",
    "ciudad_evento",
    "nombre_actividad",      # ej: Roller Coaster, Amazing Race, etc.
]

COMPANY_PROPERTIES = [
    "name", "industry", "city", "country", "numberofemployees",
    "phone", "website", "description", "hs_lead_status",
    "annualrevenue",
]

CONTACT_PROPERTIES = [
    "firstname", "lastname", "email", "jobtitle", "phone",
    "hs_lead_status", "lifecyclestage",
]

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def get_headers() -> dict:
    api_key = os.environ.get("HUBSPOT_API_KEY")
    if not api_key:
        # Try .env file
        env_path = BASE_DIR / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("HUBSPOT_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        print("ERROR: HUBSPOT_API_KEY no está configurada.")
        print("Crear un Private App en HubSpot y setear:")
        print("  export HUBSPOT_API_KEY='pat-na1-...'")
        sys.exit(1)
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def paginate(url: str, params: dict, headers: dict) -> list:
    """Paginate through all HubSpot CRM results."""
    results = []
    after = None
    while True:
        if after:
            params["after"] = after
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("results", []))
        paging = data.get("paging", {})
        after = paging.get("next", {}).get("after")
        if not after:
            break
    return results


def search_objects(object_type: str, filters: list, properties: list, headers: dict) -> list:
    """Use HubSpot search API for filtered queries."""
    url = f"{HUBSPOT_API_BASE}/crm/v3/objects/{object_type}/search"
    payload = {
        "filterGroups": [{"filters": filters}],
        "properties": properties,
        "limit": 100,
    }
    results = []
    after = None
    while True:
        if after:
            payload["after"] = after
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("results", []))
        paging = data.get("paging", {})
        after = paging.get("next", {}).get("after")
        if not after:
            break
    return results


# ---------------------------------------------------------------------------
# Fetchers
# ---------------------------------------------------------------------------

def fetch_deals(headers: dict, days_back: int = 365) -> list:
    """Fetch all deals created or closed in the last N days."""
    print(f"  Trayendo deals (últimos {days_back} días)...")
    since = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y-%m-%dT00:00:00Z")

    filters = [
        {
            "propertyName": "createdate",
            "operator": "GTE",
            "value": since,
        }
    ]

    raw = search_objects("deals", filters, DEAL_PROPERTIES, headers)

    deals = []
    for item in raw:
        props = item.get("properties", {})
        stage_id = props.get("dealstage", "")
        deals.append({
            "id": item["id"],
            "nombre": props.get("dealname", ""),
            "etapa": STAGE_LABELS.get(stage_id, stage_id),
            "etapa_id": stage_id,
            "monto_ars": props.get("amount"),
            "fecha_cierre": props.get("closedate", "")[:10] if props.get("closedate") else None,
            "fecha_creacion": props.get("createdate", "")[:10] if props.get("createdate") else None,
            "descripcion": props.get("description", ""),
            "tipo_evento": props.get("tipo_de_evento", ""),
            "actividad": props.get("nombre_actividad", ""),
            "participantes": props.get("cantidad_participantes", ""),
            "ciudad": props.get("ciudad_evento", ""),
            "companies": [],   # se rellena después con asociaciones
            "contacts": [],
        })

    print(f"    → {len(deals)} deals encontrados")
    return deals


def fetch_companies(headers: dict) -> list:
    """Fetch all companies."""
    print("  Trayendo companies...")
    url = f"{HUBSPOT_API_BASE}/crm/v3/objects/companies"
    params = {
        "properties": ",".join(COMPANY_PROPERTIES),
        "limit": 100,
    }
    raw = paginate(url, params, headers)

    companies = []
    for item in raw:
        props = item.get("properties", {})
        companies.append({
            "id": item["id"],
            "nombre": props.get("name", ""),
            "industria": props.get("industry", ""),
            "ciudad": props.get("city", ""),
            "pais": props.get("country", "Argentina"),
            "empleados": props.get("numberofemployees"),
            "sitio_web": props.get("website", ""),
            "descripcion": props.get("description", ""),
        })

    print(f"    → {len(companies)} empresas encontradas")
    return companies


def fetch_contacts(headers: dict) -> list:
    """Fetch key contacts (RRHH leads and decision makers)."""
    print("  Trayendo contactos clave...")
    # Filter: contacts with relevant job titles
    filters = [
        {
            "propertyName": "jobtitle",
            "operator": "CONTAINS_TOKEN",
            "value": "RRHH",
        }
    ]
    # Also fetch all contacts if filters return nothing
    raw = search_objects("contacts", filters, CONTACT_PROPERTIES, headers)
    if not raw:
        url = f"{HUBSPOT_API_BASE}/crm/v3/objects/contacts"
        params = {"properties": ",".join(CONTACT_PROPERTIES), "limit": 100}
        raw = paginate(url, params, headers)

    contacts = []
    for item in raw:
        props = item.get("properties", {})
        contacts.append({
            "id": item["id"],
            "nombre": f"{props.get('firstname', '')} {props.get('lastname', '')}".strip(),
            "cargo": props.get("jobtitle", ""),
            "email": props.get("email", ""),
            "etapa": props.get("lifecyclestage", ""),
        })

    print(f"    → {len(contacts)} contactos encontrados")
    return contacts


def enrich_deals_with_associations(deals: list, companies: list, contacts: list, headers: dict) -> list:
    """Attach company names and contact names to each deal."""
    if not deals:
        return deals

    print("  Enriqueciendo deals con asociaciones...")
    company_map = {c["id"]: c["nombre"] for c in companies}
    contact_map = {c["id"]: f"{c['nombre']} ({c['cargo']})" for c in contacts}

    deal_ids = [d["id"] for d in deals]

    # Batch association lookup (deals → companies)
    for i in range(0, len(deal_ids), 100):
        batch = deal_ids[i:i+100]
        url = f"{HUBSPOT_API_BASE}/crm/v3/associations/deals/companies/batch/read"
        resp = requests.post(url, json={"inputs": [{"id": d} for d in batch]},
                             headers=headers, timeout=30)
        if resp.ok:
            for result in resp.json().get("results", []):
                from_id = result.get("from", {}).get("id")
                to_ids = [t["id"] for t in result.get("to", [])]
                for deal in deals:
                    if deal["id"] == from_id:
                        deal["companies"] = [company_map.get(cid, cid) for cid in to_ids]

    # Batch association lookup (deals → contacts)
    for i in range(0, len(deal_ids), 100):
        batch = deal_ids[i:i+100]
        url = f"{HUBSPOT_API_BASE}/crm/v3/associations/deals/contacts/batch/read"
        resp = requests.post(url, json={"inputs": [{"id": d} for d in batch]},
                             headers=headers, timeout=30)
        if resp.ok:
            for result in resp.json().get("results", []):
                from_id = result.get("from", {}).get("id")
                to_ids = [t["id"] for t in result.get("to", [])]
                for deal in deals:
                    if deal["id"] == from_id:
                        deal["contacts"] = [contact_map.get(cid, cid) for cid in to_ids]

    return deals


# ---------------------------------------------------------------------------
# Context file generator
# ---------------------------------------------------------------------------

def build_context_md(deals: list, companies: list) -> str:
    """
    Generates a Markdown summary readable by Claude in every session.
    Kept concise — this is injected as context, not stored as a database.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Split deals by stage
    pipeline = [d for d in deals if d["etapa_id"] not in ("closedwon", "closedlost")]
    won      = [d for d in deals if d["etapa_id"] == "closedwon"]
    lost     = [d for d in deals if d["etapa_id"] == "closedlost"]

    lines = [
        f"# Contexto HubSpot — Celsux",
        f"_Última sincronización: {now} (America/Buenos_Aires)_",
        "",
        "---",
        "",
        f"## Pipeline activo — {len(pipeline)} negocios en curso",
        "",
    ]

    if pipeline:
        for d in sorted(pipeline, key=lambda x: x.get("fecha_cierre") or "", reverse=True):
            empresa = ", ".join(d["companies"]) or "Empresa sin asignar"
            tipo = f" · {d['actividad'] or d['tipo_evento']}" if (d['actividad'] or d['tipo_evento']) else ""
            fecha = f" · Cierre estimado: {d['fecha_cierre']}" if d['fecha_cierre'] else ""
            pax = f" · {d['participantes']} personas" if d['participantes'] else ""
            ciudad = f" · {d['ciudad']}" if d['ciudad'] else ""
            lines.append(f"- **{empresa}** — {d['nombre']}{tipo}{fecha}{pax}{ciudad}")
            lines.append(f"  Etapa: {d['etapa']}")
    else:
        lines.append("_(Sin negocios activos en el rango de fechas)_")

    lines += [
        "",
        "---",
        "",
        f"## Eventos realizados (Closed Won) — {len(won)} total",
        "",
    ]

    if won:
        for d in sorted(won, key=lambda x: x.get("fecha_cierre") or "", reverse=True)[:20]:
            empresa = ", ".join(d["companies"]) or "Empresa sin asignar"
            tipo = f" · {d['actividad'] or d['tipo_evento']}" if (d['actividad'] or d['tipo_evento']) else ""
            fecha = f" · {d['fecha_cierre']}" if d['fecha_cierre'] else ""
            pax = f" · {d['participantes']} personas" if d['participantes'] else ""
            ciudad = f" · {d['ciudad']}" if d['ciudad'] else ""
            lines.append(f"- **{empresa}**{tipo}{fecha}{pax}{ciudad}")
    else:
        lines.append("_(Sin eventos cerrados en el rango de fechas)_")

    lines += [
        "",
        "---",
        "",
        f"## Clientes / Empresas — {len(companies)} en CRM",
        "",
    ]

    if companies:
        for c in companies[:30]:
            industria = f" · {c['industria']}" if c['industria'] else ""
            empleados = f" · {c['empleados']} empleados" if c['empleados'] else ""
            lines.append(f"- **{c['nombre']}**{industria}{empleados}")
    else:
        lines.append("_(Sin empresas en CRM)_")

    lines += [
        "",
        "---",
        "",
        "## Cómo usar este contexto",
        "",
        "- Al redactar un post sobre un cliente, buscá su nombre arriba para tener datos específicos (tipo de actividad, participantes, ciudad).",
        "- Los negocios en pipeline son oportunidades de contenido: un post sobre el tipo de evento puede acelerar la decisión de un prospecto.",
        "- Los Closed Won son historias reales disponibles para posts de caso de éxito.",
        "- Nunca incluyas montos, etapas del pipeline ni datos confidenciales en posts públicos.",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sincroniza HubSpot CRM con el repo de LinkedIn posts")
    parser.add_argument("--days", type=int, default=365, help="Días hacia atrás para traer deals (default: 365)")
    args = parser.parse_args()

    print("=== Sincronizando HubSpot → linkedin-posts ===")
    headers = get_headers()

    # Fetch
    companies = fetch_companies(headers)
    contacts  = fetch_contacts(headers)
    deals     = fetch_deals(headers, days_back=args.days)
    deals     = enrich_deals_with_associations(deals, companies, contacts, headers)

    # Save JSON files
    (DATA_DIR / "deals.json").write_text(
        json.dumps(deals, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (DATA_DIR / "companies.json").write_text(
        json.dumps(companies, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (DATA_DIR / "contacts.json").write_text(
        json.dumps(contacts, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Build and save human-readable context for Claude
    context_md = build_context_md(deals, companies)
    context_path = DATA_DIR / "context.md"
    context_path.write_text(context_md, encoding="utf-8")

    print(f"\n✓ Guardado en {DATA_DIR}/")
    print(f"  deals.json     → {len(deals)} negocios")
    print(f"  companies.json → {len(companies)} empresas")
    print(f"  contacts.json  → {len(contacts)} contactos")
    print(f"  context.md     → listo para Claude")
    print("\nPróximo paso: commitear el context.md al repo para que")
    print("el session-start hook lo muestre en cada sesión.")


if __name__ == "__main__":
    main()
