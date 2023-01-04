import uuid
from typing import Optional
from application.core.models.pagination import Pagination


def generate_uuid():
    return str(uuid.uuid4())


def is_valid_uuid(uuid_to_test):
    try:
        uuid.UUID(str(uuid_to_test))
        return True
    except ValueError:
        return False


def paginate(query, page, per_page=20) -> Optional[Pagination]:
    if page < 1:
        return None
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    if not items and page != 1:
        return None

    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.order_by(None).count()

    return Pagination(data=items, page=page, per_page=per_page, total=total)
