import httpx

from config import (
    CONNECT_TIMEOUT,
    READ_TIMEOUT,
)


async def get_file_size(
    download_url: str,
    headers: dict | None = None,
) -> int:
    """
    Returns file size in bytes using a HEAD request.

    Raises:
        Exception if size cannot be determined.
    """

    headers = headers or {}

    timeout = httpx.Timeout(
        connect=CONNECT_TIMEOUT,
        read=READ_TIMEOUT,
        write=READ_TIMEOUT,
        pool=READ_TIMEOUT,
    )

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
    ) as client:

        response = await client.head(
            download_url,
            headers=headers,
        )

    response.raise_for_status()

    size = response.headers.get("Content-Length")

    if size is None:
        raise Exception("Unable to determine file size.")

    return int(size)


def can_upload(file_size: int, limit: int) -> bool:
    """
    Returns True if the file is within the upload limit.
    """
    return file_size <= limit


def format_size(size: int) -> str:
    """
    Convert bytes into KB / MB / GB.
    """

    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:

        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"
