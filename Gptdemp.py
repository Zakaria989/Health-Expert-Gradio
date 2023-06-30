import gradio as gr
import openai
import os
import time
import re



openai.api_key = 'sk-'

file_path_context = os.getcwd() + "/user_context.txt"
file_path_context_history = os.getcwd() + "/context_history.txt"

user_sex = ""
user_name = ""
user_birth_date = ""
user_age = 0
user_weight = 0.0
user_height = 0.0
user_bmi = 0.0
user_emoji = "🤠"

meal_plan = ""
workout_plan = ""




with open(file_path_context,"r",  encoding="utf8") as file:
    context = [line.rstrip() for line in file.readlines()]
    context = "\n".join(context)
    
with open(file_path_context_history,"r",  encoding="utf8") as file:
    context_history = [line.rstrip() for line in file.readlines()]
    context_history = "\n".join(context_history)

def calculate_bmi(weight, height):
    weight = float(weight)
    height = float(height)
    
    if height == 0.0 or weight == 0.0:
        bmi = 0
    else:
        bmi = (weight / (height*height))*10000
    return bmi


def calculate_age(birth_date):
    
    if birth_date == "":
        age = 0
    else:
        birth_time = time.strptime(birth_date, "%d.%m.%Y")
        current_time = time.localtime()
        age = current_time.tm_year - birth_time.tm_year
    
        if current_time.tm_mon < birth_time.tm_mon or (current_time.tm_mon == birth_time.tm_mon and current_time.tm_mday < birth_time.tm_mday):
                    age -= 1
        
    return round(age,2)

def meal_planner_prompt(diet_preference,snack_preference, meal_amount_preference, other_preference ):
    prompt = f'''
Create a meal plan for seven days, where for each day there is only {meal_amount_preference}, so for monday {meal_amount_preference} and so on. 
Make the calorie amount fitting for each person, with each meal amount. We dont want them to lose or gain weight.
the snack amount for each day is {snack_preference}.
The person who we are making the plan for has a diet preference like {diet_preference}, other preferences are {other_preference} 
please adhere to those preferences.

Make it clear how much protein, fat, and carbohydrate they need to reach their goal and then steering them towards an app like myfitnesspal (link takes you to site), 
that makes it easy for them to easily log the details can make a huge difference to people’s lives.
    '''
    assistant_answer = respond_bot(prompt)
    
    return assistant_answer


def workout_planner_prompt(amount_of_days, workout_intensity,cardio_option, strength_training, workout_duration, other_factors):
    prompt = f'''
Create a workout plan for the next month with the following specifications:
- Amount of days for working out: {amount_of_days}
- Workout intensity: {workout_intensity}
- Workout duration: {workout_duration}
- Workout type : {strength_training}
- Other factors to consider: {other_factors} + {cardio_option}

Design a workout plan that aligns with the given specifications and provides effective results.
    '''
    assistant_answer = respond_bot(prompt)
    return assistant_answer



def recipie_prompt(recipe, portions):
    
    diffouclty_of_recipie_prompt = f''''
What is the diffcuilty of this recipie {recipe}
give me the rating in terms off:
Level 1: The easiest of the levels. This level does not contain alcohol or require the use of a heat source (stove, grill, etc) making it safe for children to prepare with limited assistance. 
    Contains only a limited number of ingredients and steps to complete the recipe.

Level 2: Very easy but may require the use of a heat source and may contain alcohol. Easy to find ingredients and simple steps involved in making the recipe. 
    Older children may be able to make (non-alcoholic!) recipes that fall into this category. Recipes can usually be made by people with little to no cooking experience.
Level 3: Average. The majority of the recipes on CDKitchen fall into this category. Most recipes will require basic cooking skills (chopping, dicing, measuring, use of small appliances, etc)
    and contain ingredients that most home cooks have access to in regular grocery stores. This by no means indicates these recipes don't fall under the category of "gourmet", it just usually means the work involved isn't as hard as it sounds.
Level 4: Above-average. These recipes either contain harder to find ingredients (that require a specialty store), more advanced cooking skills, or unusual tools needed to prepare the recipe.
    Many of the recipes can be made by an "average" cook but finding some of the ingredients may take some extra shopping. Some of the recipes contain basic ingredients but require extra cooking skills or special tools. 
    Recipes that may contain significantly more preparation and assembly steps may also fall into this category.
Level 5: Difficult. For those looking for a challenge! These recipes usually contain unusual ingredients and require advanced cooking skills or elaborate preparations. 
    Not all recipes in this category are impossible but rather require more dedication from the cook!   
    '''
    amount_of_time_for_recipie_prompt = f'''
How long would it take to create the recipe of {recipe}
    '''
    
    recipie_prompt = f'''
Give me a recipe for {recipe}, that will feed {portions} people, include the price of each ingredient
    '''
    recipe_pic = respond_picture(f"Realistic picture of this recipie {recipe} on a white table, with a white plate with the food on it")
    
    assistant_answer_recipie = respond_bot(recipie_prompt)
    assistant_answer_difficulty = respond_bot(diffouclty_of_recipie_prompt)
    assistant_answer_time = respond_bot(amount_of_time_for_recipie_prompt)
    return assistant_answer_recipie, assistant_answer_difficulty, assistant_answer_time, recipe_pic



def exercise_prompt(exercise, weights):
    
    prompt = f''''
Write a step by step exercise guide for {exercise}, with {weights}  
    '''
    exercise_pic = respond_picture(f"Realistic picture of this exercise {exercise}")
    
    assistant_answer_exercise = respond_bot(prompt)
    return assistant_answer_exercise, exercise_pic



def add_values_to_file(file_path, values):
    # Used to add user input to a text, file currently not in use
    with open(file_path, 'r') as file:
        content = file.read()

    # Prepend the new values to the content
    content = content + values

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(content)
        
def add_user_info_to_file():
    file_path = file_path_context
    user_age = calculate_age(user_birth_date)
    user_bmi = calculate_bmi(float(user_weight), float(user_height))
    # Replace the placeholders in the content with user information
    content = f'''You are an absolute all knowing personal health/personal/chef assistant  dedicated to helping individuals achieve their fitness goals and improve their overall well-being.
You provide personalized guidance, tips, and recommendations based on their specific needs, only answer health, fitness and personal questions. Do not answer questions if they are not realted
to the users health.
As the personal trainer you offer:
Exercise knowledge and development
Frienship
Support
Motivation 
Reassuernce 


To answer questions use the information below.


User Information below when making plans and talking back to the user:
    
- Sex: {(user_sex)}
- Age: {user_age}
- Birth date: {user_birth_date}
- Name: {user_name}
- Weight: {(user_weight)}
- Height: {(user_height)}
- BMI: {(user_bmi)}

User Goals and Concerns:
- Overall Health Status: [insert overall health status here]
- Primary Goal: [insert primary goal here]
- Secondary Goals: [insert secondary goals here]

Current Lifestyle and Habits:
    
- Current Exercise Routine: [insert current exercise routine here]
- Dietary Preferences: [insert dietary preferences here]
- Sleep Patterns: [insert sleep patterns here]
- Stress Levels: [insert stress levels here]
- Other Relevant Habits: [insert other relevant habits here]

Additional Information:
    
'''
    # Write the updated content back to the file, overriding the existing content
    with open(file_path, 'w') as file:
        file.write(content)

        
def limit_message_history(message_history):
    # Count the number of user inputs and answers, if it exceeds 4 remove the first user input/answer
    count = sum(1 for message in message_history if message['role'] == 'user' or message['role'] == 'assistant')
    if count >= 9: 
        del message_history[1:3]
        count = 0
    return message_history


        
def run(question):
    """
        Runs the factorybot session and returns the total response
    """
    session = OpenAI_Session(context, message_history)
    bot = FactoryBot(session)
    total_response = ""
    for response in bot.session_start(question):
        print(response)
        total_response += response
    return total_response



def input_question(question):
    return  run(question)



def respond_chatbot (message, chat_history, emoji, name):
        
    bot_message = input_question(message)
    chat_history.append(( f"{str(emoji)}: "+ message, " 🏋️‍♂️: " + bot_message))
    time.sleep(2)
    return "", chat_history

def respond_bot(message):
        
    bot_message = input_question(message)
    time.sleep(2)
    return bot_message


def respond_picture(question):
    response = openai.Image.create(
    prompt=question,
    n=1,
    size="256x256"
    )
    image_url = response['data'][0]['url']
    return image_url

# Functions for checking user values
def update_visibility():
    return 

def refresh(textbox_name, textbox_placeholder):
    return gr.Textbox(label=textbox_name, placeholder=textbox_placeholder)

def check_sex(dropdown):    
    if dropdown == "":
        user = "Guest"
    elif dropdown == "CEO":
        user = "CEO"
        msg = gr.Textbox(label="CEO")
        # pre_update_chatbot.update(visible=False)
    elif dropdown == "HR":
        user = "HR"
    elif dropdown == "Guest":
        print("Guest")
    return user

def check_name(name_textbox):
    name_pattern = r"^[A-Za-z]+(?:\s[A-Za-z]+)*$"
    if re.match(name_pattern, name_textbox) is None:
        raise gr.Error("Type your name in the correct format: John Doe, John Adam Doe, or John")
    
def check_birth_date(birth_date_textbox):
    age_pattern = r"^(0[1-9]|1[0-9]|2[0-9]|3[01])\.(0[1-9]|1[012])\.\d{4}$"
    if re.match(age_pattern, birth_date_textbox) is None:
        raise gr.Error("Type your birth date in the correct format: dd.mm.yyyy")
    
def check_weight(weight_textbox):
    weight = float(weight_textbox)
    if weight <= 30 or weight >= 200:
        raise gr.exceptions.Error("Invalid weight, please type a number between 30 Kg and 200 Kg")

def check_height(height_textbox):
    height = float(height_textbox)
    if height <= 140 or height >= 200:
        raise gr.exceptions.Error("Invalid height, please type a number between 140 cm and 200 cm")

def process_sex(sex_dropdown):
    global user_sex
    user_sex = sex_dropdown
    
def process_name(name_textbox):
    global user_name
    user_name = name_textbox
    
def process_birth_date(birth_date_textbox):
    global user_birth_date
    user_birth_date = birth_date_textbox
    
def process_height(height_textbox):
    global user_height
    user_height = height_textbox

def process_weight(weight_textbox):
    global user_weight
    user_weight = weight_textbox

    
def check_all(name_textbox, birth_date_textbox, height_textbox,weight_textbox):   
    try:
        check_name(name_textbox)
        check_birth_date(birth_date_textbox)
        check_height(height_textbox)
        check_weight(weight_textbox)
        
    except gr.exceptions.Error:
        return gr.Column.update(visible=False), gr.Column.update(visible=True) 
    return gr.Column.update(visible=True), gr.Column.update(visible=False) 


    

message_history =[{"role": "system", "content": context},
            ]


class OpenAI_Session():
        
    
    """
     Class for represents an OpenAI session and provides a simple syntax for requesting a response from the AI chatbot.
    """
    def __init__(self, context_description, message_history):
        self.message_history = message_history
        
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
        
        # add_values_to_file(file_path_context_history, context_history_description )
        limit_message_history(message_history)
        print(message_history)
        
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
        
 
def transcribe(audio):
    trans = openai.Audio.transcribe("whisper-1",audio)
    return trans
    

with gr.Blocks(theme=gr.themes.Soft(),title="Health Assistant", css=".footer {display:none !important}") as demo:
    
    column1 = gr.Column(scale=2, min_width=600, variant='compact', visible=True)
    column2 = gr.Column(scale=2, min_width=900, variant='compact', visible=False)
    
    with column1:
        
        sex = gr.Dropdown(["Male", "Female", "Undefined"], label="Gender", value= "Male")
        birth_date = gr.Textbox(label="Birth Date", placeholder="dd.mm.yyyy", value="27.07.1998")
        name = gr.Textbox(label="Name", placeholder="John Doe", value="Zakaria")
        weight = gr.Textbox(label="Weight", placeholder="Kg", value="80" )
        height = gr.Textbox(label="Height", placeholder="cm", value="177")
        
        user_emoji = gr.Dropdown(["😃", "😄", "😊", "😎", "😍", "🙂", "🤩", "😇", "😊", "😉", "🤗", "😌", "😀", "😁", "😆", "😋", "😏"], 
                                    label="Pick an Emoji to represent you in the chat", value = "😃")        
        
        b = gr.Textbox(value="No Errors", label= "Error Box")
        
        btn_1 = gr.Button(label="Submit", variant="primary") 
        
        btn_1.click(check_name ,inputs=name ,outputs= b)
        btn_1.click(check_birth_date ,inputs=birth_date ,outputs= b)
        btn_1.click(check_weight ,inputs=weight,outputs= b)
        btn_1.click(check_height ,inputs=height,outputs= b)
        btn_1.click(check_all, inputs=[name,birth_date,height,weight], outputs=[column2,column1])

        btn_1.click(fn= process_name, inputs=name)
        btn_1.click(fn= process_birth_date, inputs=birth_date)
        btn_1.click(fn= process_height, inputs= height)
        btn_1.click(fn= process_weight, inputs= weight)
        btn_1.click(fn= process_sex, inputs=sex )
        btn_1.click(fn= add_user_info_to_file)
        
        
    with column2:
        with gr.Blocks():
            with gr.Tab("Chatbot"):
                chatbot = gr.Chatbot(show_label=True).style(height=750)
                msg = gr.Textbox()
                msg.submit(respond_chatbot, [msg, chatbot, user_emoji, name], [msg,chatbot])
                
            with gr.Tab("Meal planner"):
                diet_preference = gr.CheckboxGroup(["Vegan", "Pescitarian", "Keto", "Vegetarian", "Flexitarian", "Mediterranean", "Paleolithic (Paleo)", "Whole30", "Gluten-free", "Dairy-free", "Low-carb", "Low-fat", "DASH"],
                                                    label="Food preference", info="What do you prefer?")
                snack_amount = gr.CheckboxGroup(["None", "1-2 snacks", "2-3 snacks", "3+ snacks"], label="Snack amount", info="How many snacks do you prefer?")

                meal_amount = gr.CheckboxGroup(["1 meal", "2 meals", "3 meals", "4+ meals"], label="Meal amount", info="How many meals do you prefer?")

                other_factors_meal = gr.Textbox(label="Any other important factors to consider, for your meal plan?")
                
                meal_planner_output = gr.TextArea()
                btn_2 = gr.Button(label="Submit", variant="primary") 
                btn_2.click(fn = meal_planner_prompt, inputs=[diet_preference, snack_amount,meal_amount,other_factors_meal], outputs= meal_planner_output)
                
                            
            with gr.Tab("Workout routine planner"):
                
                workout_days = gr.CheckboxGroup(["1 day", "2 days", "3 days", "4 days", "5 days", "6 days", "7 days"],
                                        label="Workout days", info="How many days per week do you plan to work out?")

                workout_intensity = gr.CheckboxGroup(["Low intensity", "Moderate intensity", "High intensity"],
                                        label="Workout intensity", info="What intensity level do you prefer for your workouts?")
                workout_duration = gr.CheckboxGroup(["30 minutes", "45 minutes", "60 minutes", "More than 60 minutes"],
                                    label="Workout duration", info="How long do you prefer your workout sessions?")


                cardio_options = gr.CheckboxGroup(["None","Running", "Cycling", "Swimming", "Hiking", "Rowing"],
                                        label="Cardio options", info="Select the cardio activities you enjoy:")

                strength_training = gr.CheckboxGroup(["Bodyweight exercises", "Weightlifting", "Resistance bands", "Yoga", "Pilates"],
                                            label="Strength training", info="Choose the type of strength training you prefer:")
                
                other_factors_workout = gr.Textbox(label="Any other important factors to consider, for your workout plan")

                workout_plan_output = gr.TextArea()
                btn_3 = gr.Button(label="Submit", variant="primary")
                btn_3.click(fn=workout_planner_prompt, inputs=[workout_days, workout_intensity, cardio_options, strength_training, workout_duration,other_factors_workout ],
                            outputs=workout_plan_output)

            with gr.Tab("Recipe"):
                
                recipe = gr.Textbox(label="What meal do you want to cook")
                portion_amount = gr.Dropdown(["1","2","3", "4","5","6"],label="Portions")
                
                
                btn_4 = gr.Button(label="Submit", variant="primary")
                
                difficulty_out = gr.Textbox(label="Difficulty:")
                time_out = gr.Textbox(label="Time to create:")
                recipe_out = gr.TextArea(label="The recipe:", scroll_to_output = True)
                

                recipe_picture = gr.Image(shape=[256,256])
                btn_4.click(fn=recipie_prompt, inputs=[recipe, portion_amount], outputs=[recipe_out, difficulty_out, time_out, recipe_picture])
                
                
            with gr.Tab("Exercise"):
                
                exercise = gr.Textbox(label="What exercise do you want to know more about")
                weight_amount = gr.Dropdown(["Wights", "No wights"],label="Are you using weights")
                
                btn_4 = gr.Button(label="Submit", variant="primary")
                
                exercise_tips = gr.TextArea(label="The recipe:", scroll_to_output = True)
                

                exercise_picture = gr.Image(shape=[256,256])
                btn_4.click(fn=exercise_prompt, inputs=[exercise, weight_amount], outputs=[exercise_tips, exercise_picture])
                

                
            with gr.Tab("Voice assistant"):
                
                mic = gr.Audio(source="microphone")
                btn_5 = gr.Button(label=("Submit"), variant="primary")
                
                
                out_text = gr.TextArea(label="Return Text:",)
                
                btn_5.click(fn=transcribe, inputs= mic, outputs= out_text)
                
                

if __name__ == "__main__":  
    demo.launch()