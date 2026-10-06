"""Local MySQL-connected campus placement UI. Bind only to localhost."""
from pathlib import Path
import json, os
from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv
import mysql.connector
load_dotenv()
ROOT=Path(__file__).parent
CONFIG=json.loads((ROOT/'config.json').read_text())
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=16384

def connect():
    return mysql.connector.connect(host=os.getenv('MYSQL_HOST','127.0.0.1'),port=int(os.getenv('MYSQL_PORT','3306')),user=os.getenv('MYSQL_USER','root'),password=os.getenv('MYSQL_PASSWORD',''),database=os.getenv('MYSQL_DATABASE','campus_placement'))

@app.after_request
def headers(response):
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['X-Frame-Options']='DENY'
    return response

@app.route('/')
def index(): return send_file(ROOT/'web/index.html')

@app.route('/api/state')
def state():
    try:
        with connect() as db:
            cur=db.cursor(dictionary=True)
            data={}
            for table in CONFIG:
                cur.execute(f'SELECT * FROM `{table}` ORDER BY `{CONFIG[table]["pk"]}`')
                data[table]=[{k:float(v) if hasattr(v,'as_tuple') else v.isoformat() if hasattr(v,'isoformat') else v for k,v in row.items()} for row in cur.fetchall()]
            return jsonify(data)
    except mysql.connector.Error:
        return jsonify(error='MySQL connection failed. Check .env and run schema.sql and seed.sql.'),503

@app.route('/api/<table>',methods=['POST'])
@app.route('/api/<table>/<int:rid>',methods=['PUT','DELETE'])
def mutate(table,rid=None):
    if table not in CONFIG: return jsonify(error='Unknown table'),404
    # Same-origin local requests only: no remote website may write through this API.
    origin=request.headers.get('Origin')
    if origin and origin!=request.host_url.rstrip('/'): return jsonify(error='Origin not allowed'),403
    cfg=CONFIG[table]; fields=list(cfg['fields']); pk=cfg['pk']
    try:
        with connect() as db:
            cur=db.cursor(dictionary=True)
            if request.method in ('PUT','DELETE'):
                cur.execute(f'SELECT `{pk}` FROM `{table}` WHERE `{pk}`=%s FOR UPDATE',(rid,))
                if not cur.fetchone(): return jsonify(error='Record not found'),404
            if request.method=='DELETE':
                cur.execute(f'DELETE FROM `{table}` WHERE `{pk}`=%s',(rid,))
            else:
                d=request.get_json(silent=True)
                if not isinstance(d,dict) or set(d)!=set(fields): return jsonify(error='Supply all required fields'),400
                for k,typ in cfg['fields'].items():
                    v=d[k]
                    if typ=='number' or (isinstance(typ,str) and typ in CONFIG):
                        if isinstance(v,bool) or not isinstance(v,(int,float)): return jsonify(error=f'{k} must be numeric'),400
                        if k.endswith('_id') or k=='round_no':
                            if int(v)!=v or v<1:return jsonify(error=f'{k} must be a positive integer'),400
                        if k in ('cgpa','min_cgpa') and not 0<=v<=10:return jsonify(error='CGPA must be between 0 and 10'),400
                        if k in ('ctc','package') and v<=0:return jsonify(error='Package must be positive'),400
                    elif isinstance(typ,list):
                        if v not in typ:return jsonify(error='Invalid status or result'),400
                    elif not isinstance(v,str) or not v.strip() or len(v)>150:return jsonify(error=f'{k} must contain 1–150 characters'),400
                    elif typ=='email' and ('@' not in v or '.' not in v.split('@')[-1]):return jsonify(error='Enter a valid email'),400
                vals=[d[k].strip() if isinstance(d[k],str) else d[k] for k in fields]
                if request.method=='POST':
                    cols=','.join('`'+k+'`' for k in fields)
                    cur.execute(f'INSERT INTO `{table}` ({cols}) VALUES ({",".join(["%s"]*len(fields))})',vals)
                    rid=cur.lastrowid
                else:
                    sets=','.join('`'+k+'`=%s' for k in fields)
                    cur.execute(f'UPDATE `{table}` SET {sets} WHERE `{pk}`=%s',vals+[rid])
            db.commit()
            return jsonify(ok=True,id=rid)
    except mysql.connector.IntegrityError as e:
        if e.errno==1062:msg='Duplicate record: email, department, application, interview round or placement must be unique.'
        elif e.errno in (1451,1452):msg='Related record constraint: check references, or delete dependent records first.'
        else:msg='Database constraint failed. Check values and relationships.'
        return jsonify(error=msg),409
    except mysql.connector.Error as e:
        if e.errno==1644:return jsonify(error=e.msg),409
        return jsonify(error='Database operation failed. Check connection and field values.'),400

if __name__=='__main__':
    print('Open http://127.0.0.1:5000 — MySQL connection is required for the assessed demo.')
    app.run(host='127.0.0.1',port=5000,debug=False)
