import os

import aiofiles
import httpx

from config import (
    CONNECT_TIMEOUT,
    READ_TIMEOUT,
    TEMP_DIR,
)


CHUNK_SIZE = 1024 * 1024  # 1 MB


async def download_file(
    download_url: str,
    filename: str,
    headers: dict | None = None,
    progress_callback=None,
):
    """
    Downloads a file asynchronously.

    progress_callback(downloaded_bytes, total_bytes)

    Returns:
        file_path
    """

    headers = headers or {}

    timeout = httpx.Timeout(
        connect=CONNECT_TIMEOUT,
        read=READ_TIMEOUT,
        write=READ_TIMEOUT,
        pool=READ_TIMEOUT,
    )

    file_path = TEMP_DIR / filename

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
    ) as client:

        async with client.stream(
            "GET",
            download_url,
            headers=headers,
        ) as response:

            response.raise_for_status()

            total = int(
                response.headers.get(
                    "Content-Length",
                    0,
                )
            )

            downloaded = 0

            try:

                async with aiofiles.open(
                    file_path,
                    "wb",
                ) as file:

                    async for chunk in response.aiter_bytes(CHUNK_SIZE):

                        if not chunk:
                            continue

                        await file.write(chunk)

                        downloaded += len(chunk)

                        if progress_callback:
                            await progress_callback(
                                downloaded,
                                total,
                            )

            except Exception:

                if file_path.exists():
                    os.remove(file_path)

                raise

    return file_path


def delete_file(file_path):
    """
    Delete downloaded temporary file.
    """

    try:

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception:
        pass
