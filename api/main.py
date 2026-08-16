from fastapi import FastAPI
from api.database import create_db_and_tables
from api.routers import auth, characters, inventory, rules, spells

app = FastAPI()

app.include_router(auth.router)
app.include_router(rules.router)

@app.on_event("startup")
def on_startup():
    print("Aplicação iniciada.")
    create_db_and_tables()  # Chame a função para criar o banco de dados e as tabelas

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
