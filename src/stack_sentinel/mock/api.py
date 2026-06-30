from fastapi import FastAPI, HTTPException

app = FastAPI(title="stack-sentinel-mock")

TICKETS = {
    "TCK-101": {
        "summary": "Login cai sob carga",
        "severity": "high",
        "service": "auth",
        "status": "open",
    },
}
BUILDS = {
    "BLD-203": {
        "service": "auth",
        "status": "failed",
        "branch": "main",
        "commit": "a1b2c3d",
    },
}
DOCS = {
    "severity-policy": "P1 critico em ate 1h; P2 alto em ate 4h; P3 medio no dia.",
}
HEALTH = {"auth": "degraded", "billing": "ok"}


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    if ticket_id not in TICKETS:
        raise HTTPException(404, "ticket not found")
    return TICKETS[ticket_id]


@app.get("/builds/{build_id}")
def get_build(build_id: str):
    if build_id not in BUILDS:
        raise HTTPException(404, "build not found")
    return BUILDS[build_id]


@app.get("/docs/{slug}")
def get_doc(slug: str):
    if slug not in DOCS:
        raise HTTPException(404, "doc not found")
    return {"slug": slug, "content": DOCS[slug]}


@app.get("/services/{service_name}/health")
def get_health(service_name: str):
    return {"service": service_name, "status": HEALTH.get(service_name, "unknown")}
