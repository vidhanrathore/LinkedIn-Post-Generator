from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag, subject, post_style):
    prompt = get_prompt(length, language, tag, subject, post_style)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, subject, post_style=''):
    length_str = get_length_str(length)
    post_style_part = ''
    if post_style.strip():
        post_style_part = f'''5) Use the writing style as per the following example.
    Example: {post_style}'''
    
    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    4) More Context: {subject}
    {post_style_part}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    return prompt


if __name__ == "__main__":
    # print(generate_post("Medium", "English", "Mental Health"))
    print(get_prompt("Short", "English","marketing","how to sell","  "))
    