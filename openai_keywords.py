import openai


class OpenaiKeywords():

    def __init__(self) -> None:
        openai.api_key_path = "api_key.txt"

    def __get_text(self) -> str:
        text = ""
        with open('transcript.txt', 'r') as f:
            text = f.read()

        return text

    def get_keywords(self):

        prompttext = self.__get_text()

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="What are the top 10 keywords for "+prompttext+"?",
            temperature=0.3,
            max_tokens=800,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        return response["choices"][0]["text"]


if __name__ == "__main__":
    pass