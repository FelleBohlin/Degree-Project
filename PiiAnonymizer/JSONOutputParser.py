from langchain_core.output_parsers import OutputParser

class JSONOutputParser(OutputParser):
    def parse(self, response):
        # Assumes the response is a JSON object that includes a 'choices' list
        try:
            # Trying to parse the first choice's 'message' content
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            raise ValueError("Failed to parse JSON response: " + str(e))
