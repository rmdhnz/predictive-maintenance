import mysql.connector

class DB : 
  def __init__(self,host,user,password,db_name):
    self.conn = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
    )
    self.cursor = self.conn.cursor(True)

  def find_all(self,table) : 
    self.cursor.execute(f'SELECT * FROM {table}')
    return self.cursor.fetchall()

  def find_by_id(self,table,id_value,id_field='id') :
    query = f"SELECT * FROM {table} WHERE {id_field} = {id_value}"
    self.cursor.execute(query)
    return self.cursor.fetchone()

  def where(self,table,conditions: dict) :  
    keys = list(conditions.keys())
    values = list(conditions.values())
    where_clause =  " AND ".join([f"{k} = %s" for k in keys])
    query = f"SELECT * FROM {table} WHERE {where_clause}"
    self.cursor.execute(query, tuple(values))
    return self.cursor.fetchall()
  
  def select_field(self,table,fields:list,where:dict = None) : 
    field_clause = ", ".join(fields)
    query = f"SELECT {field_clause} FROM {table}"
    values = ()
    if where : 
      where_clause = " AND ".join([f"{k} = %s" for k in where.keys()])
      query += f" WHERE {where_clause}"
      values = tuple(where.values())
    
    self.cursor.execute(query, values)
    return self.cursor.fetchall()
  

  def close(self) : 
    self.cursor.close()
    self.conn.close()