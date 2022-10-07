from quart import request, jsonify
from dependency_injector.wiring import Provide, inject

from .. import api
from energy_gym_server.services import AuthorizationService, UsersService
from energy_gym_server.models import dto
from energy_gym_server.containers import Application


@api.post('/authorization/registration-user')
@inject
async def registration_new_student(
    user_service: UsersService = Provide[Application.services.students],
    auth_service: AuthorizationService = Provide[Application.services.authorization]
):
    body = await request.get_json()
    request_dto = dto.RegistrationUserRequest(**body)

    await user_service.add_user(request_dto)
    await user_service.commit()

    login_data = await auth_service.generate_token(
        dto.LoginRequest(
            username=request_dto.name,
            password=request_dto.password
        )
    )
    await auth_service.commit()

    return jsonify(login_data.dict())


@api.get('/authorization/login')
@inject
async def get_login_token(
    service: AuthorizationService = Provide[Application.services.authorization]
):
    body = await request.get_json()
    request_dto = dto.LoginRequest(**body)

    data = await service.generate_token(request_dto)
    await  service.commit()

    return jsonify(data.dict())
