from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from schema import URL
from pydantic import ValidationError
from database.db import connect_db, get_id, get_url, add_url
import base64

app = Flask(__name__)

CORS(app, origins=[
   "http://localhost:5500",
   "http://127.0.0.1:5500"
])

mainURL = "http://localhost:8080/"

@app.post('/api/get_url')
async def fetch_url():
   data = request.get_json(silent=True)
   try:
      data = URL.model_validate(data)
   except ValidationError as error:
      return jsonify({"message":"Invalid input", "error":error}), 400

   conn = await connect_db()
   url = data.url
   id = await get_id(conn, url)
   if id is not None:
         encoded_id = base64.urlsafe_b64encode(str(id).encode('utf-8'))
         id = encoded_id.decode("utf-8")
         short_url = mainURL + str(id)
         await conn.close()
         
         return jsonify({
            'message':"short URL created successfully.",
            'shorturl': short_url
         }), 201

   await add_url(conn, url)
   id = str(await get_id(conn, url))      
   encoded_id = base64.urlsafe_b64encode(id.encode('utf-8'))
   id = encoded_id.decode("utf-8")
   short_url = mainURL + id

   await conn.close()
   return jsonify({
         'message':"short URL created successfully.",
         'shorturl': short_url
      }), 201
   
@app.route('/<string:id>')
async def short(id: str):
   conn = await connect_db()
   decoded_id = base64.urlsafe_b64decode(id)
   id = decoded_id.decode('utf-8')
   url = await get_url(conn, id)

   if url is None:
      return jsonify({"message":"Invalid URL"}), 400

   return redirect(url)

if __name__ == "__main__":
    app.run('localhost', 8080, debug=True)