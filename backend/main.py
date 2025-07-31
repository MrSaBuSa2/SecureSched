import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.db import Base, engine
from src.routers import auth, users as users_router, schedules

# === Logger ===
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

logger.debug("🚀 Démarrage de SecureSched main.py")

# === Chargement des variables d’environnement ===
load_dotenv()
logger.debug("✅ Variables d’environnement chargées")

# === Création automatique des tables ===
try:
    Base.metadata.create_all(bind=engine)
    logger.debug("✅ Tables créées automatiquement dans la base de données")
except Exception as e:
    logger.error("❌ Erreur lors de la création des tables", exc_info=True)

# === App FastAPI ===
app = FastAPI(
    title="SecureSched API",
    description="Plateforme sécurisée de gestion d'horaires avec rôles et échanges",
    version="0.1.0"
)

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ À restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Middleware de log ===
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️  {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"⬅️  {response.status_code} {request.method} {request.url}")
    response.headers["X-Processed-By"] = "SecureSched-API"
    return response

# === Gestion des erreurs globales ===
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    body = await request.body()
    logger.error(f"❌ Exception pour {request.method} {request.url}")
    logger.error(f"Payload: {body}")
    logger.exception(exc)
    raise HTTPException(status_code=500, detail="Internal Server Error")

# === Routes internes ===
@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to SecureSched"}

@app.get("/health", tags=["debug"])
async def healthcheck():
    return {"status": "ok"}

@app.get("/api/routes", tags=["debug"])
async def list_routes():
    return [{"path": route.path, "name": route.name} for route in app.routes]

# === Inclusion des routers ===
routers = [
    (auth.router, ["auth"], "/auth"),
    (users_router.router, ["users"], "/users"),
    (schedules.router, ["schedules"], "/schedules"),
]

for router, tags, prefix in routers:
    try:
        logger.debug(f"Inclusion du router : {tags[0]} ({prefix})")
        app.include_router(router, prefix=prefix, tags=tags)
    except Exception as e:
        logger.error(f"Erreur lors de l’inclusion du router {tags[0]}", exc_info=True)

# === Route catch-all (optionnelle) ===
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    logger.warning(f"❗ Route non trouvée : {request.method} /{path_name}")
    return {"error": "Route not found"}

# === Lancement local avec Uvicorn ===
if __name__ == "__main__":
    import uvicorn
    logger.debug("Lancement du serveur local avec Uvicorn")
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="debug")
