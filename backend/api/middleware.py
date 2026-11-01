from fastapi.middleware.cors import CORSMiddleware 

def setup_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://cat-dog-classifier-seven.vercel.app",
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )