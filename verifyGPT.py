import json


def wrap_context_question_answers_GPTanswer_rate(context, question, answers, GPTanswer, success_rate):
    return {"context": context, "question": question, "answers": answers, "GPTanswer": GPTanswer,
            "succsees_rate": success_rate}


BLUE = '\033[94m'
RED = '\033[91m'
PURPLE = '\033[95m'


def print_possible_answers(possible_answers):
    print(BLUE + "possible_answers")
    for entry in possible_answers:
        print(entry['text'])


def print_model_answer(model_answer):
    print(RED + "model_answers:")
    print(model_answer)


def print_to_user():
    print(PURPLE + "Press y if the answer is correct")


def is_possible_answer(model_answer, possible_answers):
    for entry in possible_answers:
        if entry['text'].lower() == model_answer.lower():
            return True
        if entry['text'].lower() + "." == model_answer.lower():
            return True
        if "\"" + entry['text'].lower() + "\"" == model_answer.lower():
            return True
    return False


def add_to_possible_answers(model_answer, possible_answers):
    possible_answers.append({'text': model_answer})


def add_to_wrong_answers(model_answer, wrong_answers):
    wrong_answers.append(model_answer)
    wrong_answers.append(model_answer + ".")


def verify_answers(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("The file was not found.")
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")
    answers_to_verify = data
    for entry in answers_to_verify:
        possible_answers = entry['answers']
        wrong_answers = []
        model_answers = entry['GPTanswer']
        correct_count = 0
        for model_answer in model_answers:
            if not model_answer in wrong_answers:

                if is_possible_answer(model_answer, possible_answers):
                    correct_count = correct_count + 1
                else:
                    print_possible_answers(possible_answers)
                    print_model_answer(model_answer)
                    print_to_user()
                    while True:
                        usrInput = input("Enter a single character as input: ")
                        if len(usrInput) == 1:
                            print(f'Your single character input was: {usrInput}')
                            if usrInput == 'y':
                                correct_count = correct_count + 1
                                add_to_possible_answers(model_answer, possible_answers)
                            else:
                                add_to_wrong_answers(model_answer, wrong_answers)
                            break
                        print("Please enter a single character to continue\n")
        success_rate = correct_count / len(model_answers)
        entry.update({"succsees_rate": success_rate})
        print(entry)
    # Writing the list of dictionaries to a JSON file
    with open(output_file_path, 'w') as file:
        json.dump(answers_to_verify, file, indent=4)
    print(f"List of dictionaries saved to {output_file_path}")


file_path = "model=gpt-4-0613prompt=p1_input=imaginary_if_no.json"
input_file_path = "OUTPUT/"+file_path
output_file_path = "VERIFIED_OUTPUT/"+file_path

verify_answers(input_file_path)
