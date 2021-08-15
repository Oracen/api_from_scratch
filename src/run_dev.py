import uvicorn


def main() -> None:
    uvicorn.run(
        "api_from_scratch.api.api:app",
        host="localhost",
        port=5000,
        log_level="info",
        reload=True,
    )


if __name__ == "__main__":
    main()
