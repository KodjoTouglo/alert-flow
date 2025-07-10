import aiofiles
import asyncio

async def read_lines(file_path: str, queue: asyncio.Queue, delay: float = 2.0):
    """Lit un fichier ligne par ligne avec un délai simulé entre chaque ligne"""
    async with aiofiles.open(file_path, "r") as f:
        async for line in f:
            await asyncio.sleep(delay)  # Introduire un délai entre chaque ligne
            line = line.strip()  # Retirer les espaces superflus
            if line:
                await queue.put(line)  # Ajouter la ligne à la queue pour traitement
