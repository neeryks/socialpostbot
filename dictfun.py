

def dict_fun(text):
    dict_function = {
          "select_all_quotes": "self.select_all_quotes()",
          "add_quotes":"self.add_quotes(regex_arguments['amount'])",
          "quote_audio": "self.quote_audio(regex_arguments['text'])"
        }
    return dict_function[text]
