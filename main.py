import uvicorn


def main():
    uvicorn.run(
        app="wsgi:app",   # Uygulamanın doğru referans edildiğinden emin olun
        host="127.0.0.1",  # Yerel makine için 127.0.0.1 veya localhost
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    main()
