from flask import Flask, request, render_template
import library
import stories as s
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)  # creating an instance of the Flask Class

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

# creating global variables
story = {}
needed = []
story_obj = None

# 1 - Home Page
@app.route('/')
def home():
		"""Load the root home page,
		which has a drop-down form
		to select a story to use for
		the MadLib.
		"""
		return render_template('home.html')

# 2 - Enter Words Page
@app.route('/enter')
def enter():
	"""Load the form to enter the words
	to use in the MadLib.
	Also pulls the requested story and 
	needed words from the library file.
	Calls the Display page and passes
	in the story and needed words.
	"""
	# Use the global variables
	global story
	global needed
	global story_obj

	# Get which story was selected by the user
	# and set the 'story' and 'needed' variables.
	selection = request.args['selection']
	if selection == 'Story1':
			story = library.story1['story']
			needed = library.story1['needed']
	elif selection == 'Story2':
			story = library.story2['story']
			needed = library.story2['needed']
	elif selection == 'Story2':
			story = library.story3['story']
			needed = library.story3['needed']
	else:
			story = library.story4['story']
			needed = library.story4['needed']

	# Create an instance from the Story class
	story_obj = s.Story(needed, story)

	return render_template('enter_words.html', needed=needed)

# 3 - Display Words & Story Page
@app.route('/display_story')
def display():
	"""Capture the words the user entered and 
	put them into a dict that can be used as an 
	argument and passed into the generate method.
	Call the view page to present the story.
	"""

	# Use the global variables
	global needed
	global story_obj
	
	# Array to store the user entered words
	words_to_use = []
	user_words_dict = {}

	# Put the user entered words into a list
	for word in needed:
		prompt = request.args[word] # get the corresponding form entry
		words_to_use.append(prompt)
	
	for x in range(0, len(needed)):
		user_words_dict[needed[x]] = words_to_use[x]
	# Sample output: 
 	# user_words_dict = {'place': 'san diego', 'noun': 'kettle', 'verb': 'snooze'}

	# Call the generate method on the class instance using the user entered words.
	compiled_story = story_obj.generate(user_words_dict)

	return render_template('display_story.html', compiled_story=compiled_story)
