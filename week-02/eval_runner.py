from eval_set import eval_set
from structured_output import get_structured_ticket

def eval_run(eval_set):
    all_results=[]

    for case in eval_set:
        input_message=case['input']
        expected=case['expected']

        ticket=get_structured_ticket(input_message)

        if ticket is None:
            case_result={
                'input':input_message,
                'expected':expected,
                'actual':None,
                'correct_fields':0,
                'exact_match':False
            }
        else:
            ticket_dict=ticket.model_dump()

            correct_field=0

            for field in expected:
                if ticket_dict[field]==expected[field]:
                    correct_field+=1

            exact_match=correct_field==len(expected)

            case_result={
                'input': input_message,
                'expected': expected,
                'actual': ticket_dict,
                'correct_fields': correct_field,
                'exact_match': exact_match
            }

        all_results.append(case_result)

    return all_results

if __name__=='__main__':
    results=eval_run(eval_set)
    count_correct = sum(r['exact_match'] for r in results)
    accuracy = (count_correct ) / (len(results)) * 100
    print(f"Accuracy: {accuracy}%")

print("\n--- Failed Cases ---")
for r in results:
    if r['exact_match'] == False:
        print(f"Input: {r['input']}")
        print(f"Expected: {r['expected']}")
        print(f"Actual: {r['actual']}")