# # main.py
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import httpx
# from google.adk.cli.fast_api import get_fast_api_app


# app: FastAPI = get_fast_api_app(
#     agents_dir = "./",
#     allow_origins="*",
#     web=True,
#     a2a=False,
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/health")
# def health_check():
#     return {"message": "OK"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.adk.cli.fast_api import get_fast_api_app

# create ADK generated app
adk_app = get_fast_api_app(
    agents_dir="./",
    allow_origins="*",
    web=True,
    a2a=False,
)

# create root FastAPI app
app = FastAPI()

# apply CORS on root
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount ADK app
app.mount("/", adk_app)


@app.get("/health")
def health():
    return {"status": "ok"}