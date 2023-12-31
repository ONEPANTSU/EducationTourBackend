from fastapi import UploadFile
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database_utils.base_query import BaseQuery
from src.database_utils.cascade_base_response_handler import CascadeBaseResponseHandler
from src.event_module.database.event.event_models import EventModels
from src.event_module.database.event.event_query import EventQuery
from src.event_module.database.event.text.event_data_key import EventDataKey
from src.event_module.database.event.text.event_details import EventDetails
from src.event_module.database.event.text.event_message import EventMessage
from src.event_module.database.event_tag.event_tag_models import EventTagFilter
from src.event_module.database.event_tag.event_tag_query import EventTagQuery
from src.google_drive.directories import Directory
from src.instruments import image_handler
from src.schemas import Response
from src.tour_module.database.tour_event.tour_event_models import TourEventFilter
from src.tour_module.database.tour_event.tour_event_query import TourEventQuery
from src.university_module.database.university_event.university_event_models import (
    UniversityEventFilter,
)
from src.university_module.database.university_event.university_event_query import (
    UniversityEventQuery,
)
from src.user_module.database.user_event.user_event_models import UserEventFilter
from src.user_module.database.user_event.user_event_query import UserEventQuery
from src.utils import Status, return_json


class EventResponseHandler(CascadeBaseResponseHandler):
    _query: EventQuery = EventQuery()
    _message: EventMessage = EventMessage()
    _data_key: EventDataKey = EventDataKey()
    _details: EventDetails = EventDetails()

    _dependencies: dict[BaseQuery, object] = {
        EventTagQuery(): EventTagQuery.dependency_fields[EventTagFilter.EVENT],
        TourEventQuery(): TourEventQuery.dependency_fields[TourEventFilter.EVENT],
        UniversityEventQuery(): UniversityEventQuery.dependency_fields[
            UniversityEventFilter.EVENT
        ],
        UserEventQuery(): UserEventQuery.dependency_fields[UserEventFilter.EVENT],
    }

    _models: EventModels = EventModels()
    _schema_create_class: type = _models.create_class
    _schema_update_class: type = _models.update_class
    _schema_read_class: type = _models.read_class
    _model: type = _models.database_table

    _google_directory: Directory = Directory.EVENT

    async def get_by_filter(
        self,
        category_list: list[int] | None,
        tag_id: int | None,
        tour_id: int | None,
        university_id: int | None,
        session: AsyncSession,
    ) -> Response:
        try:
            schemas = await self._query.get_by_filter_query(
                category_list=category_list,
                tag_id=tag_id,
                tour_id=tour_id,
                university_id=university_id,
                session=session,
            )
            if schemas is not None:
                data = {
                    self._data_key.get("count"): len(schemas),
                    self._data_key.get("schemas"): schemas,
                }
                return return_json(
                    status=Status.SUCCESS,
                    message=self._message.get("get_all_success"),
                    data=data,
                )
            else:
                raise Exception()
        except Exception as e:
            logger.error(str(e))
            return return_json(
                status=Status.ERROR,
                message=self._message.get("get_all_error"),
                details=str(e),
            )

    async def get_all(self, session: AsyncSession) -> Response:
        try:
            schemas = await self._query.get_all(session=session)
            if schemas is not None:
                data = {
                    self._data_key.get("count"): len(schemas),
                    self._data_key.get("schemas"): schemas,
                }
                return return_json(
                    status=Status.SUCCESS,
                    message=self._message.get("get_all_success"),
                    data=data,
                )
            else:
                raise Exception()
        except Exception as e:
            logger.error(str(e))
            return return_json(
                status=Status.ERROR,
                message=self._message.get("get_all_error"),
                details=str(e),
            )

    async def get_by_id_list(
        self, model_id_list: list[int], session: AsyncSession
    ) -> Response:
        try:
            schemas = [
                await self._query.get_by_id(model_id=model_id, session=session)
                for model_id in model_id_list
            ]
            if len(schemas) is not None:
                data = {self._data_key.get("schemas"): schemas}
                return return_json(
                    status=Status.SUCCESS,
                    message=self._message.get("get_all_success"),
                    data=data,
                )
            else:
                raise Exception()
        except Exception as e:
            logger.error(str(e))
            return return_json(
                status=Status.ERROR,
                message=self._message.get("get_all_error"),
                details=str(e),
            )

    @logger.catch
    async def create(
        self, model_create: _schema_create_class, session: AsyncSession
    ) -> Response:
        try:
            error = await self._query.create(model_create=model_create, session=session)
            if error is None:
                return return_json(
                    status=Status.SUCCESS, message=self._message.get("create_success")
                )
            else:
                raise error
        except IntegrityError as e:
            logger.error(str(e))
            return return_json(
                status=Status.ERROR,
                message=self._message.get("create_error"),
                details=self._details.get("wrong_category_id"),
            )

    @logger.catch
    async def get_by_categories(
        self, category_list: list[int], session: AsyncSession
    ) -> Response:
        try:
            events = await self._query.get_by_categories_query(
                category_list=category_list, session=session
            )
            if events is not None:
                data = {
                    self._data_key.get("count"): len(events),
                    self._data_key.get("schemas"): events,
                }
                return return_json(
                    status=Status.SUCCESS,
                    message=self._message.get("get_by_category_success").format(
                        id=category_list
                    ),
                    data=data,
                )
            else:
                raise Exception()
        except Exception as e:
            logger.error(str(e))
            return return_json(
                status=Status.ERROR,
                message=self._message.get("get_by_category_error"),
                details=str(e),
            )

    @logger.catch
    async def get_by_category(
        self, category_id: int, session: AsyncSession
    ) -> Response:
        try:
            events = await self._query.get_by_category_query(
                category_id=category_id, session=session
            )
            if events is not None:
                data = {
                    self._data_key.get("count"): len(events),
                    self._data_key.get("schemas"): events,
                }
                return return_json(
                    status=Status.SUCCESS,
                    message=self._message.get("get_by_category_success").format(
                        id=category_id
                    ),
                    data=data,
                )
            else:
                raise Exception()
        except Exception as e:
            logger.error(str(e))
            return return_json(
                status=Status.ERROR,
                message=self._message.get("get_by_category_error"),
                details=str(e),
            )
