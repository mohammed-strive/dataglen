from flask import (
    Blueprint, g, request, url_for
)
from .db import get_db
from datetime import datetime
import json
from .auth import basicauth
from operator import itemgetter

__LIMIT__ = 1000

bp = Blueprint('sensor', __name__, url_prefix='/api/v1/sensordata')

@bp.route('/<int:sensorid>', methods=['POST'])
@basicauth.login_required
def storeSensorData(sensorid):
    reading = float(request.form['reading'])
    timestamp = float(request.form['timestamp'])
    sensorType = str(request.form['sensortype'])

    date = datetime.fromtimestamp(timestamp)
    isotime = date.isoformat();

    db = get_db()
    cur = db.cursor()
    cur.execute(
        'INSERT INTO data(sensorid, reading, timestamp, sensortype)'
        'VALUES (?, ?, ?, ?)',
        (sensorid, reading, isotime, sensorType),
    )
    db.commit()
    newid = cur.lastrowid
    return json.dumps({'success': True, 'id': newid })

@bp.route('/<int:sensorid>', methods=['GET'])
@basicauth.login_required
def getSensorData(sensorid):
    db = get_db()
    data = db.execute(
        'SELECT * FROM data WHERE SENSORID = ?',
        (sensorid,)
    ).fetchall()
    print(data)
    data = [dict(row) for row in sorted(data, key=itemgetter('id'))]

    for result in data:
        result['timestamp'] = datetime.fromisoformat(result['timestamp']).timestamp()

    count = 0
    nxt = ''
    if len(data) > __LIMIT__:
        nxt = url_for('sensor.getSensorData', {'from': len(data) + 1, 'to': (len(data) + 1 + __LIMIT__)})
        count = __LIMIT__

    results = {
        'success': True,
        'data': data,
    }

    if count: results['count'] = count
    if nxt: results['next'] = nxt

    return json.dumps(results)

