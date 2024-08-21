from openai import OpenAI
import json

client = OpenAI(
    organization='org-bEZxJ55dx3RaRijsY8IOlW21',
    project='proj_FCStOPo4SHooGzqKmC5YVoEg',
    api_key='sk-proj-t2NlocYPXURGYg362k5sT3BlbkFJxaMa12BDTXEoyjH1FFpK'
)


def extract_context_question_answers(data):
    paragraphs = data['paragraphs'][0]
    context = paragraphs['context']
    qas = paragraphs['qas'][0]
    question = qas['question']
    answers = qas['answers']
    return context, question, answers


def wrap_context_question_answers_GPTanswer(context, question, answers, GPTanswer):
    return {"context": context, "question": question, "answers": answers, "GPTanswer": GPTanswer}


def generate_p1(context, question):
    return (f"Text:{context} Question: “{question}”. Shortest possible answer please. If the question cannot be "
            f"answered with a singlespan from the text, return “None”")


def generate_p2(context, question):
    return (f"Text:“{context}” Question: “{question}” Important! The answer should be an exact span extracted from the "
            f"text. Important! Give the shortest possible answer. If the question cannot be answered with one span from "
            f"the text - return “None” (and nothing else). Answer:")


# files_names={"contradicting_because.json","contradicting_if_yes.json","imaginary_because.json","imaginary_if_yes.json","supported_because.json","supported_if_yes.json"}
files_names = {"imaginary_because.json"}#"imaginary_because.json", "imaginary_if_yes.json", "imaginary_if_no.json", "imaginary_after.json"}

# model = "gpt-3.5-turbo-0125"
model = "gpt-4-0613"


def askGPT(path, model, generate_prompt):
    print(path)
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("The file was not found.")
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")
    question_bank = data["data"]

    GPT_answers = []

    for i in range(len(question_bank)):
        context, question, answers = extract_context_question_answers(question_bank[i])
        prompt1 = generate_prompt(context, question)
        listGPTanswers = []
        print(prompt1)
        for i in range(10):
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt1}],
                stream=True,
            )
            GPTanswer = ""

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    GPTanswer = GPTanswer + chunk.choices[0].delta.content
                    # print(chunk.choices[0].delta.content, end="")
            print("GPT answer:" + GPTanswer, end='\n')
            listGPTanswers.append(GPTanswer)
        GPT_answers.append(wrap_context_question_answers_GPTanswer(context, question, answers, listGPTanswers))
        print("\n next question:\n")
    print(GPT_answers)

    file_path = 'OUTPUT\\model=' + model + 'prompt=p1_input=' + file_name

    # Writing the list of dictionaries to a JSON file
    with open(file_path, 'w') as file:
        json.dump(GPT_answers, file, indent=4)
    print(f"List of dictionaries saved to {file_path}")


for file_name in files_names:
    askGPT('INPUT\\' + file_name, model, generate_p1)
