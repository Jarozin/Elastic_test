import asyncio
import ast
import csv
import sys
from datetime import datetime

from app.db import Document, async_session, init_db
from app.es import ensure_index, es_client, index_document


def parse_rubrics(value: str) -> list[str]:
    value = (value or "").strip()
    if not value:
        return []
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except (ValueError, SyntaxError):
        pass
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_date(value: str) -> datetime:
    value = (value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


async def main(csv_path: str) -> None:
    await init_db()
    await ensure_index()

    indexed = 0
    async with async_session() as session:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = (row.get("text") or "").strip()
                if not text:
                    continue

                doc = Document(
                    rubrics=parse_rubrics(row.get("rubrics", "")),
                    text=text,
                    created_date=parse_date(row.get("created_date", "")),
                )
                session.add(doc)
                await session.flush()
                await index_document(doc.id, doc.text)
                indexed += 1

                if indexed % 100 == 0:
                    print(f"Импортировано: {indexed}")

        await session.commit()

    print(f"Готово. Всего документов: {indexed}")
    await es_client.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))