
def function_list():
    list_of_functions = [
        {
      "name": "select_all_quotes",
      "description": "get all the Quotes from the database",
      "parameters": {
        "type": "object",
        "properties": {
          "Quotes": {
            "type": "string",
            "description": "String of quotes"
          },
        },
      }
    }
    ]
       
    return list_of_functions