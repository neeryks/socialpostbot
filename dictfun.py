

def dict_fun(text):
    dict_function = {
          "select_all_quotes": "self.select_all_quotes()",
          "add_quotes":"self.add_quotes(regex_arguments['amount'])",
          "quote_audio": "self.quote_audio(regex_arguments['text'])",
          "image_maker": "self.image_maker(regex_arguments['quote'],regex_arguments['sizeofimage'])",
          "video_maker": "self.video_maker(regex_arguments['quote'],regex_arguments['idofvideo'])",
        }
    return dict_function[text]
