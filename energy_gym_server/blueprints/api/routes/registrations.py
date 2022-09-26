from quart import jsonify

from .. import api


@api.get('/reg')
async def get_reg():
    return jsonify({'k1': 'v1', 'k2': 'v2'})
