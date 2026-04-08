from fastapi import FastAPI
import os

app = FastAPI()

@app.on_event("startup")
async def startup():
    print("\n" + "="*60)
    print("🚀 APP STARTUP")
    print(f"Working Dir: {os.getcwd()}")
    print(f"Files: {os.listdir('.')[:10]}")
    print("="*60 + "\n")

@app.get("/")
def root():
    return {"message": "Hello from Job Scrapper!"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
