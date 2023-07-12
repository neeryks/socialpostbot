
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
            "type": "string",
            "description": "the number of quotes that need to be inserted"
          }
        }

      }
    },
    {
      "name": "image_maker",
      "description": "makes a image with a quote on it , the quote is given as a parameter",
      "parameters": {
        "type": "object",
        "properties": {
          "quote": {
            "type": "string",
            "description": "the quote that needs to be inserted into the image"
          },
          "sizeofimage": {
            "type": "string",
            "description": "the size of the image that needs to be created ,it will be either 'tall' or 'short' if nother is given it will be short"
          }
        },
      },
    },
    {
      "name": "video_maker",
      "description": "makes a video with a quote on it , the quote is given as a parameter and the video id is also given as a parameter",
      "parameters": {
        "type": "object",
        "properties": {
          "quote": {
            "type": "string",
            "description": "the quote that needs to be inserted into the image"
          },
          "idofvideo": {
            "type": "integer",
            "description": "the id of the video that needs to be downloaded"
          }
        }
      },
    },
    ]
       
    return list_of_functions