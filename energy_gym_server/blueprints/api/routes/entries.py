from quart import request, jsonify
from dependency_injector.wiring import Provide, inject

from .. import api
from energy_gym_server.services import EntriesService, AuthorizationService
from energy_gym_server.models import dto, AccesRights
from energy_gym_server.containers import Application


@api.get('/entries/get-list')
@AuthorizationService.check_acces(AccesRights.ENTRY.EDITANY)
@inject
async def get_entry_list(
    service: EntriesService = Provide[Application.services.entries]
):
    data = await service.get_list_all_entry()
    return jsonify(data.dict())


@api.get('/entries/get-in-day')
@AuthorizationService.check_acces(AccesRights.ENTRY.EDITANY)
@inject
async def get_entry_list_in_day(
    service: EntriesService = Provide[Application.services.entries]
):
    body = await request.get_json()
    request_dto = dto.EntryListInDayRequest(**body)

    data = await service.get_entries_in_day(request_dto)
    return jsonify(data.dict())


@api.get('/entries/get-for-student')
@AuthorizationService.check_acces(AccesRights.ENTRY.GET)
@inject
async def get_entry_list_for_student(
    service: EntriesService = Provide[Application.services.entries]
):
    body = await request.get_json()
    request_dto = dto.EntryListStudentRequest(**body)

    data = await service.get_entries_for_student(request_dto)
    return jsonify(data.dict())


@api.get('/entries/get-by-code')
@AuthorizationService.check_acces(AccesRights.ENTRY.GET)
@inject
async def get_entry_for_code(
    service: EntriesService = Provide[Application.services.entries]
):
    body = await request.get_json()
    request_dto = dto.ItemByCodeRequest(**body)

    data = await service.get_detailed_entry(request_dto)
    return jsonify(data.dict())


@api.get('/entries/get-list-by-codes')
@AuthorizationService.check_acces(AccesRights.ENTRY.GET)
@inject
async def get_entry_list_for_codes(
    service: EntriesService = Provide[Application.services.entries]
):
    body = await request.get_json()
    request_dto = dto.ItemListByCodesRequest(**body)

    data = await service.get_entry_list_by_codes(request_dto)
    return jsonify(data.dict())


@api.post('/entries/add')
@AuthorizationService.check_acces(AccesRights.ENTRY.ADD)
@inject
async def add_entry(
    service: EntriesService = Provide[Application.services.entries]
):
    body = await request.get_json()
    request_dto = dto.EntryAddRequest(**body)

    data = await service.add_entry(request_dto)
    await service.commit()

    return jsonify(data.dict())


@api.delete('/entries/delete')
@AuthorizationService.check_acces(AccesRights.ENTRY.DELETE)
@inject
async def delete_entry(
    service: EntriesService = Provide[Application.services.entries]
):
    body = await request.get_json()
    request_dto = dto.ItemDeleteRequest(**body)

    data = await service.delete_entry(request_dto)
    await service.commit()

    return jsonify(data.dict())
