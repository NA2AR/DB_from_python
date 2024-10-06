import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    DROP TABLE phones;
                    DROP TABLE info;
                    """)
        cur.execute("""
                    CREATE TABLE info(
                        id SERIAL PRiMARY KEY,
                        first_name VARCHAR(60) NOT NULL,
                        last_name VARCHAR(60) NOT NULL,
                        email VARCHAR(60) NOT NULL
                            );
                    """)
        cur.execute("""
                    CREATE TABLE phones(
                        client_id int REFERENCES info(id),
                        phone INTEGER 
                            );
                    """)
        conn.commit()

def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO info(first_name, last_name, email)
                    VALUES(%s,%s,%s);
                    """,(first_name, last_name, email))
        conn.commit()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO phones(client_id, phone)
                    VALUES(%s, %s);
                    """,(client_id, phone))
        conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute("""
                        UPDATE info 
                        SET first_name = %s
                        WHERE id = %s;
                        """,(first_name, client_id))
        if last_name != None:
            cur.execute("""
                        UPDATE info 
                        SET last_name = %s
                        WHERE id = %s;
                        """,(last_name, client_id))

        if email != None:
            cur.execute("""
                        UPDATE info 
                        SET email = %s,
                        WHERE id = %s;
                        """,(email, client_id))

def change_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                    UPDATE phones
                    SET phone = %s
                    WHERE client_id  = %s;
                    """,(phone, client_id))
        conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM phones
                    WHERE client_id = %s AND phone = %s
                    """,(client_id, phone))
    conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM info
                    WHERE id = %s
                    """,(client_id))

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT * FROM info  
                    WHERE first_name = %s AND last_name = %s AND email = %s            
                    """,(first_name, last_name, email))
        print(cur.fetchall())


with psycopg2.connect(database="db_python", user="postgres", password="rfhfrfnbwf1975") as conn:
    create_db(conn)
    add_client(conn, 'Ivan','Vanko','IvV@mail.py')
    add_phone(conn, '1', '11111111')
    change_client(conn, '1', 'Oleg' ,'Volkov', None)
    change_phone(conn,'1','2222222')
    delete_phone(conn,'1', '2222222')
    delete_client(conn,'1')
    find_client(conn, 'Oleg')
conn.close()

