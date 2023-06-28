import openai
import savedfile
from function_list import function_list
from regex import regex as re
from sql_queries import Sql_Query


class Quote_Getter(Sql_Query):
  def __init__(self,query):
    super().__init__()
    self.query = query
  
  def query_ai(self):
    openai.api_key = savedfile.openai_key()
    completion = openai.ChatCompletion.create( 
      model="gpt-3.5-turbo-0613",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{self.query}"},],
      functions=function_list())

    response = completion.choices[0].message
    return response
  
  def query_sort(self):
    response=self.query_ai()
    print(response)
    try:
      regex_arguments = re.sub(r"\t|\n|\r|\ |", '', response["function_call"]["arguments"])
      print(regex_arguments)

      dict_function = {
          "select_all_quotes": self.select_all_quotes(),
          "add_quotes":self.add_quotes(regex_arguments["amount"]),
        }
  
      function_call = response["function_call"]
      function_name = function_call["name"]
      data = dict_function[function_name]
      #data = self.add_quotes(regex_arguments["amount"])
      print(data)
      return data

    except:
      return response["content"]
    
  def answer_back(self):
    data = self.query_sort()
    return str(data)
  
  def add_quotes(self,amount):
    data = self.query_ai(f"Get me {amount} motivational quotes")
    data_list = list(map(lambda x: x[1],data.split("\n")))
    print(data_list)
    return self.insert_quotes_auto(data_list)
  
  

