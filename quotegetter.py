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
      self.mydb.commit()
      print(cursor.rowcount, "records inserted.")

  def insert_quote(self,quote):
    cursor = self.mydb.cursor()
    cursor.execute(f"INSERT INTO quotes (Quotes) VALUES ('{quote}');")
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
  
  def select_quote(self,id):
    cursor = self.mydb.cursor()
    cursor.execute(f"SELECT Quotes FROM quotes WHERE id = {id};")
    quote_one = cursor.fetchone()
    for quo in quote_one:
      print(quo)

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
