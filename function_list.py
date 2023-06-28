
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
    },
    {
      "name": "add_quotes",
      "description": "Automatically insert or adds quotes into the database with the amount of quotes you want",
      "parameters": {
        "type": "object",
        "properties": {
          "Quotes": {
            "type": "string",
            "description": "String of quotes"
          },
          "amount": {
            "type": "integer",
            "description": "Amount of quotes you want to insert"
          }
        },
        "required": ["amount"]
      }
    }
    ]
       
    return list_of_functions