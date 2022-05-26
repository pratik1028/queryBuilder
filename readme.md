1. Install requirements.txt </br>
```
    pip install requirements.txt
```

2. Run the django server </br>
```
    python manage.py runserver 8000
```
3. Following API's:</br>
    1. SQL:
   ```
    http://127.0.0.1:8000/get_query
    body: {
            "input_query": "(Java AND python) OR (Ruby AND ('ruby on rails' AND ('ruby on rails' OR (ROR AND pyhton))))",
            "output_format": "SQL"
          }
    response: {"SQL_Query": "SELECT * FROM resume WHERE (text RLIKE \"Java\" AND text RLIKE \"python\") OR (text RLIKE \"Ruby\" AND (text RLIKE \"ruby on rails\" AND (text RLIKE \"ruby on rails\" OR (text RLIKE \"ROR\" AND text RLIKE \"pyhton\"))))"}
      ```
    2. MONGO:
   ```
    http://127.0.0.1:8000/get_query
    body: {
            "input_query": "(Java AND python) OR (Ruby AND ('ruby on rails' AND ('ruby on rails' OR (ROR AND pyhton))))",
            "output_format": "MONGO"
          }
    response: {"MONGO_Query": "db.resume.find({\"$OR\": [{\"$AND\": [{\"$AND\": [{\"$OR\": [{\"$AND\": [{\"text\": \"/.*pyhton.*/\"}, {\"text\": \"/.*ROR.*/\"}]}, {\"text\": \"/.*ruby on rails.*/\"}]}, {\"text\": \"/.*ruby on rails.*/\"}]}, {\"text\": \"/.*Ruby.*/\"}]}, {\"$AND\": [{\"text\": \"/.*python.*/\"}, {\"text\": \"/.*Java.*/\"}]}]})"}
      ```
   3. ORM:
   ```
    http://127.0.0.1:8000/get_query
    body: {
            "input_query": "(Java AND python) OR (Ruby AND ('ruby on rails' AND ('ruby on rails' OR (ROR AND pyhton))))",
            "output_format": "MONGO"
          }
    response: {"ORM_Query": ["abc xyz"] // name of matching candidate}
   ```
