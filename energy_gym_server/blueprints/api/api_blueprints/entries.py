from flask import request, jsonify, Blueprint

from energy_gym_server.services import EntriesService, AuthorizationService
from energy_gym_server.models import database, dto, AccesRights


entries_bl = Blueprint('entries', __name__)


@entries_bl.get('/get-list')
@AuthorizationService.check_acces(AccesRights.ENTRY.EDITANY)
def get_entry_list():
    with EntriesService() as service:
        data = service.get_list_all_entry()

    return jsonify(data.dict())


@entries_bl.get('/get-in-day')
@AuthorizationService.check_acces(AccesRights.ENTRY.EDITANY)
def get_entry_list_in_day():
    request_dto = dto.EntryListInTimeRequest(**request.json)

    with EntriesService() as service:
        data = service.get_entries_in_time(request_dto)

    return jsonify(data.dict())


@entries_bl.get('/get-for-student')
@AuthorizationService.check_acces(AccesRights.ENTRY.GET, return_user_info=True)
def get_entry_list_for_student(user: database.User):
    request_dto = dto.EntryListUserRequest(**request.json)

    with EntriesService() as service:
        data = service.get_entries_for_user(user, request_dto)

    return jsonify(data.dict())


@entries_bl.get('/get-by-code')
@AuthorizationService.check_acces(AccesRights.ENTRY.GET, return_user_info=True)
def get_entry_for_code(user: database.User):
    request_dto = dto.ItemByCodeRequest(**request.json)

    with EntriesService() as service:
        data = service.get_detailed_entry(user, request_dto)

    return jsonify(data.dict())


@entries_bl.post('/add')
@AuthorizationService.check_acces(AccesRights.ENTRY.ADD, return_user_info=True)
def add_entry(user: database.User):
    request_dto = dto.EntryAddRequest(**request.json)

    with EntriesService() as service:
        data = service.add_entry(user, request_dto)
        service.commit()

    return jsonify(data.dict())


@entries_bl.delete('/delete')
@AuthorizationService.check_acces(AccesRights.ENTRY.DELETE, return_user_info=True)
def delete_entry(user: database.User):
    request_dto = dto.ItemDeleteRequest(**request.json)

    with EntriesService() as service:
        data = service.delete_entry(user, request_dto)
        service.commit()

    return jsonify(data.dict())
