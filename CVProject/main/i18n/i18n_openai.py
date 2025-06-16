import openai
import environ

env = environ.Env()
environ.Env.read_env()

api_key = env('OPEN_AI_TOKEN')
model = "gpt-4o-mini"

# Available list of languages with ISO 639-3 international codes
languages = [
    {'code': 'eng', 'language': 'English'},
    {'code': 'crn', 'language': 'Cornish'},
    {'code': 'gvn', 'language': 'Manx'},
    {'code': 'bre', 'language': 'Breton'},
    {'code': 'ikt', 'language': 'Inuktitut'},
    {'code': 'kal', 'language': 'Kalaallisut'},
    {'code': 'rom', 'language': 'Romani'},
    {'code': 'oci', 'language': 'Occitan'},
    {'code': 'lad', 'language': 'Ladino'},
    {'code': 'xsn', 'language': 'Northern Sarni'},
    {'code': 'hsb', 'language': 'Upper Sorbian'},
    {'code': 'csb', 'language': 'Kashubian'},
    {'code': 'zaz', 'language': 'Zazaki'},
    {'code': 'chv', 'language': 'Chuvash'},
    {'code': 'liv', 'language': 'Livonian'},
    {'code': 'tsk', 'language': 'Tsakonian'},
    {'code': 'sam', 'language': 'Saramaccan'},
    {'code': 'bis', 'language': 'Bislama'},
]


def translate_list(strings, target_language):
    # Preparing the OpenAI client and message
    client = openai.OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": f"You are a strict assistant that translates text to {target_language}."},
        {"role": "user", "content": f"Translate the following list of strings and return the list with no heading:\n\n{strings}"}
    ]

    # Sending the API request
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    translation = completion.choices[0].message.content

    # Attempt to split the response into a list if it's formatted that way
    try:
        translated_list = eval(translation)
        if isinstance(translated_list, list):
            return translated_list
    except Exception as e:
        print(f"Failed to evaluate the list from response:\n  {e}")
        print(f"Response:\n  {translation}")
    return None
