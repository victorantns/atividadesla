import os
import psycopg2


conn = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS sensors;')
cur.execute('CREATE TABLE sensors (id serial PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'description text NOT NULL,'
                                 'token varchar(200) NOT NULL,' 
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO sensors (name, description, token)'
            'VALUES (%s, %s, %s)',
            ('Sonar ração granja 1',
             'Sonar que identifica a quantidade de ração no silo da granja 1',
             'asa3tea3f3t35efa3ta4g34a'
              )
            )

cur.execute('INSERT INTO sensors (name, description, token)'
            'VALUES (%s, %s, %s)',
            ('Temperatura aviário 2',
             'Sensor de temperatura interna do aviário 2',
             'asa3tea3f3asffa3ta4g34a'
              )
            )

cur.execute('INSERT INTO sensors (name, description, token)'
            'VALUES (%s, %s, %s)',
            ('Umidade do ar aviário 2',
             'Sensor de umidade do aviário 2',
             'asa3ta3ffeaefa3ta4g34a'
              )
            )





conn.commit()

cur.close()
conn.close()