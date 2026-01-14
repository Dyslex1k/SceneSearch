from collections.abc import Iterable

from neo4j import AsyncSession

from app.core.database import neo4j_driver

def get_session() -> AsyncSession:
    return neo4j_driver.session() # type: ignore

async def create_prefab_relationships(
    prefab_id: str,
    use_cases: Iterable[str],
    categories: Iterable[str],
    tags: Iterable[str],
) -> None:
    async with get_session() as session:
        for uc in use_cases:
            await session.run(
                """
                MERGE (p:Prefab {id: $prefab_id})
                MERGE (u:UseCase {name: $use_case})
                MERGE (p)-[:USED_FOR]->(u)
                """,
                prefab_id=prefab_id,
                use_case=uc,
            )

        for cat in categories:
            await session.run(
                """
                MERGE (c:Category {name: $category})
                MERGE (p:Prefab {id: $prefab_id})
                MERGE (p)-[:IN_CATEGORY]->(c)
                """,
                prefab_id=prefab_id,
                category=cat,
            )

        for tag in tags:
            await session.run(
                """
                MERGE (t:Tag {name: $tag})
                MERGE (p:Prefab {id: $prefab_id})
                MERGE (p)-[:HAS_TAG]->(t)
                """,
                prefab_id=prefab_id,
                tag=tag,
            )
