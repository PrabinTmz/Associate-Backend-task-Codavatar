from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql import func
from typing import TypeVar
from schemas.pagination import PaginationBase, PaginatedResponse

T = TypeVar("T")


async def paginate_query(
    db_session: AsyncSession, query: Select, offset: int, limit: int
) -> PaginatedResponse[T]:
    """
    Centralized pagination utility for async SQLAlchemy queries.
    Args:
        db_session: The AsyncSession to interact with the database.
        query: The SQLAlchemy query object.
        offset: The starting index for items.
        limit: The number of items to fetch.

    Returns:
        A PaginatedResponse object.
    """
    # Fetch total count
    count_query = query.with_only_columns(func.count())
    total = await db_session.scalar(count_query)

    # Fetch items with pagination
    paginated_query = query.offset(offset).limit(limit)
    result = await db_session.execute(paginated_query)
    items = result.scalars().all()

    next_offset = offset + limit if offset + limit < total else None
    prev_offset = offset - limit if offset - limit >= 0 else None

    return PaginatedResponse(
        data=items,
        pagination=PaginationBase(
            total=total,
            limit=limit,
            offset=offset,
            next_offset=next_offset,
            prev_offset=prev_offset,
        ),
    )
