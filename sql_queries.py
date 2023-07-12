import mysql.connector

class Sql_Query():
  
  def __init__(self):
    self.mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="H.no194/3A",
    database="quote_db")


  def insert_quotes_auto(self,data):
    cursor = self.mydb.cursor()
    rc = 0
    for quo in data:
      print(quo)
      cursor.execute(f'INSERT INTO quotes (Quotes) VALUES ("""{quo}""");')
      self.update_Used("No",cursor.lastrowid)
      rc += cursor.rowcount
      print(rc)
    self.mydb.commit()
    return f"{rc} records inserted."

  def insert_quote(self,quote):
    cursor = self.mydb.cursor()
    cursor.execute(f"INSERT INTO quotes (Quotes) VALUES ('{quote}');")
    self.update_Used("No",cursor.lastrowid)
    self.mydb.commit()
    return cursor.rowcount, "records inserted."

  def show_databases(self):
    cursor = self.mydb.cursor()
    cursor.execute("SHOW DATABASES")
    list_db= "\n".join(list(map(lambda x: x[0],cursor.fetchall())))
    return list_db

  def show_columns(self):
    cursor = self.mydb.cursor()
    cursor.execute("SHOW COLUMNS FROM quotes")
    list_columns= "\n".join(list(map(lambda x: x[0],cursor.fetchall())))
    return list_columns
    
  def delete_table(self):
    cursor = self.mydb.cursor()
    cursor.execute("DROP TABLE quotes")
    self.mydb.commit()
    print(cursor.rowcount, "record(s) deleted")

  def select_all_quotes(self):
    cursor = self.mydb.cursor()
    cursor.execute("SELECT * FROM quotes")
    myresult = cursor.fetchall()
    quote_list = "\n".join(list(map(lambda x: x[0],myresult)))
    return quote_list
  
  def select_quote_byid(self,id):
    cursor = self.mydb.cursor()
    cursor.execute(f"SELECT Quotes FROM quotes WHERE id = {id};")
    quote_one = cursor.fetchone()
    for quo in quote_one:
      print(quo[0])
  
  def select_quote_byUsed(self,used, Limit):
    cursor = self.mydb.cursor()
    cursor.execute(f"SELECT Quotes FROM quotes WHERE Used = '{used}' LIMIT {Limit};")
    quote_one = cursor.fetchall()
    for quo in quote_one:
      print(quo[0])

  def delete_quote(self,id):
    cursor = self.mydb.cursor()
    cursor.execute(f"DELETE FROM quotes WHERE id  = {id};")
    self.mydb.commit()
    print(cursor.rowcount, "record(s) deleted")

  def update_quote(self,newquote,ids):
    cursor = self.mydb.cursor()
    cursor.execute(f"UPDATE quotes SET Quotes = '{newquote}' WHERE id = {ids};")
    self.mydb.commit()
    print(cursor.rowcount, "record(s) affected")

  def add_column(self,name):
    cursor = self.mydb.cursor()
    cursor.execute(f"ALTER TABLE quotes ADD COLUMN {name} VARCHAR(255)")
    self.mydb.commit()
    print(cursor.rowcount, "record(s) affected")

  def using_quote(self):
    cursor = self.mydb.cursor()
    cursor.execute("SELECT Quotes, id FROM quotes WHERE Used = 'No' LIMIT 1;") 
    myresult = cursor.fetchall()
    for result in myresult:
      result = result[0]
      print(result)
    self.update_Used("Yes",myresult[0][1])
    return result
  
  def update_Used(self,used,ids):
    cursor = self.mydb.cursor()
    cursor.execute(f"UPDATE quotes SET Used = '{used}' WHERE id = {ids};")
    self.mydb.commit()
    print(cursor.rowcount, "record(s) affected")
    self.mydb.commit()

  def show_column_used(self):
    cursor = self.mydb.cursor()
    cursor.execute("SELECT Used FROM quotes")
    myresult = cursor.fetchall()
    for result in myresult:
      print(result[0])


if __name__ == "__main__":
  sql = Sql_Query()
  for i in range(1,11):
    sql.update_Used("No",i)