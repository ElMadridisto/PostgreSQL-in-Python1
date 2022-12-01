import psycopg2

def create_db(conn):
    cur.execute("""
        DROP TABLE phones;
        DROP TABLE clients;
        """)
    cur.execute("""
        CREATE TABLE clients(
            id_client SERIAL PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            surname VARCHAR(80) NOT NULL,
            email VARCHAR(80));
        """)
    cur.execute("""
        CREATE TABLE phones(
            id_phone SERIAL PRIMARY KEY,
            number_phone VARCHAR(80) UNIQUE,
            fk_client_id INTEGER REFERENCES clients(id_client) NOT NULL);
        """)
    print('Create tables')

def add_client(conn, name, surname, email):
    cur.execute("""
        INSERT INTO clients(name, surname, email)
        VALUES (%s,%s,%s); 
        """, (name,surname, email))
    print('Client added')

def add_phone(conn, number_phone, fk_client_id):
    cur.execute("""
        INSERT INTO phones(number_phone, fk_client_id)
        VALUES (%s,%s); 
        """, (number_phone, fk_client_id))
    print('Added customer phone')

def change_client(conn, id_client, data1):
    data = input('Choose what data you want to change(name, surname, email:')
    if data == 'name':
        cur.execute("""
                UPDATE clients
                SET name = %s
                WHERE id_client = %s;
                """, (data1, id_client))
    if data == 'surname':
        cur.execute("""
                UPDATE clients
                SET surname = %s
                WHERE id_client = %s;
                """, (data1, id_client))
    if data == 'email':
        cur.execute("""
                UPDATE clients
                SET email = %s
                WHERE id_client = %s;
                """, (data1, id_client))
    pass

def delete_phone(conn, fk_client_id, number_phone):
    cur.execute('''
            DELETE FROM phones
            WHERE fk_client_id = %s AND number_phone = %s;
        ''', (fk_client_id, number_phone))
    print('Number phone delete')

def delete_client(conn, id_client):
    cur.execute('''
            DELETE FROM phones
            WHERE EXISTS
                (SELECT id_client
                    FROM clients
                    WHERE fk_client_id = %s);
        ''', (id_client,))

    cur.execute('''
                DELETE FROM clients
                WHERE id_client = %s;
            ''', (id_client,))
    print('Client delete')

def tuple_in_list(rows):
  result = []
  for b in rows:
    for c in b:
      if c not in result:
        result.append(c)
  return(result)

def find_client(conn, name=None, surname=None, email=None, number_phone=None):
    cur.execute('''
        SELECT name, surname, email, number_phone
        FROM clients c
        LEFT JOIN phones p ON p.fk_client_id = c.id_client
        WHERE (name=%s OR name IS NULL)
            OR (surname=%s OR surname IS NULL)
            OR (email=%s OR email IS NULL)
            OR (number_phone=%s OR number_phone IS NULL);
    ''', (name, surname, email, number_phone,))
    rows = cur.fetchall()
    print(tuple_in_list(rows))

conn = psycopg2.connect(database='Введите название базы данных', user='Пользователь', password='Пароль')

with conn.cursor() as cur:
    create_db(conn)
    add_client(conn, 'Денис', 'Тихоновский', 'bukaissela@mail.ru')
    add_client(conn, 'Сергей', 'Леднев', 'bukaissela1@mail.ru')
    add_phone(conn, '89104567890', 2)
    add_phone(conn, '89102567458', 1)
    add_phone(conn, '89107684567', 1)
    add_phone(conn, '89102567459', 1)
    change_client(conn, 1, 'but@mail.ru')
    delete_phone(conn, 1, '89107684567')
    delete_client(conn, 2)
    find_client(conn, name='Денис')

    conn.commit()
conn.close()
