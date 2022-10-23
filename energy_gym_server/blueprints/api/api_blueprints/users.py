from flask import request, jsonify, Blueprint

from energy_gym_server.services import UsersService, AuthorizationService
from energy_gym_server.models import dto, AccesRights


users_bl = Blueprint('users', __name__)


users_bl.get('/get-list')
@AuthorizationService.check_acces(AccesRights.USER.EDITANY)
def get_student_list():
    with UsersService() as service:
        data = service.get_user_list()

    return jsonify(data.dict())


users_bl.get('/get-by-code')
@AuthorizationService.check_acces(AccesRights.USER.GET)
def get_student_by_code():
    request_dto = dto.ItemByCodeRequest(**request.json)

    with UsersService() as service:
        data = service.get_by_code(request_dto)

    return jsonify(data.dict())


users_bl.post('/add')
@AuthorizationService.check_acces(AccesRights.USER.ADD)
def add_student():
    request_dto = dto.RegistrationUserRequest(**request.json)

    with UsersService() as service:
        data = service.add_user(request_dto)
        service.commit()

    return jsonify(data.dict())


users_bl.delete('/delete')
@AuthorizationService.check_acces(AccesRights.USER.DELETE)
def delete_student():
    request_dto = dto.ItemDeleteRequest(**request.json)

    with UsersService() as service:
        data = service.delete_user(request_dto)
        service.commit()

    return jsonify(data.dict())
