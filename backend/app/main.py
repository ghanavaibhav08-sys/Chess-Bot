from fastapi import FastAPI

app = FastAPI(title="AI Chess Coach")

@app.get("/health")
def health():
    return {"status": "ok"}
