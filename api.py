from db import Table, Column
from flask import Flask, Request, jsonify, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


columns = [
        Column(name="name", unique=False, type='str'),
        Column(name="number", unique=True, type='str'),
        Column(name="age", unique=False, type='int'),
    ]

path = "/root/dblab"
tbl = Table(dir=path, columns=columns)


@app.route('/columns')
@cross_origin()
def return_table_columns():
    columns = []
    for col in tbl.columns:
        colinfo = {"name":col.name, "field":col.name, "label":col.name}
        columns.append(colinfo)
    return jsonify(columns)


@app.route("/all")
@cross_origin()
def get_all():
    return jsonify(tbl.get_all())


@app.route("/byid/:id")
@cross_origin()
def get_by_id(id):
    return jsonify(tbl.get_by_id(id))


@app.route("/byfield")
@cross_origin()
def get_by_field(req: Request):
    json = req.json()
    return jsonify(tbl.search_by_field_value(json['column'], json['value']))


@app.route("/fastbyfield")
@cross_origin()
def fast_get_by_field(req: Request):
    json = req.json()
    return jsonify(tbl.fast_search_by_field(json['column'], json['value']))


@app.route("/insert")
@cross_origin()
def insert(req:Request):
    json = req.json()
    tbl.insert(json)
    return Response(status=200)


@app.route("/update/:id")
@cross_origin()
def update(req:Request, id):
    json = req.json()
    tbl.update(id, json)


@app.route("/remove/:id")
@cross_origin()
def remove_by_id(id):
    tbl.remove_by_id(id)


@app.route("/removebyval")
@cross_origin()
def remove_by_value(req:Request):
    json = req.json()
    tbl.remove_by_value(json['column'], json['value'])


@app.route('/init')
@cross_origin()
def initdb():
    tbl.init_db()


@app.route('/cleanup')
@cross_origin()
def cleanup():
    tbl.cleanup()


@app.route('/deleteall')
@cross_origin()
def delete_all():
    tbl.delete_all()


@app.route('/backup')
@cross_origin()
def backup():
    tbl.backup()


@app.route('/restore')
@cross_origin()
def restore():
    tbl.restore()


@app.route('/dump')
@cross_origin()
def dump():
    tbl.to_csv()

