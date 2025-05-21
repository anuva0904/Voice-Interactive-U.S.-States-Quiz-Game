import turtle
import pandas as pd
import tkinter as tk
from voice import VoiceAssistant
from dialogbox import VoiceInputDialog

# Setup GUI and Turtle screen
root = tk.Tk()
root.withdraw()

screen = turtle.Screen()
screen.title("U.S. States Game Start")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

# Load data
data = pd.read_csv("50_states.csv")
all_states = data.state.to_list()
all_states = list(map(lambda state: state.strip(), all_states))
guessed_states = []

# Setup voice assistant
va = VoiceAssistant()
va.speak("Hello, today I will assist you in your U.S. States quiz game.")

# Game loop
while len(guessed_states) < 50:
    va.speak(f"Enter the states out of{len(all_states)} states. ")
    title_text = f"{len(guessed_states)}/50 States Correct"
    dialog = VoiceInputDialog(root, title_text, va)  
    answer_state = dialog.result
    if  answer_state:
      answer_state = answer_state.strip().title()
      if answer_state in all_states:
           va.speak("Congratulations, you got it!")
      elif answer_state == "Exit":
           va.speak("Goodbye, see you next time!")
           missing_states = [state for state in all_states if state not in guessed_states]
           pd.DataFrame(missing_states).to_csv("missing_states.csv")
           va.speak("Exiting the game. I've saved the states you missed.")
           break

      else:
           va.speak("uh oh you have entered the wrong states!" )
      if answer_state in all_states and answer_state not in guessed_states:
         guessed_states.append(answer_state)
         t = turtle.Turtle()
         t.hideturtle()
         t.penup()
         state_data = data[data.state == answer_state]
         t.goto(int(state_data.x.item()), int(state_data.y.item()))
         t.write(answer_state)
      elif answer_state not in guessed_states:
          guessed_states = guessed_states
va.speak(f"Game over. You guessed {len(guessed_states)} states.")
screen.mainloop()