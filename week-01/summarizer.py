import argparse
from api_wrapper import APIWrapper

parser=argparse.ArgumentParser(description='CLI tool that summarizes text and gives key points and sentiment')

group=parser.add_mutually_exclusive_group(required=True)
group.add_argument('--file',help='Path to a text file to summarize')
group.add_argument('--text',help='Text to summarize, provided directly in the terminal')

args=parser.parse_args()

if args.file:
    print(f'You gave a file: {args.file}')
    with open(args.file,'r') as f:
        input_text=f.read()
else:
    print(f'You gave text: {args.text}')
    input_text=args.text


if __name__=='__main__':
    wrapper=APIWrapper()
    prompt=f'Please do 4 lines summary, 3 key points and sentiment with this {input_text},Give anser in this format: Summary:  ,Key points: , Sentiment:  '
    result=wrapper.send_message (prompt)
    if result is not None:
        print(result.choices[0].message.content)
    else:
        print('No response recieved')