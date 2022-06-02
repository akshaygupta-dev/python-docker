import psycopg2
import json
import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/widgets')
def get_widgets():
  mydb = psycopg2.connect(
      dbname= os.environ['DATABASE_NAME'], 
      user=os.environ['DATABASE_USER'], 
      password=os.environ['DATABASE_PASSWORD'], 
      port=os.environ['DATABASE_PORT'], 
      host=os.environ['DATABASE_HOST']
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM widgets")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()
  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)

@app.route('/initdb')
def db_init():

  mydb = psycopg2.connect(
      dbname= os.environ['DATABASE_NAME'], 
      user=os.environ['DATABASE_USER'], 
      password=os.environ['DATABASE_PASSWORD'], 
      port=os.environ['DATABASE_PORT'], 
      host=os.environ['DATABASE_HOST']
  )
  
  cursor = mydb.cursor()

  cursor.execute("DROP TABLE IF EXISTS widgets;")
  cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255));")
  cursor.execute("INSERT INTO widgets VALUES('cursor' , 'representing position');")
  
  mydb.commit()
  
  cursor.close()

  return 'init database'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
