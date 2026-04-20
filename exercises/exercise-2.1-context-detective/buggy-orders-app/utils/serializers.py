"""Generic serialization helpers.

These utilities provide a model-agnostic way to convert SQLAlchemy objects
into JSON-safe dictionaries.  They are used by the admin dashboard (not yet
shipped) and are **not** used by the public API endpoints in ``routes/``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence


def serialize_model(instance: Any, include_relationships: bool = False) -> dict:
    """Convert a SQLAlchemy model instance to a plain dict.

    Parameters
    ----------
    instance:
        Any SQLAlchemy model object.
    include_relationships:
        If ``True``, attempt to serialize related objects one level deep.

    Returns
    -------
    dict
        A JSON-serialisable dictionary.

    .. warning::

        # TODO: this doesn't handle nested relationships properly - revisit
        # When include_relationships=True, child collections that use
        # lazy loading may trigger N+1 queries or return stale data
        # depending on the session state.  Needs refactoring to accept
        # an explicit list of relationship names + eager-load strategy.
    """
    mapper = instance.__class__.__mapper__

    data: dict[str, Any] = {}
    for column in mapper.columns:
        value = getattr(instance, column.key)
        if isinstance(value, datetime):
            value = value.isoformat() + "Z"
        data[column.key] = value

    if include_relationships:
        for rel in mapper.relationships:
            related = getattr(instance, rel.key)
            if related is None:
                data[rel.key] = None
            elif isinstance(related, list):
                # TODO: this doesn't handle nested relationships properly - revisit
                data[rel.key] = [serialize_model(child) for child in related]
            else:
                data[rel.key] = serialize_model(related)

    return data


def serialize_list(
    instances: Sequence[Any],
    include_relationships: bool = False,
) -> list[dict]:
    """Serialize a list of model instances."""
    return [
        serialize_model(inst, include_relationships=include_relationships)
        for inst in instances
    ]
