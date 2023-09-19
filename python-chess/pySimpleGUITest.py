import PySimpleGUI as gui                        
# Define the window's contents
layout = [  [gui.Text("Chess")],
            [gui.Column([[0],[1],[2]])]
          
         ]     
# Create the window
window = gui.Window('Window Title', layout)      
                                                
# Display and interact with the Window
event, values = window.read()                   # Event loop or Window.read call

# Do something with the information gathered
print('Hello', values[0], "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()                                  