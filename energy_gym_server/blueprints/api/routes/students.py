from quart import request, jsonify
from dependency_injector.wiring import Provide, inject

from .. import api
from energy_gym_server.services import StudentsService
from energy_gym_server.models import dto
from energy_gym_server.containers import Application


@api.post('/students/add')
@inject
async def add_student(
    service: StudentsService = Provide[Application.services.students]
):
    body = await request.get_json()
    request_dto = dto.StudentAddRequest(**body)

    data = await service.add_student(request_dto)
    await service.commit()

    return jsonify(data.dict())


@api.get('/students/get-list')
@inject
async def get_student_list(
    service: StudentsService = Provide[Application.services.students]
):
    data = await service.get_student_list()
    return jsonify(data.dict())


@api.delete('/students/delete')
@inject
async def delete_student(
    service: StudentsService = Provide[Application.services.students]
):
    body = await request.get_json()
    request_dto = dto.ItemsDeleteRequest(**body)

    data = await service.delete_student(request_dto)
    await service.commit()

    return jsonify(data.dict())
