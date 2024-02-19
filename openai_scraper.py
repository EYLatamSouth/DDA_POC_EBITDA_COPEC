import os
import openai

class OpenAI:
  def __init__(self):
    openai.api_type = "azure"
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = "2023-07-01-preview"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    self.prompt = """
            Para el siguiente texto enviame en formato json, el kpi financiero que se menciona junto con su periodo , su monto y moneda. Por ejemplo si dice: 'los costos operacionales del primer trimestre del año 2021 fueron 21MMCLP', esto debe retornar siempre este formato: {'kpi': 'costos operacionales', 'periodo': '1T21', 'monto': '21.000.000.000', 'moneda': 'CLP'}. Si no se menciona ningún kpi financiero en el texto proporcionado retorna 'None'.: 
            """

  def get_response(self, message):
    message_text = [{"role":"user","content": self.prompt + message}]
    completion = openai.ChatCompletion.create(
      engine="pdf_scraper",
      messages = message_text,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    return completion.choices[0].message['content']
  

if __name__ == "__main__":
  # message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."}]
  message = ""
  while(message != "exit"):
    message = input("You: ")
    message_text = [{"role":"user","content":message}]
    completion = openai.ChatCompletion.create(
      engine="pdf_scraper",
      messages = message_text,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    print(completion.choices[0].message['content'])