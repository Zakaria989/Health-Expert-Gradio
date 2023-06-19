import gradio as gr
import openai
import os


openai.api_key = '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'

file_path_context = os.getcwd() + "/context.txt"
file_path_context_history = os.getcwd() + "/context_history.txt"



with open(file_path_context,"r") as file:
    context = [line.rstrip() for line in file.readlines()]
    context = "\n".join(context)
    
with open(file_path_context_history,"r") as file:
    context_history = [line.rstrip() for line in file.readlines()]
    context_history = "\n".join(context_history)


def add_values_to_file(file_path, values):
    # Read the existing content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Prepend the new values to the content
    content = content + values

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(content)
        
def context_shortener(file_path):
    """
    Takes a file path, reads its content, and if it exceeds 4 inputs divided by | remove the first one.
    """
    char_val = "|"
    with open(file_path, "r") as file:
        content = [line.rstrip() for line in file.readlines()]
        content = "\n".join(content)

    list_of_index = [pos for pos, char in enumerate(content) if char == char_val]

    if len(list_of_index) >= 4:
        print(f"We got {list_of_index} {char_val}")
        content = content.split(char_val, 1)[-1]  # Removes the first |, but keeps the rest

    with open(file_path, "w") as file:
        file.write(content)


class OpenAI_Session():
        
    
    """
     Class for represents an OpenAI session and provides a simple syntax for requesting a response from the AI chatbot.
    """
    def __init__(self, context_description,context_history_description):
        self.message_history = [
            {"role": "system", "content": context_description},
            {"role":"system", "content": context_history_description}
            ]
        
    """
        Initializes an OpenAI session with the given context description and replacements, replacements can be set to none, truncate and smart
    """
    
    def chat_completion(self,message):
        
        """
        Sends a user message to the OpenAI chatbot and returns the bots response.
        """
                
        user_question = {"role": "user", "content": message}
        self.message_history.append(user_question)
        chat = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = self.message_history)
        reply = chat.choices[0].message.content
        assistant_answer = {"role":"assistant", "content":reply}
        self.message_history.append(assistant_answer)
        
        context_history_description =  user_question.get("role") + " : "+ user_question.get("content") + " " + assistant_answer.get("role") + " : " + assistant_answer.get("content") + " | \n\t"
        add_values_to_file(file_path_context_history, context_history_description )
        context_shortener(file_path_context_history)
        print(context)
        return reply
    
    

class FactoryBot():
    
    """
        Our factory bot that interacts with the assistant
    """
    
    def __init__(self, session):
        """
            Initializes the assistant with OpenAI session
        """
        self.session = session
    
    
    def session_start(self,question):
        def headline(str):
            return "\n" + str 
        yield self.session.chat_completion(question)
        
        

        
def run(question):
    """
        Runs the factorybot session and returns the total response
    """
    session = OpenAI_Session(context, context_history)
    bot = FactoryBot(session)
    total_response = ""
    for response in bot.session_start(question):
        print(response)
        total_response += response
    return total_response






def input_question(question):
    return  run(question)

demo = gr.Interface(fn=input_question, inputs="text", outputs="text")

demo.launch()   



# def create_blocks_ui():
#     def block_run(el):
#         """parameter el: dictinary of element values indexed by element"""
#         return run(el[product], el[spec], el[optimize_for], el[parameters], GRADIO_LATEX_REPLACEMENTS)
        
#     with gr.Blocks() as ui:
#         product = gr.components.Textbox(label="What is the product to evaluate")
#         spec = gr.components.Textbox(label="Describe the design and requirements", lines=4)
#         optimize_for = gr.components.Textbox(label="Which parameters to optimize for, e.g. low cost, durability")
#         parameters = gr.components.Textbox(label="Parameters to evaluate (separated by comma)")
#         go = gr.Button("Report")
#         examples=gr.Examples([[EX_PRODUCT, EX_SPEC, EX_OPTIMIZE_FOR, EX_PARAMETERS]], [product, spec, optimize_for, parameters])

#         analysis = gr.components.Markdown(value=" ", label="Analysis")
#         go.click(fn=block_run, inputs={product, spec, optimize_for, parameters}, outputs=analysis),
#     return ui


# ui = create_blocks_ui()
# ui.launch()