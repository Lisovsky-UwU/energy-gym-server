from flask import request, jsonify, Blueprint

from energy_gym_server.services import AuthorizationService, UsersService
from energy_gym_server.models import dto


authorization_bl = Blueprint('authorization', __name__)


@authorization_bl.post('/registration')
def registration_new_student():
    request_dto = dto.RegistrationUserRequest(**request.json)

    with UsersService() as user_service:
        user_service.add_user(request_dto)
        user_service.commit()

    with AuthorizationService() as auth_service:
        login_data = auth_service.generate_token(
            dto.LoginRequest(
                username=request_dto.name,
                password=request_dto.password
            )
        )
        auth_service.commit()

    return jsonify(login_data.dict())


@authorization_bl.get('/login')
def get_login_token():
    request_dto = dto.LoginRequest(**request.json)

    with AuthorizationService() as service:
        data = service.generate_token(request_dto)
        service.commit()

    return jsonify(data.dict())
