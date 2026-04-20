"""Pagination helper for SQLAlchemy queries."""

from __future__ import annotations

from typing import Any

from flask_sqlalchemy.query import Query


DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def paginate_query(
    query: Query,
    args: dict[str, Any],
) -> tuple[dict, list]:
    """Apply pagination to *query* based on request args.

    Parameters
    ----------
    query:
        An un-executed SQLAlchemy query.
    args:
        Typically ``request.args`` - should contain optional ``page`` and
        ``per_page`` keys.

    Returns
    -------
    tuple[dict, list]
        A (metadata dict, list of model instances) pair.
    """
    try:
        page = max(1, int(args.get("page", 1)))
    except (TypeError, ValueError):
        page = 1

    try:
        per_page = min(
            MAX_PAGE_SIZE,
            max(1, int(args.get("per_page", DEFAULT_PAGE_SIZE))),
        )
    except (TypeError, ValueError):
        per_page = DEFAULT_PAGE_SIZE

    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return (
        {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
        },
        items,
    )
