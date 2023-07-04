
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
      "name": "quote_audio",
      "description": "converts the text that is given into audio",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "description": "the text that needs to be converted to audio"
          },
        }
      },
    },
    {
      "name": "add_quotes",
      "description": "inserts a specific number of quotes into the database",
      "parameters": {
        "type": "object",
        "properties": {
          "amount": {
            "type": "integer",
            "description": "the number of quotes that need to be inserted"
          }
        }

      }
    }
    ]
       
    return list_of_functions