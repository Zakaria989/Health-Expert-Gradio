def limit_message_history(message_history):
    # Count the number of user inputs and answers
    count = sum(1 for message in message_history if message['role'] == 'user' or message['role'] == 'assistant')
    print("\n" + str(count) + " \n")
    # Check if there are four or more user inputs and answers
    if count >= 4:
        # Find the index of the second user input and assistant answer
        index = 0
        found = False
        for i, message in enumerate(message_history):
            if message['role'] == 'user' or message['role'] == 'assistant':
                if found:
                    index = i
                    break
                else:
                    found = True
        
        # Remove the first user input and assistant answer
        del message_history[index]
    
    return message_history



mess = [{'role': 'user', 'content': ' '}, {'role': 'system', 'content': 'You are an absolute all knowing personal health/personal/chef assistant  dedicated to helping individuals achieve their fitness goals and improve their overall well-being.\nYou provide personalized guidance, tips, and recommendations based on their specific needs, only answer health, fitness and personal questions.\nTo answer questions use the information below.\n\n\nUser Information:\n\n- Sex:\n- Age: 24\n- Birth date: 27.07.1998\n- Name: Zakaria Ahmed\n- Weight: 80\n- Height: 177\n- BMI: 25.535446391522235\n\nUser Goals and Concerns:\n- Overall Health Status: [insert overall health status here]\n- Primary Goal: [insert primary goal here]\n- Secondary Goals: [insert secondary goals here]\n\nCurrent Lifestyle and Habits:\n\n- Current Exercise Routine: [insert current exercise routine here]\n- Dietary Preferences: [insert dietary preferences here]\n- Sleep Patterns: [insert sleep patterns here]\n- Stress Levels: [insert stress levels here]\n- Other Relevant Habits: [insert other relevant habits here]\n\nAdditional Information:\n'}, {'role': 'user', 'content': 'remember the number 2 for me'}, {'role': 'assistant', 'content': "Sure, I'll remember the number 2 for you! Is there anything specific you want me to do with this number?"}, {'role': 'user', 'content': 'how many weeks will it take me to lose 5 kgs?'}, {'role': 'assistant', 'content': "The amount of time it takes to lose 5 kilograms (11 pounds) can vary depending on various factors such as starting weight, body composition, exercise routine, and diet. A safe and healthy rate of weight loss is typically 0.5 to 1 kilogram (1 to 2 pounds) per week. At this rate, it is reasonable to expect to lose 5 kilograms in 5 to 10 weeks. However, keep in mind that individual results may vary and it's important to maintain a sustainable approach to weight loss through a combination of healthy eating habits and regular exercise."}, {'role': 'user', 'content': 'what is the best gym in norway?'}, {'role': 'assistant', 'content': "There are several great gyms in Norway, and the best one for you may depend on your location and personal preferences. Here are a few popular gyms in Norway:\n\n1. SATS - This is one of the largest gym chains in Norway with facilities throughout the country. They offer a variety of classes and equipment, as well as personal training services.\n\n2. EVO Fitness - This is a more budget-friendly gym chain that focuses on providing a no-frills workout experience. They have facilities throughout Norway and offer 24/7 access to equipment.\n\n3. Fresh Fitness - This is another popular gym chain in Norway that offers a variety of classes and equipment. They have facilities throughout the country, including some that are open 24/7.\n\n4. Athletica - This is a gym chain with facilities located at several universities across Norway. They offer a variety of classes and sports facilities, as well as personal training services.\n\nUltimately, the best gym for you will depend on your fitness goals, location, and personal preferences. It's a good idea to shop around and try out several gyms before committing to a membership."}, {'role': 'user', 'content': 'nice where can i find a personal trainer?'}, {'role': 'assistant', 'content': "There are several ways to find a personal trainer:\n\n1. Ask at your local gym - Most gyms and health clubs offer personal training services, so you may be able to find a personal trainer by asking at your gym.\n\n2. Online platforms - There are many online platforms like Thumbtack, MyFitnessPal, IDEA FitnessConnect, etc. that can connect you with personal trainers in your area. You can browse profiles of trainers, read reviews, and compare prices to find the one that's right for you.\n\n3. Referrals - If you know anyone who has worked with a personal trainer before, you can ask for a referral. They may be able to recommend a trainer who they've had a positive experience with.\n\n4. Certification organizations - Certification organizations like the National Strength and Conditioning Association, the American Council on Exercise, or the International Sports Sciences Association maintain lists of certified personal trainers which you can search in your area.\n\nWhichever way you choose to find a personal trainer, it's important to do your research and ensure that the trainer has appropriate certifications and credentials, as well as experience and expertise in the areas that align with your goals and needs."}, {'role': 'user', 'content': 'niec'}, {'role': 'assistant', 'content': 'Glad to be of help. Is there anything else I can help you with?'}]


x = limit_message_history(mess)

print(x)