from flask import request, jsonify

from .. import api
from energy_gym_server.services import EntriesService, AuthorizationService
from energy_gym_server.models import dto, AccesRights


@api.get('/entries/get-list')
@AuthorizationService.check_acces(AccesRights.ENTRY.EDITANY)
def get_entry_list():
    with EntriesService() as service:
        data = service.get_list_all_entry()

    return jsonify(data.dict())


@api.get('/entries/get-in-day')
@AuthorizationService.check_acces(AccesRights.ENTRY.EDITANY)
def get_entry_list_in_day():
    request_dto = dto.EntryListInDayRequest(**request.json)

    with EntriesService() as service:
        data = service.get_entries_in_day(request_dto)

    return jsonify(data.dict())


@api.get('/entries/get-for-student')
@AuthorizationService.check_acces(AccesRights.ENTRY.GET)
def get_entry_list_for_student():
    request_dto = dto.EntryListUserRequest(**request.json)

    with EntriesService() as service:
        data = service.get_entries_for_user(request_dto)

    return jsonify(data.dict())


@api.get('/entries/get-by-code')
@AuthorizationService.check_acces(AccesRights.ENTRY.GET)
def get_entry_for_code():
    request_dto = dto.ItemByCodeRequest(**request.json)

    with EntriesService() as service:
        data = service.get_detailed_entry(request_dto)

    return jsonify(data.dict())


@api.post('/entries/add')
@AuthorizationService.check_acces(AccesRights.ENTRY.ADD)
def add_entry():
    request_dto = dto.EntryAddRequest(**request.json)

    with EntriesService() as service:
        data = service.add_entry(request_dto)
        service.commit()

    return jsonify(data.dict())


@api.delete('/entries/delete')
@AuthorizationService.check_acces(AccesRights.ENTRY.DELETE)
def delete_entry():
    request_dto = dto.ItemDeleteRequest(**request.json)

    with EntriesService() as service:
        data = service.delete_entry(request_dto)
        service.commit()

    return jsonify(data.dict())
