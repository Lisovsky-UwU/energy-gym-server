from quart import request, jsonify
from dependency_injector.wiring import Provide, inject

from .. import api
from energy_gym_server.services import UserService, StudentsService
from energy_gym_server.models import dto
from energy_gym_server.containers import Application


@api.post('/authorization/registration-student')
@inject
async def registration_new_student(
    student_service: StudentsService = Provide[Application.services.students],
    user_service: UserService = Provide[Application.services.user]
):
    body = await request.get_json()
    request_dto = dto.RegistrationStudentRequest(**body)

    await student_service.add_student(request_dto)
    await student_service.commit()

    login_data = await user_service.generate_token(
        dto.LoginRequest(
            username=request_dto.name,
            password=request_dto.password
        )
    )
    await user_service.commit()

    return jsonify(login_data.dict())


@api.get('/authorization/login')
@inject
async def get_login_token(
    service: UserService = Provide[Application.services.user]
):
    body = await request.get_json()
    request_dto = dto.LoginRequest(**body)

    data = await service.generate_token(request_dto)
    await  service.commit()

    return jsonify(data.dict())
