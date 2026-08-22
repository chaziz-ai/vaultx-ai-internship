#  -------------------Zero Shot--------------------------- 


def zero_shot_prompt(task_instruction:str,user_input:str) -> list:
    messages = [
        {'role': 'system','content':task_instruction},
        {'role':'user', 'content':user_input}
    ]
    return messages


#  -------------------Few Shot--------------------------- 


examples = [
    ("Product broke on day 1", "Negative"),
    ("Amazing quality!", "Positive")
]


def few_shot_prompt(task_instruction:str,examples:list,user_input:str) -> list:
    messages=[
        {'role':'system','content':task_instruction}
    ]

    for example in examples:
        messages.append({'role':'user',"content":example[0]})
        messages.append({'role':'assistant',"content":example[1]})

    messages.append({'role':'user','content':user_input})
    return messages


    #  -------------------Role/System--------------------------- 


def role_based_prompt(role_description:str,user_input:str) -> list:
    messages=[
        {'role':'system','content':role_description},
        {'role':'user','content':user_input}
    ]
    return messages


    #  -------------------Chain of Thought--------------------------- 


def cot_based_prompt(task_instruction:str,user_input:str) -> list:
    cot_instruction=task_instruction + '\n\nThink step by step before giving your final answer.'
    messages=[
        {"role":'system','content':cot_instruction},
        {'role':'user','content':user_input}
    ]
    return messages

    #  -------------------Constrained Based---------------------------


def constrained_based_prompt(task_instruction:str,output_format:str,user_input:str) -> list:
    constrained_instruction=task_instruction + '\n\n' + output_format
    messages=[
        {'role':'system','content':constrained_instruction},
        {'role':'user','content':user_input}
    ]
    return messages



if __name__=='__main__':
    print('\n ---Zero shot---')
    result1=zero_shot_prompt('Classify sentiment of message',"My order is recienved but it's broken")
    print(result1)

    print('\n ---Few shot---')
    result2=few_shot_prompt('Classify sentiment of message',examples,"My order is recienved but it's broken")
    print(result2)

    print('\n ---Role Based---')
    role='You are a senior customer support agent at a large tech company. You are calm, professional, and empathetic.'
    result3=role_based_prompt(role,"My order is recienved but it's broken")
    print(result3)

    print('\n ---Chain of Thought---')
    result4=cot_based_prompt('Classify the priority of this support ticket as High, Medium, or Low',
                             "I ordered 2 days ago, paid extra for express shipping, still not arrived. Third time this happened")
    print(result4)

    print('\n ---Constrained Output---')
    result5 = constrained_based_prompt(
    "Classify this support message",
    "Respond ONLY with valid JSON in this format: {\"category\": \"string\", \"priority\": \"high|medium|low\", \"sentiment\": \"positive|negative|neutral\", \"needs_human\": true/false}",
    "My order is recienved but it's broken"
    )
    print(result5)