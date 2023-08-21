from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.event_module.database.category.category_response_handler import (
    CategoryResponseHandler,
)
from src.event_module.database.event.event_response_handler import EventResponseHandler
from src.event_module.database.event_tag.event_tag_response_handler import (
    EventTagFilter,
    EventTagResponseHandler,
)
from src.event_module.database.tag.tag_response_handler import TagResponseHandler
from src.event_module.schemas import (
    CategoryCreate,
    CategoryUpdate,
    EventCreate,
    EventTagListCreate,
    EventTagListDelete,
    EventUpdate,
    TagCreate,
    TagUpdate,
)
from src.event_module.utils import check_university_event
from src.schemas import Response
from src.tour_module.database.tour_event.tour_event_responses import (
    TourEventResponseHandler,
)
from src.university_module.router import university_event_response_handler
from src.utils import Role, access_denied, role_access

event_router = APIRouter(prefix="/event", tags=["event"])
category_router = APIRouter(prefix="/event/category", tags=["category"])
tag_router = APIRouter(prefix="/event/tag", tags=["tag"])

event_response_handler = EventResponseHandler()
category_response_handler = CategoryResponseHandler()
tag_response_handler = TagResponseHandler()
event_tag_response_handler = EventTagResponseHandler()
tour_event_response_handler = TourEventResponseHandler()


@event_router.get("/", response_model=Response)
async def get_all_events(
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    return await event_response_handler.get_all(session=session)


@event_router.get("/category_filter/", response_model=Response)
async def get_events_by_categories(
    category_list: list[int] = Query(),
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    return await event_response_handler.get_by_categories(
        category_list=category_list, session=session
    )


@event_router.get("/category_filter/{category_id}", response_model=Response)
async def get_events_by_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    return await event_response_handler.get_by_category(
        category_id=category_id, session=session
    )


@event_router.get("/{event_id}", response_model=Response)
async def get_event_by_id(
    event_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    return await event_response_handler.get_by_id(model_id=event_id, session=session)


@event_router.post("/", response_model=Response)
async def create_event(
    user_role: Role,
    event: EventCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    if role_access[user_role] >= role_access[Role.UNIVERSITY]:
        return await event_response_handler.create(model_create=event, session=session)
    else:
        return access_denied()


@event_router.put("/{event_id}", response_model=Response)
async def update_event(
    user_role: Role,
    user_id: int | None,
    event: EventUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    if role_access[user_role] == role_access[Role.ADMIN]:
        return await event_response_handler.update(model_update=event, session=session)
    elif role_access[user_role] == role_access[Role.UNIVERSITY] and user_id is not None:
        if await check_university_event(
            university_id=user_id, event_id=event.id, session=session
        ):
            return await event_response_handler.update(
                model_update=event, session=session
            )

    return access_denied()


@event_router.delete("/{event_id}", response_model=Response)
async def delete_event(
    user_role: Role,
    user_id: int | None,
    event_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    if role_access[user_role] == role_access[Role.ADMIN]:
        return await event_response_handler.delete(model_id=event_id, session=session)
    elif role_access[user_role] == role_access[Role.UNIVERSITY] and user_id is not None:
        if await check_university_event(
            university_id=user_id, event_id=event_id, session=session
        ):
            return await event_response_handler.delete(
                model_id=event_id, session=session
            )

    return access_denied()


@category_router.get("/", response_model=Response)
async def get_all_categories(
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    return await category_response_handler.get_all(session=session)


@category_router.get("/{category_id}", response_model=Response)
async def get_category_by_id(
    category_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    return await category_response_handler.get_by_id(
        model_id=category_id, session=session
    )


@category_router.post("/", response_model=Response)
async def create_category(
    user_role: Role,
    category: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    if role_access[user_role] >= role_access[Role.ADMIN]:
        return await category_response_handler.create(
            model_create=category, session=session
        )
    else:
        return access_denied()


@category_router.put("/{category_id}", response_model=Response)
async def update_category(
    user_role,
    category: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    if role_access[user_role] >= role_access[Role.ADMIN]:
        return await category_response_handler.update(
            model_update=category, session=session
        )
    else:
        return access_denied()


@category_router.delete("/{category_id}", response_model=Response)
async def delete_category(
    user_role: Role,
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    if role_access[user_role] >= role_access[Role.ADMIN]:
        return await category_response_handler.delete(
            model_id=category_id, session=session
        )
    else:
        return access_denied()


@tag_router.get("/", response_model=Response)
async def get_all_tags(
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    return await tag_response_handler.get_all(session=session)


@tag_router.get("/{tag_id}", response_model=Response)
async def get_tag_by_id(
    tag_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    return await tag_response_handler.get_by_id(model_id=tag_id, session=session)


@tag_router.post("/", response_model=Response)
async def create_tag(
    user_role: Role, tag: TagCreate, session: AsyncSession = Depends(get_async_session)
) -> Response:
    if role_access[user_role] >= role_access[Role.ADMIN]:
        return await tag_response_handler.create(model_create=tag, session=session)
    else:
        return access_denied()


@tag_router.put("/{tag_id}", response_model=Response)
async def update_tag(
    user_role: Role, tag: TagUpdate, session: AsyncSession = Depends(get_async_session)
) -> Response:
    if role_access[user_role] >= role_access[Role.ADMIN]:
        return await tag_response_handler.update(model_update=tag, session=session)
    else:
        return access_denied()


@tag_router.delete("/{tag_id}", response_model=Response)
async def delete_tag(
    user_role: Role, tag_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    if role_access[user_role] >= role_access[Role.ADMIN]:
        return await tag_response_handler.delete(model_id=tag_id, session=session)
    else:
        return access_denied()


@event_router.post("/{event_id}/tags", response_model=Response)
async def set_tags(
    user_role: Role,
    user_id: int | None,
    event_tag: EventTagListCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    if role_access[user_role] == role_access[Role.ADMIN]:
        return await event_tag_response_handler.create_list(
            model_create=event_tag, session=session
        )
    elif role_access[user_role] == role_access[Role.UNIVERSITY] and user_id is not None:
        if await check_university_event(
            university_id=user_id, event_id=event_tag.event_id, session=session
        ):
            return await event_tag_response_handler.create_list(
                model_create=event_tag, session=session
            )

    return access_denied()


@event_router.get("/tour_filter/{tour_id}", response_model=Response)
async def get_event_id_list_by_tour_id(
    tour_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    return await tour_event_response_handler.get_by_filter(
        value=tour_id, session=session
    )


@tag_router.get("/event_filter/{event_id}", response_model=Response)
async def get_tag_id_list_by_event_id(
    event_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    return await event_tag_response_handler.get_by_filter(
        event_tag_filter=EventTagFilter.EVENT, value=event_id, session=session
    )


@event_router.get("/tag_filter/{tag_id}", response_model=Response)
async def get_event_id_list_by_tag_id(
    tag_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    return await event_tag_response_handler.get_by_filter(
        event_tag_filter=EventTagFilter.TAG, value=tag_id, session=session
    )


@event_router.delete("/{event_id}/event_tag", response_model=Response)
async def delete_event_tag(
    user_role: Role,
    user_id: int | None,
    event_tags: EventTagListDelete,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    if role_access[user_role] == role_access[Role.ADMIN]:
        return await event_tag_response_handler.delete_by_delete_schema(
            model_delete=event_tags, session=session
        )
    elif role_access[user_role] == role_access[Role.UNIVERSITY] and user_id is not None:
        if await check_university_event(
            university_id=user_id, event_id=event_tags.event_id, session=session
        ):
            return await event_tag_response_handler.delete_by_delete_schema(
                model_delete=event_tags, session=session
            )

    return access_denied()


@event_router.get("/university_filter/{university_id}", response_model=Response)
async def get_event_id_list_by_university_id(
    university_id: int, session: AsyncSession = Depends(get_async_session)
) -> Response:
    return await university_event_response_handler.get_by_filter(
        value=university_id, session=session
    )
