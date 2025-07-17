from llm_helper import llm


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag, subject):
    prompt = get_prompt(length, language, tag, subject)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, subject):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    4) More Context: {subject}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health","How yoga affect sleep cycle ?"))