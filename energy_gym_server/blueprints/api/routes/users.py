from quart import request, jsonify
from dependency_injector.wiring import Provide, inject

from .. import api
from energy_gym_server.services import UsersService, AuthorizationService
from energy_gym_server.models import dto, AccesRights
from energy_gym_server.containers import Application


@api.get('/users/get-list')
@AuthorizationService.check_acces(AccesRights.STUDENT.EDITANY)
@inject
async def get_student_list(
    service: UsersService = Provide[Application.services.students]
):
    data = await service.get_user_list()
    return jsonify(data.dict())


@api.get('/users/get-by-code')
@AuthorizationService.check_acces(AccesRights.STUDENT.GET)
@inject
async def get_student_by_code(
    service: UsersService = Provide[Application.services.students]
):
    body = await request.get_json()
    request_dto = dto.ItemByCodeRequest(**body)

    data = await service.get_by_code(request_dto)

    return jsonify(data.dict())


@api.get('/users/get-list-by-codes')
@AuthorizationService.check_acces(AccesRights.STUDENT.EDITANY)
@inject
async def get_student_list_by_codes(
    service: UsersService = Provide[Application.services.students]
):
    body = await request.get_json()
    request_dto = dto.ItemListByCodesRequest(**body)

    data = await service.get_list_by_codes(request_dto)

    return jsonify(data.dict())


@api.post('/users/add')
@AuthorizationService.check_acces(AccesRights.STUDENT.ADD)
@inject
async def add_student(
    service: UsersService = Provide[Application.services.students]
):
    body = await request.get_json()
    request_dto = dto.RegistrationUserRequest(**body)

    data = await service.add_user(request_dto)
    await service.commit()

    return jsonify(data.dict())


@api.delete('/users/delete')
@AuthorizationService.check_acces(AccesRights.STUDENT.DELETE)
@inject
async def delete_student(
    service: UsersService = Provide[Application.services.students]
):
    body = await request.get_json()
    request_dto = dto.ItemDeleteRequest(**body)

    data = await service.delete_user(request_dto)
    await service.commit()

    return jsonify(data.dict())
