import httpx

from config import (
    RESOLVE_API,
    CONNECT_TIMEOUT,
    READ_TIMEOUT,
)


async def resolve_link(url: str) -> dict:
    """
    Resolve a Terabox share URL using the configured API.

    Returns:
        {
            "filename": "...",
            "direct_link": "...",
            "headers": {...}
        }
    """

    timeout = httpx.Timeout(
        connect=CONNECT_TIMEOUT,
        read=READ_TIMEOUT,
        write=READ_TIMEOUT,
        pool=READ_TIMEOUT,
    )

    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:

        response = await client.get(
            RESOLVE_API,
            params={
                "url": url,
            },
        )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != "success":
        raise Exception("Failed to resolve Terabox link.")

    direct_link = data.get("direct_link")
    filename = data.get("filename")
    headers = data.get("headers", {})

    if not direct_link:
        raise Exception("Direct download link not found.")

    if not filename:
        filename = "Unknown File"

    return {
        "filename": filename,
        "direct_link": direct_link,
        "headers": headers,
    }
