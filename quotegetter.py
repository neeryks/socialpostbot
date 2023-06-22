import openai
import mysql.connector
import savedfile

class Quote_Getter:
  def __init__(self):
    pass

  def get_quote(self,amount):

    openai.api_key = savedfile.openai_key()
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0613",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"give me {amount} unique motivational quote"}]
    )
    quotes = [self.splitter(x) for x in completion.choices[0].message["content"].split("\n") if x != ""]
    return quotes

  def splitter(self,quote):
    quote = quote.split('"')[1]
    quote = quote.split('"')[0]
    return quote


class Sql_Query(Quote_Getter):

  def __init__(self):
    self.mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="H.no194/3A",
    database="quote_db")


  def insert_quotes_auto(self,amount):
    cursor = self.mydb.cursor()
    for quo in self.get_quote(amount):
      cursor.execute(f'INSERT INTO quotes (Quotes) VALUES ("{quo}");')
      self.update_Used("No",cursor.lastrowid)
      self.mydb.commit()
      print(cursor.rowcount, "records inserted.")

  def insert_quote(self,quote):
    cursor = self.mydb.cursor()
    cursor.execute(f"INSERT INTO quotes (Quotes) VALUES ('{quote}');")
    self.update_Used("No",cursor.lastrowid)
    self.mydb.commit()
    print(cursor.rowcount, "records inserted.")

  def show_databases(self):
    cursor = self.mydb.cursor()
    cursor.execute("SHOW DATABASES")
    for x in cursor:
      print(x)

  def show_columns(self):
    cursor = self.mydb.cursor()
    cursor.execute("SHOW COLUMNS FROM quotes")
    for x in cursor:
      print(x)

  def delete_table(self):
    cursor = self.mydb.cursor()
    cursor.execute("DROP TABLE quotes")
    self.mydb.commit()
    print(cursor.rowcount, "record(s) deleted")

  def select_all_quotes(self):
    cursor = self.mydb.cursor()
    cursor.execute("SELECT * FROM quotes")
    myresult = cursor.fetchall()
    for x in myresult:
      print(x[0])
    return myresult
  
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

get = Sql_Query()
for i in range(1,11):
  get.update_Used("No",i)