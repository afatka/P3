"""
This class is the most granular section of the P3 Grade Tool. 

It takes a subcategory from the xml and generates all GUI components for grading. 

It includes all class attributes required to retrieve and load grading attributes [comments, values, etc]
"""

import maya.cmds as cmds
# import maya.utils
import xml.etree.ElementTree as et
import re, sys
class  SubcategoryGradeSection(object):

	def __init__(self, subcategoryFromXML, defaultsFromXML, runAuto, configDict):
		"""
		take the element tree element 'subcategory' from the xml to generate the subcategory section'
		"""
		# self.updateFunction  = updateFunction
		self.runAuto = runAuto
		self.configDict = configDict

		# colors
		self.colors = {"default color" : (0.26666666666666666, 0.26666666666666666, 0.26666666666666666),
				  	   "red" : (0.36666666666666666, 0.26666666666666666, 0.26666666666666666),
				  	   "green" : (0.26666666666666666, 0.36666666666666666, 0.26666666666666666),
				  	   "dim" : (0.26666666666666666, 0.26666666666666666, 0.26666666666666666)}

		self.default_comment_is_visible = False

		scrollField_height = 125
		row_spacing = 0

		# self.current_grade_value = 0
		self.current_comment_text = ''
		# self.current_default_comment_text = ''
		# self.current_example_comment_text = ''
		# self.auto_flagged_list = []
		# self.is_complete = False

		self.subcatXML = subcategoryFromXML
		# self.log('trying to unpack gradeValue from defaults')
		# self.log('defaultsFromXML are: %s' % defaultsFromXML)
		# self.grade_values = defaultsFromXML.find('gradeValue')
		# self.log('grade_values: %s' % self.grade_values)

		self.title = self.subcatXML.get('title')
		if self.title == None:
			self.title = self.subcatXML.find('title').text

		# self.weight = self.subcatXML.get('weight')
		# if self.weight == None:
		# 	self.weight = self.subcatXML.find('weight').text

		# try: 
		# 	self.auto = self.subcatXML.find('auto').text
		# except AttributeError: 
		# 	self.auto = ''

		# self.autocomplete = self.subcatXML.get('autocomplete')
		# if self.autocomplete:
		# 	try:
		# 		self.autocomplete = float(self.autocomplete)
		# 	except ValueError as e:
		# 		cmds.error("\n\nSubcategory: {}\nautocomplete value: {}\nThe value of autocomplete must be a legal number.".format(self.title, self.autocomplete))

		self.rmb = [] # [0] title, [1] text, [2] divider
		if self.subcatXML.findall('RMB'):
			for item in self.subcatXML.findall('RMB'):
				self.rmb.append([item.get('title'), item.text, item.get('divider')])

		self.log('\nRiGHT HERE!')
		if self.rmb != []:
			for item in self.rmb:
				self.log('\nTitle: {}\n{}'.format(item[0], item[1]))
		self.log('RMB: {}'.format(self.rmb))
		
		self.log('starting subcategory GUI')
		# self.subcat_main_column_layout = cmds.formLayout(numberOfDivisions = 100, backgroundColor = self.configDict["colors"]['incomplete color'])
		# self.subcat_main_column_layout = cmds.formLayout(numberOfDivisions = 100, 
		# 												 backgroundColor = self.configDict["colors"]['incomplete color'],
		# 												 visible = False) # P3 update - visible = false


		seperatorReference = cmds.separator(style = 'in')

		# self.titleText = cmds.text(label = self.title, align = 'left')
		# if self.auto != '':
		# 	cmds.popupMenu(parent = self.titleText, button = 3)
		# 	cmds.menuItem(label = 'Run Auto', command = lambda *args: self.runAuto(self.subcatXML, self, auto = True))
		# 	cmds.menuItem(label = 'Select Flagged', command = lambda *args: self.select_flagged())
		# self.int_field_slider_row_layout = cmds.rowLayout(numberOfColumns = 2)#int_field_slider_row_layout
		# self.int_field_slider_row_layout = cmds.formLayout(numberOfDivisions = 100)

		# self.grade_intField = cmds.intField( minValue=0, maxValue=150, step=1, width = 36, changeCommand = lambda *args: self.update_subcategory('intField', *args))
		# self.grade_slider = cmds.intSlider( min=-100, max=0, value=0, step=1, changeCommand = lambda *args: self.update_subcategory('slider', *args), dragCommand = lambda *args: self.update_subcategory('slider', *args)) 

		# cmds.setParent(self.int_field_slider_row_layout)
		# cmds.formLayout(self.int_field_slider_row_layout, edit = True,
		# 	attachForm = [(self.grade_intField, 'left', 0),(self.grade_slider, 'right', 0)],
		# 	attachControl = [(self.grade_slider, 'left', 5, self.grade_intField)]
		# 	)

		# cmds.setParent(self.subcat_main_column_layout)

		# cmds.formLayout(self.subcat_main_column_layout, edit = True,
		# 	attachForm = [(seperatorReference, 'left', 0),(seperatorReference, 'top', 0),(seperatorReference, 'right', 0),
		# 				(self.titleText, 'left', 0),
		# 				(self.int_field_slider_row_layout, 'left', 0),(self.int_field_slider_row_layout, 'right', 10)],
		# 	attachControl = [(self.titleText, 'top', 0, seperatorReference), (self.int_field_slider_row_layout, 'top', 2, self.titleText)]
		# 	)


		# self.radio_creator(self.subcatXML.find('gradeComment'))

		# cmds.formLayout(self.subcat_main_column_layout, edit = True,
		# 	attachForm = [(self.radio_row_layout, 'left', 0),(self.radio_row_layout, 'right', 0)],
		# 	attachControl = [(self.radio_row_layout, 'top', 0, self.int_field_slider_row_layout)]
		# 	)

		# self.log('radios created, starting comment frames')
		# self.subcat_comments_frame_layout = cmds.frameLayout( label='Comments', collapsable = True, collapse = False, backgroundColor = self.configDict["colors"]['dim'], expandCommand = self.maintain_default_comment_visibility) 
		self.subcat_comments_frame_layout = cmds.frameLayout( label=self.title, collapsable = True, collapse = False, backgroundColor = self.configDict["colors"]['dim'])#, expandCommand = self.maintain_default_comment_visibility) 


		# self.default_comments_frameLayout = cmds.frameLayout( label='Default Comments', collapsable = True, collapse = True, backgroundColor = self.colors['dim']) 
		# self.default_comments = cmds.scrollField( height = scrollField_height, wordWrap = True, visible = self.default_comment_is_visible, changeCommand = lambda *args: self.update_subcategory('default_comments_text', *args)) 
		# cmds.setParent('..')

		self.comments_text_field = cmds.scrollField( height = scrollField_height, wordWrap = True,  changeCommand = lambda *args: self.update_subcategory('comments_text', *args))

		self.rmb_menu = cmds.popupMenu(parent = self.comments_text_field, button = 3)
			# i = 0
		if self.rmb != []:
			for item in self.rmb:

				divider = item[2]
				if divider != None and divider.lower() == "true":
					divider = True
				if divider == None:
					divider = False	

				self.log('{}:{}'.format(item[0], item[1]))
				cmds.menuItem(parent = self.rmb_menu, label = item[0], command = lambda args, i = item[1]:self.add_comment_to_comments(i), divider = divider)
				# i += 1

		cmds.menuItem(divider = True)
		# cmds.menuItem(label = 'Append session comment', command = lambda *args: self.append_session_commment())
		cmds.menuItem(label = 'Select Multiple Comments', command = lambda *args: self.selectMultipleComments())
		cmds.menuItem(divider = True)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = 'Clear Comments', command = self.clear_comments)
		self.toggleDefaultCommentVisButton = cmds.button(label = "Toggle Default Comment Visibility", command = self.toggle_default_comments, backgroundColor = self.configDict["colors"]['dim'], visible = False) # P3 Update visible = false
		cmds.setParent('..')

		cmds.setParent('..')

		# if self.autocomplete:
		# 	self.autocomplete_update()

	def toggle_default_comments(self, *args):
		 if self.default_comment_is_visible: 
		 	cmds.scrollField( self.default_comments, edit = True, visible = False)
		 	self.default_comment_is_visible = False
		 else:
		 	cmds.scrollField( self.default_comments, edit = True, visible = True)
		 	self.default_comment_is_visible = True

	# def maintain_default_comment_visibility(self, *args):
	# 	if self.default_comment_is_visible: 
	# 	 	cmds.scrollField( self.default_comments, edit = True, visible = True)
	# 	else:
	# 	 	cmds.scrollField( self.default_comments, edit = True, visible = False)
	# 	 	cmds.button(self.toggleDefaultCommentVisButton, edit = True, visible = False) # P3 Update

	def clear_comments(self, *args):
		cmds.scrollField(self.comments_text_field, edit = True, text = '')
		self.update_subcategory('comments_text')

	def select_flagged(self):
		self.log('select flagged!')
		if len(self.auto_flagged_list) == 0:
			cmds.warning('No objects in flagged list')
		else:
			self.log('selecting objects')
			cmds.select(self.auto_flagged_list)
			self.log('objects selected')

	def validate_tag_name(self, tag):
		updatedTag = re.sub('plus', '+', tag)
		if updatedTag.startswith('_'):
			updatedTag = updatedTag[1:]

		return updatedTag

	def radio_creator(self, gradeComments):
		"""
		take the gradeComments element from the xml and create radio buttons labeled correctly
		"""
		labels = []
		longestLabel = 0

		if gradeComments == None or len(gradeComments) == 0:
			raise Exception('No grade comments provided for subcategory: {}'.format(self.title))
		for label in gradeComments:
			
			tagLength = len(self.validate_tag_name(label.tag))
			if tagLength > longestLabel:
				longestLabel = tagLength
			labels.append(label)

		adjustedCellWidth = (25 + (longestLabel * 5))
	

		self.radio_row_layout = cmds.gridLayout(cellHeight = 18, height = 30, cellWidth = adjustedCellWidth, numberOfColumns = len(labels) ,columnsResizable = False)

		self.grade_radio_collection = cmds.radioCollection()
		for label in labels:
			self.log('processing label: {}'.format(label.tag))
			tag = self.validate_tag_name(label.tag)
			self.log('processed label: {}\n'.format(tag))

			cmds.radioButton(label = tag, changeCommand = lambda *args: self.update_subcategory('radioButton', *args))

		##
		self.resetRadioButton = cmds.radioButton(label = '.', visible = False)
		##
		cmds.setParent('..')
		cmds.setParent('..')

	def gutCheck_update(self, intValue, *args):
		cmds.intField(self.grade_intField, edit = True, value = intValue)
		self.update_subcategory('intField')
		cmds.frameLayout(self.subcat_comments_frame_layout, edit = True, collapse = True)

	def autocomplete_update(self, *args):
		cmds.intField(self.grade_intField, edit = True, value = self.autocomplete)
		self.update_subcategory('intField')

	def update_subcategory(self, control_type, *args):
		"""
		trigger on element change command to update all the other fields in subcategory
		"""

		# if control_type == 'intField':
		# 	self.log('query intField and update others')
		# 	intField_value = cmds.intField(self.grade_intField, query = True, value = True)
		# 	self.log('intField is %s' % intField_value)

		# 	self.current_grade_value = intField_value
		# 	self.log('current grade is: %s' % self.current_grade_value)
		# 	cmds.intSlider(self.grade_slider, edit=True, value = -intField_value)
		# 	self.update_radios_default_comments(intField_value)
		# 	self.update_default_comments()
		# 	self.update_is_complete()
		# 	self.updateFunction()

		# elif control_type == 'slider':

		# 	self.log('query slider and update others')
		# 	slider_value = abs(cmds.intSlider(self.grade_slider, query = True, value = True))
		# 	self.log('intSlider is %s' % slider_value)

		# 	self.current_grade_value = slider_value
		# 	self.log('current grade is: %s' % self.current_grade_value)
		# 	cmds.intField(self.grade_intField, edit = True, value = slider_value)
		# 	self.update_radios_default_comments(slider_value)
		# 	self.update_default_comments()
		# 	self.update_is_complete()
		# 	self.updateFunction()

		# elif control_type == 'radioButton':
		# 	self.log('query radio collection and update others')
		# 	selected = cmds.radioCollection(self.grade_radio_collection, query = True, select = True)
		# 	selected_letter = cmds.radioButton(selected, query = True, label = True)
		# 	selected_letter = re.sub('\\+', 'plus', selected_letter)
		# 	self.log('selected radioButton: %s' % selected_letter)

		# 	try:
		# 		self.current_grade_value = int(self.grade_values.find(selected_letter).text)
		# 	except AttributeError as e:
		# 		self.current_grade_value = int(self.grade_values.find("_{}".format(selected_letter)).text)


		# 	# self.current_grade_value = int(self.grade_values.find(selected_letter).text)
		# 	self.log('current grade is: %s' % self.current_grade_value)
		# 	cmds.intField(self.grade_intField, edit = True, value = self.current_grade_value)
		# 	cmds.intSlider(self.grade_slider, edit = True, value = -self.current_grade_value)
		# 	self.log('selected_letter: %s' % selected_letter)
			
		# 	try:
		# 		cmds.scrollField(self.default_comments, edit = True, text = self.subcatXML.find('gradeComment').find(selected_letter).text)
		# 	except AttributeError as e:
		# 		cmds.scrollField(self.default_comments, edit = True, text = self.subcatXML.find('gradeComment').find("_{}".format(selected_letter)).text)

		# 	# cmds.scrollField(self.default_comments, edit = True, text = self.subcatXML.find('gradeComment').find(selected_letter).text)
		# 	self.current_default_comment_text = cmds.scrollField(self.default_comments, query = True, text = True)
		# 	self.log('Default Comments Updated')
		# 	self.log(self.current_default_comment_text)
		# 	self.update_is_complete()
		# 	self.updateFunction()

		# elif control_type == 'default_comments_text':
		# 	self.current_default_comment_text = cmds.scrollField(self.default_comments, query = True, text = True)
		# 	self.log('Default Comments Updated')
		# 	self.log(self.current_default_comment_text)
		# 	self.update_is_complete()

		# elif control_type == 'example_comments_text':
		# 	self.current_example_comment_text = cmds.scrollField(self.example_comments, query = True, text = True)
		# 	self.log('examples updated')
		# 	self.log(self.current_example_comment_text)

		# else:
		self.current_comment_text = cmds.scrollField(self.comments_text_field, query = True, text = True)
		self.log('comments updated')
		self.log(self.current_comment_text)
	
	def update_radios_default_comments(self, value):
		"""
		take value and set radio buttons associated with that buttons
		"""
		self.log('set dim radios')

		grade_value_letter = ""
		do_break = False
		for g_value in self.grade_values:
			for g_comment in self.subcatXML.find('gradeComment'):
				if g_value.tag == g_comment.tag:
					grade_value_letter = g_value.tag
					if int(g_value.text) <= value:
						do_break = True
						break
			if do_break:
				break

		grade_value_letter = re.sub('plus', '+', grade_value_letter)
		radioButtons = cmds.radioCollection(self.grade_radio_collection, query = True, collectionItemArray = True)
		# print('grade_value_letter: {}'.format(grade_value_letter))
		for butn in radioButtons:
			# print('radio button to test: {}'.format(cmds.radioButton(butn, query=True, label = True)))
			if cmds.radioButton(butn, query=True, label = True) == grade_value_letter or cmds.radioButton(butn, query=True, label = True) == grade_value_letter[1:]:
				# print('they match... should have selected it...?')
				cmds.radioButton(butn, edit = True, select = True)

	def update_default_comments(self):
		"""
		query grade values and update default comments accordingly

		SETS BASED ON RADIO BUTTONS. RADIO BUTTONS MUST BE UPDATED FIRST 
		"""
		self.log('update dim default comments')
		selected_letter = ''
		radioButtons = cmds.radioCollection(self.grade_radio_collection, query = True, collectionItemArray = True)
		for butn in radioButtons:
			if cmds.radioButton(butn, query=True, select = True):
				selected_letter = cmds.radioButton(butn, query = True, label = True)
				# print("Selected lettter: {}".format(selected_letter))
				break
		if selected_letter == '':
			cmds.error('selected_letter not set.\n{}\nGrade Value: {}\n\n'.format(self.title, self.current_grade_value))

		# print('selected letter: {}'.format(selected_letter))
		if '+' in selected_letter:
			# print('plus detected!')
			# selected_letter = re.sub('+', 'plus', selected_letter)
			selected_letter = selected_letter.replace('+', 'plus')
			# print('new selected_letter: {}'.format(selected_letter))
		try:
			cmds.scrollField(self.default_comments, edit = True, text = self.subcatXML.find('gradeComment').find(selected_letter).text)
		except AttributeError as e:
			cmds.scrollField(self.default_comments, edit = True, text = self.subcatXML.find('gradeComment').find("_{}".format(selected_letter)).text)
		

		self.current_default_comment_text = cmds.scrollField(self.default_comments, query = True, text = True)
		self.log('Default Comments Updated')
		self.log(self.current_default_comment_text)

	def selectMultipleComments(self, *args):

		def collectComments(self, *args):
			comments = ""
			for element in rccCheckBoxes:
				# print("element: {}".format(element))
				if cmds.checkBox(element[0], query = True, value = True):
					comments += element[1]

			self.add_comment_to_comments(comments)

			cmds.deleteUI('SelectMultipleCommmentsWindow')

		def clearAll(self, *args):
			for element in rccCheckBoxes:
				cmds.checkBox(element[0], edit = True, value = False)


		# window_widthHeight = (280, 600)
		elementWidth = 300
		elementCount = 2

		#if SelectMultipleCommmentsWindow window exists delete it
		if (cmds.window('SelectMultipleCommmentsWindow', exists = True)):
			cmds.deleteUI('SelectMultipleCommmentsWindow')

		comment_window = cmds.window('SelectMultipleCommmentsWindow', title = 'Select Multiple Comments')

		rccFormLayout = cmds.formLayout(parent = comment_window, numberOfDivisions = 100)
		rccScrollLayout = cmds.scrollLayout(parent = rccFormLayout)

		cmds.formLayout(rccFormLayout, edit = True, 
			attachForm=[(rccScrollLayout, 'top', 5), (rccScrollLayout, 'left', 5), 
		    			(rccScrollLayout, 'bottom', 5), (rccScrollLayout, 'right', 5)])

		# self.rmb [0] title, [1] text, [2] divider

		cmds.button(parent = rccScrollLayout, label = "Clear All",  width = elementWidth, command = clearAll, backgroundColor = self.configDict["colors"]['dim'])

		rccCheckBoxes = []

		# rcc[0] = title
		# rcc[1] = comment
		# rcc[2] = divider status
		for rcc in self.rmb:
			elementCount += 1

			isTitle = rcc[2] # if it is a divider, disable
			if isTitle != None and isTitle.lower() == "true":
				isTitle = True
			if isTitle == None:
				isTitle = False	

			# print('RCC: {}: {}'.format(rcc[0], rcc[1]))
			if isTitle:
				cmds.text(parent = rccScrollLayout, label = rcc[0],  font = "boldLabelFont", backgroundColor = tuple(map(lambda i : i - 0.03,  self.configDict["colors"]['dim'])))
			else:
				if rcc[1] != None:
					if rcc[1].strip() != '':
						rccCheckBoxes.append( (cmds.checkBox(parent = rccScrollLayout, label = rcc[0] ), rcc[1]))

		cmds.button(parent = rccScrollLayout, label = "Add to Comments and Close", width = elementWidth, command = lambda args: collectComments(self), backgroundColor = self.configDict["colors"]['dim'])
		# cmds.window('SelectMultipleCommmentsWindow', edit = True, height = (elementCount * 10), width = elementWidth)

		cmds.showWindow(comment_window)

	def append_session_commment(self):
		self.log('append session comment stuff')

		def close_command(*args):
			self.log('close command')
			# maya.utils.executeDeferred("cmds.deleteUI('ASCW')")

		def get_comment(*args):
			self.log('get comment')
			title = cmds.textField(comment_title, query = True, text = True)
			comment = cmds.scrollField(comment_text, query = True, text = True)
			self.log('\nTitle: {}\nComment: {}'.format(title, comment))
			if title != 'Comment Title' and comment != 'Type your comment text here...':
				cmds.menuItem(parent = self.rmb_menu, label = title, command = lambda args, i = comment:self.add_comment_to_comments(i))
				cmds.deleteUI('ASCW')
				reorder_comments()
			else:
				cmds.error('Type in a comment title and comment text to continue.\nClose the window to cancel.')
			self.add_comment_to_comments(comment)

		def reorder_comments(*args):
			self.log('reorder comments')
			comment_items = cmds.popupMenu(self.rmb_menu, query = True, itemArray = True)
			comment_items[-1], comment_items[-2] = comment_items[-2], comment_items[-1]
			comment_labels_commands = []
			for i in comment_items:
				l = cmds.menuItem(i, query = True, label = True)
				c = cmds.menuItem(i, query = True, command = True)
				comment_labels_commands.append((l,c))
			cmds.popupMenu(self.rmb_menu, edit = True, deleteAllItems = True)
			for i in comment_labels_commands:
				cmds.menuItem(label = i[0], command = i[1], parent = self.rmb_menu)



		self.log('make comment window')
		window_widthHeight = (250, 200)
		padding = 2

		#if ASCW window exists delete it
		if (cmds.window('ASCW', exists = True)):
			cmds.deleteUI('ASCW')

		comment_window = cmds.window('ASCW', title = 'Append Session Comment', 
									width = window_widthHeight[0], 
									height = window_widthHeight[1],
									closeCommand = close_command)
		comment_form = cmds.formLayout(numberOfDivisions = 250)
		comment_title = cmds.textField(text = 'Comment Title')
		comment_text = cmds.scrollField(editable = True, wordWrap = True, text = 'Type your comment text here...')
		comment_btn = cmds.button(label = 'Append Comment', command = get_comment)
		cmds.setParent('..')

		cmds.formLayout(comment_form, edit = True, attachForm = [
			(comment_title, 'left', padding),
			(comment_title, 'right', padding),
			(comment_title, 'top', padding),
			(comment_text, 'left', padding),
			(comment_text, 'right', padding),
			(comment_btn, 'left', padding), 
			(comment_btn, 'right', padding), 
			(comment_btn, 'bottom', padding)], 
			attachControl = [
			(comment_text, 'top', padding, comment_title),
			(comment_text, 'bottom', padding, comment_btn)])
		cmds.showWindow(comment_window)
	 
	def add_comment_to_comments(self, comment, *args):
		self.log('add comment to comments')
		# text_bucket = cmds.scrollField(self.comments_text_field, query = True, text = True)
		# # self.log('index: {}'.format(index))
		# self.log('RMB: {}'.format(self.rmb))
		# text_bucket += ' {}'.format(comment)
		# cmds.scrollField(self.comments_text_field, edit = True, text = text_bucket)
		cmds.scrollField(self.comments_text_field, edit = True, insertText = " {}".format(comment), insertionPosition = 0)
		self.update_subcategory('comments_text')

	def update_is_complete(self, reset = False):
		self.log('updating "is_complete"')
		if reset:
			self.is_complete = False
			cmds.formLayout(self.subcat_main_column_layout, edit = True, backgroundColor = self.configDict["colors"]['incomplete color'])
			self.log('is_complete: reset')
		elif self.current_grade_value == 0 and self.current_default_comment_text == '':
			self.is_complete = False
			cmds.formLayout(self.subcat_main_column_layout, edit = True, backgroundColor = self.configDict["colors"]['incomplete color'])
			self.log('not complete')
		else:
			self.is_complete = True
			cmds.formLayout(self.subcat_main_column_layout, edit = True, backgroundColor = self.configDict["colors"]['complete color'])
			self.log('is_complete now TRUE')

	def what_is_the_grade(self):
		"""
		collect grade from subcategory and return
		"""

		# update comments before returning 
		self.update_subcategory("comments_text")

		return_dict = {
			'section_title': self.title, 
			# 'section_weight': self.weight,
			# 'grade_value' : self.current_grade_value,
			'comment_text' : self.current_comment_text,
			# 'default_comments_text' : self.current_default_comment_text,
			# 'example_comments_text' : self.current_example_comment_text,
			# 'is_complete': self.is_complete
		}

		return return_dict

	def this_is_the_grade(self, grade_to_set):
		"""
		take an input dictionary and populate all the grade fields accordingly
		"""

		cmds.intField(self.grade_intField, edit = True, value = grade_to_set['grade_value'])
		self.update_subcategory('intField')
		if grade_to_set['grade_value'] != '':
			cmds.scrollField(self.comments_text_field, edit = True, text = grade_to_set['comment_text'])
			self.update_subcategory('comments_text')
		if grade_to_set['default_comments_text'] != '':	
			cmds.scrollField(self.default_comments, edit = True, text = grade_to_set['default_comments_text'])
			self.update_subcategory('default_comments_text')
		# if grade_to_set['example_comments_text'] != '':
		# 	cmds.scrollField(self.example_comments, edit = True, text = grade_to_set['example_comments_text'])
		# 	self.update_subcategory('example_comments_text')

		# self.auto_flagged_list = grade_to_set.get('examples', [])
		self.log('auto_flagged_list updated: \n{}'.format(self.auto_flagged_list))

	def reset(self):
		# cmds.intField(self.grade_intField, edit = True, value = 0)
		# self.update_subcategory('intField')
		cmds.scrollField(self.comments_text_field, edit = True, text = '')
		self.update_subcategory('comments_text')
		# cmds.scrollField(self.default_comments, edit = True, text = '')
		# self.update_subcategory('default_comments_text')
		# cmds.scrollField(self.example_comments, edit = True, text = '')
		# self.update_subcategory('example_comments_text')
		# self.log('reset subsection: {}'.format(self.title))
		# self.log('Selection hidden radio')
		# cmds.radioButton(self.resetRadioButton, edit = True, select = True)
		self.log('hidden radio selected')
		# self.is_complete = False
		#collapse frames

		#cmds.frameLayout(self.subcat_comments_frame_layout, edit = True, collapse = False)
		
		# self.maintain_default_comment_visibility()

		# if self.autocomplete:
		# 	self.autocomplete_update()

	def update(self):
		self.current_grade_value = cmds.intField(self.grade_intField, query = True, value = True)
		self.current_default_comment_text = cmds.scrollField(self.default_comments, query = True, text = True)
		# self.current_example_comment_text = cmds.scrollField(self.example_comments, query = True, text = True)
		self.current_comment_text = cmds.scrollField(self.comments_text_field, query = True, text = True)

	# def disable(self):
	# 	cmds.formLayout(self.subcat_main_column_layout, edit = True, enable = False)

	# def enable(self):
	# 	cmds.formLayout(self.subcat_main_column_layout, edit = True, enable = True)

	def log(self, message, prefix = '.:subcategory_class::', hush = True):
		"""
		print stuff yo!
		"""
		if not hush:
			print("%s: %s" % (prefix, message))

class MainCategoryGradeSection(object):

	def __init__(self, mainCategoryFromXML, defaultsFromXML, configDict):

		self.colors = configDict['colors']
		self.configDict = configDict

		scrollField_height = 100
		row_spacing = 0

		self.current_highnote_comment_text = ''
		# self.current_grade_value = 0 

		# self.updatePGS = updateFunction

		self.log("Main Category Initializing")
		self.maincategory = mainCategoryFromXML
		self.defaults = defaultsFromXML

		# self.log('\n\nGutCheck:')
		# self.gutCheck = None
		
		# if self.maincategory.find('gutCheck') != None:
		# 	self.gutCheck = self.maincategory.find('gutCheck').text
		# self.log('{}\n\n'.format(self.gutCheck))

		self.rmb = []
		if self.maincategory.findall('RMB'):
			for item in self.maincategory.findall('RMB'):
				self.rmb.append([item.get('title'), item.text, item.get('divider')])

		self.log('\nRiGHT HERE!')
		if self.rmb != []:
			for item in self.rmb:
				self.log('\nTitle: {}\n{}'.format(item[0], item[1]))
		self.log('RMB: {}'.format(self.rmb))
		
		self.title = self.maincategory.get('title')
		if self.title == None:
			self.title = self.maincategory.find('title').text

		# self.weight = self.maincategory.get('weight')
		# if self.weight == None:
		# 	self.weight = self.maincategory.find('weight').text
			
		# self.log('{} Category Weight: {}'.format(self.title, self.weight))

		self.mainCategoryRootScrollLayout = cmds.scrollLayout(childResizable = True)
		self.maincat_main_column_layout = cmds.formLayout(parent = self.mainCategoryRootScrollLayout, numberOfDivisions = 100, enable = True)

		self.mainFrameLayout = cmds.frameLayout(label = 'Category Comments',collapsable = False, collapse = False, backgroundColor = self.colors['dim'])

		# P3 Update - comment out
		# if self.gutCheck == 'True':
		# 	self.log('running gut check GUI stuff')
		# 	self.gutCheckFrameLayout = cmds.frameLayout(label = 'Gut Check', collapsable = True, collapse = self.configDict['manage states']['collapse gut check'], backgroundColor = self.colors['dim'])
		# 	self.gutCheckWindowGo()
		# 	cmds.setParent(self.mainFrameLayout)

		self.highnote_comments = cmds.scrollField( height = scrollField_height, wordWrap = True, changeCommand = lambda *args: self.update_maincategory('highnotes', *args)) 

		self.rmb_menu = cmds.popupMenu(parent = self.highnote_comments, button = 3)
			# i = 0
		if self.rmb != []:
			for item in self.rmb:
				
				divider = item[2]
				if divider != None and divider.lower() == "true":
					divider = True
				if divider == None:
					divider = False				

				self.log('{}:{}'.format(item[0], item[1]))
				cmds.menuItem(label = item[0], command = lambda args, i = item[1]:self.add_comment_to_comments(i), divider = divider)
				# i += 1

		cmds.menuItem(divider = True)
		cmds.menuItem(label = 'Select Multiple Comments', command = lambda *args: self.selectMultipleCategoryComments())
		cmds.menuItem(divider = True)
		cmds.menuItem(divider = True)
		cmds.menuItem(label = 'Clear Category Comments', command = self.clear_category_comments)


		cmds.setParent(self.mainFrameLayout)
		cmds.setParent(self.maincat_main_column_layout)

		#attach the highnotes to the formlayout
		cmds.formLayout(self.maincat_main_column_layout, edit = True, 
			attachForm=[(self.mainFrameLayout, 'top', 0), (self.mainFrameLayout, 'left', 0), (self.mainFrameLayout, 'right', 0) ],
		    )

		subcatColumnLayout = cmds.formLayout(numberOfDivisions = 100)

		self.subcategories = []#this will be the subcategory object
		# self.log('maincategory: %s' % self.maincategory.find('title').text)
		self.log('main category title: %s' % self.title)
		self.subcats = self.maincategory.findall('subcategory') #this is the xml subcategory
		self.log('subcategories found: %s' % self.subcats)


		#create subcats
		for sub in self.subcats:
			self.subcategories.append(SubcategoryGradeSection(sub, self.defaults, self.runAuto, self.configDict))
			cmds.setParent(subcatColumnLayout)

		# attach subcats to form layout
		cmds.formLayout(subcatColumnLayout, edit = True, 
			attachForm = [(self.subcategories[0].subcat_comments_frame_layout, 'top', 0), 
						(self.subcategories[0].subcat_comments_frame_layout, 'left', 0), 
						(self.subcategories[0].subcat_comments_frame_layout, 'right', 0)]
			)
		# cmds.formLayout(subcatColumnLayout, edit = True, 
		# 	attachForm = [(self.subcategories[0].subcat_comments_frame_layout, 'left', 0), (self.subcategories[0].subcat_comments_frame_layout, 'right', 0)],
		# 	attachControl = [(self.subcategories[0].subcat_comments_frame_layout, 'top', 5, self.subcategories[0].subcat_main_column_layout)]
		# 	)
		temp_parent = self.subcategories[0].subcat_comments_frame_layout
		for sub in self.subcategories[1:]:

			#attach grade section of subcat
			# cmds.formLayout(subcatColumnLayout, edit = True, 
			# attachForm = [(sub.subcat_main_column_layout, 'left', 0), (sub.subcat_main_column_layout, 'right', 0)],
			# attachControl = [(sub.subcat_main_column_layout, 'top', 5, temp_parent)]
			# )
			# temp_parent = sub.subcat_main_column_layout

			#attach comment section of subcat
			cmds.formLayout(subcatColumnLayout, edit = True, 
			attachForm = [(sub.subcat_comments_frame_layout, 'left', 0), (sub.subcat_comments_frame_layout, 'right', 0)],
			attachControl = [(sub.subcat_comments_frame_layout, 'top', 5, temp_parent)]
			)
			temp_parent = sub.subcat_comments_frame_layout

		
		# cmds.setParent(self.maincat_main_column_layout)
		cmds.formLayout(self.maincat_main_column_layout, edit = True, 
			attachForm = [(subcatColumnLayout, 'left', 0), (subcatColumnLayout, 'right', 0)],
			attachControl = [(subcatColumnLayout, 'top', 5, self.mainFrameLayout)]
			)

		#####
		#####
		#####
		#####

		# begin edit 5/2/23
		# add previous and next category buttons
		# self.previous_tab_button = cmds.button("previous tab button", label = "< Previous")
		# self.next_tab_button = cmds.button("next tab button", label = "Next >")
		# cmds.setParent(self.maincat_main_column_layout)

		# print("Previous: {}".format(self.previous_tab_button))
		# print("Next: {}".format(self.next_tab_button))

		# attach buttons to frame
		# cmds.formLayout(self.maincat_main_column_layout, edit = True, 
		# 	attachForm = [(self.previous_tab_button, 'left', 0),(self.previous_tab_button, 'bottom', 0), (self.next_tab_button, 'right', 0), (self.next_tab_button, 'bottom', 0)],
		# 	attachControl = [(self.next_tab_button, 'left', 5, self.previous_tab_button)], 
		# 	attachPosition = [(self.previous_tab_button, 'right', 0, 50)]
		# 	)

		#####
		#####
		#####
		#####

	# def set_previous_category_button_command(self, new_command):
	# 	cmds.button(self.previous_tab_button, edit = True, command = new_command)

	# def set_next_category_button_command(self, new_command):
	# 	cmds.button(self.next_tab_button, edit = True, command = new_command)


	def append_session_commment(self):
		self.log('append session comment stuff')

		def close_command(*args):
			self.log('close command')
			# maya.utils.executeDeferred("cmds.deleteUI('ASCW')")

		def get_comment(*args):
			self.log('get comment')
			title = cmds.textField(comment_title, query = True, text = True)
			comment = cmds.scrollField(comment_text, query = True, text = True)
			self.log('Title: {}\nComment: {}'.format(title, comment))
			if title != 'Comment Title' and comment != 'Type your comment text here...':
				cmds.menuItem(parent = self.rmb_menu, label = title, command = lambda args, i = comment:self.add_comment_to_comments(i))
				cmds.deleteUI('ASCW')
			else:
				cmds.error('Type in a comment title and comment text to continue.\nClose the window to cancel.')

		self.log('make comment window')
		window_widthHeight = (250, 200)
		padding = 2

		#if ASCW window exists delete it
		if (cmds.window('ASCW', exists = True)):
			cmds.deleteUI('ASCW')

		comment_window = cmds.window('ASCW', title = 'Append Session Comment', 
									width = window_widthHeight[0], 
									height = window_widthHeight[1],
									closeCommand = close_command)
		comment_form = cmds.formLayout(numberOfDivisions = 250)
		comment_title = cmds.textField(text = 'Comment Title')
		comment_text = cmds.scrollField(editable = True, wordWrap = True, text = 'Type your comment text here...')
		comment_btn = cmds.button(label = 'Append Comment', command = get_comment)
		cmds.setParent('..')

		cmds.formLayout(comment_form, edit = True, attachForm = [
			(comment_title, 'left', padding),
			(comment_title, 'right', padding),
			(comment_title, 'top', padding),
			(comment_text, 'left', padding),
			(comment_text, 'right', padding),
			(comment_btn, 'left', padding), 
			(comment_btn, 'right', padding), 
			(comment_btn, 'bottom', padding)], 
			attachControl = [
			(comment_text, 'top', padding, comment_title),
			(comment_text, 'bottom', padding, comment_btn)])
		cmds.showWindow(comment_window)
	
	def selectMultipleCategoryComments(self, *args):

		def collectComments(self, *args):
			comments = ""
			for element in rccCheckBoxes:
				# print("element: {}".format(element))
				if cmds.checkBox(element[0], query = True, value = True):
					comments += element[1]

			self.add_comment_to_comments(comments)

			cmds.deleteUI('SelectMultipleCommmentsWindow')

		def clearAll(self, *args):
			for element in rccCheckBoxes:
				cmds.checkBox(element[0], edit = True, value = False)


		# window_widthHeight = (280, 600)
		elementWidth = 300
		elementCount = 2

		#if SelectMultipleCommmentsWindow window exists delete it
		if (cmds.window('SelectMultipleCommmentsWindow', exists = True)):
			cmds.deleteUI('SelectMultipleCommmentsWindow')

		comment_window = cmds.window('SelectMultipleCommmentsWindow', title = 'Select Multiple Comments')

		rccFormLayout = cmds.formLayout(parent = comment_window, numberOfDivisions = 100)
		rccScrollLayout = cmds.scrollLayout(parent = rccFormLayout)

		cmds.formLayout(rccFormLayout, edit = True, 
			attachForm=[(rccScrollLayout, 'top', 5), (rccScrollLayout, 'left', 5), 
		    			(rccScrollLayout, 'bottom', 5), (rccScrollLayout, 'right', 5)])

		# self.rmb [0] title, [1] text, [2] divider

		cmds.button(parent = rccScrollLayout, label = "Clear All",  width = elementWidth, command = clearAll, backgroundColor = self.configDict["colors"]['dim'])

		rccCheckBoxes = []

		# rcc[0] = title
		# rcc[1] = comment
		# rcc[2] = divider status
		for rcc in self.rmb:
			elementCount += 1

			isTitle = rcc[2] # if it is a divider, disable
			if isTitle != None and isTitle.lower() == "true":
				isTitle = True
			if isTitle == None:
				isTitle = False	

			# print('RCC: {}: {}'.format(rcc[0], rcc[1]))
			if isTitle:
				cmds.text(parent = rccScrollLayout, label = rcc[0],  font = "boldLabelFont", backgroundColor = tuple(map(lambda i : i - 0.03,  self.configDict["colors"]['dim'])))
			else:
				if rcc[1] != None:
					if rcc[1].strip() != '':
						rccCheckBoxes.append( (cmds.checkBox(parent = rccScrollLayout, label = rcc[0] ), rcc[1]))

		cmds.button(parent = rccScrollLayout, label = "Add to Comments and Close", width = elementWidth, command = lambda args: collectComments(self), backgroundColor = self.configDict["colors"]['dim'])
		# cmds.window('SelectMultipleCommmentsWindow', edit = True, height = (elementCount * 10), width = elementWidth)

		cmds.showWindow(comment_window)

	def add_comment_to_comments(self, comment, *args):
		self.log('add comment to comments')
		# text_bucket = cmds.scrollField(self.highnote_comments, query = True, text = True)
		# # self.log('index: {}'.format(index))
		# self.log('RMB: {}'.format(self.rmb))
		# text_bucket += ' {}'.format(comment)
		# cmds.scrollField(self.highnote_comments, edit = True, text = text_bucket)
		# print("Insert Position: {}".format(cmds.scrollField(self.highnote_comments, query = True, insertionPosition = True)))
		cmds.scrollField(self.highnote_comments, edit = True, insertText = " {}".format(comment), insertionPosition = 0)

		self.update_maincategory('highnotes')

	# def enable(self):
	# 	self.log('enable the section')
	# 	cmds.formLayout(self.maincat_main_column_layout, edit = True, enable = True)
	# 	for sub in self.subcategories:
	# 		sub.enable()

	# def disable(self):
	# 	self.log('disable the section')
	# 	cmds.formLayout(self.maincat_main_column_layout, edit = True, enable = False)
	# 	for sub in self.subcategories:
	# 		sub.disable()
	# 	self.log('did it work?')

	def gutCheckGo(self, *args):
		self.log('gut check')
		self.disable()
		self.gutCheckWindowGo()

	def gutCheckWindowGo(self, *args):
		self.log('gut check window')

		row_spacing = 0

		self.gutCheckWindow = cmds.formLayout(numberOfDivisions = 100)
		# gutCheckLabel = cmds.text(label = 'Gut Check Input', align = 'left')

		quick_set_formLayout = cmds.formLayout(numberOfDivisions = 100)
		btn100 = cmds.button(label = 100, command = lambda *args: self.quick_set(100))
		btn75 = cmds.button(label = 75, command = lambda *args: self.quick_set(75))
		btn50 = cmds.button(label = 50, command = lambda *args: self.quick_set(50))
		btn25 = cmds.button(label = 25, command = lambda *args: self.quick_set(25))
		btnReset = cmds.button(label = "Reset", command = self.quick_reset)
		cmds.setParent('..')

		cmds.formLayout(quick_set_formLayout, edit = True, 
						attachForm = [(btnReset, 'right', 10), (btnReset, 'top', 0),
									  (btn100, 'left', 0), (btn100, 'top', 0), 
									  (btn75, 'top', 0), (btn50, 'top', 0), (btn25, 'top', 0)],
						attachControl = [(btn75, 'left', 5, btn100),
										 (btn50, 'left', 5, btn75),
										 (btn25, 'left', 5, btn50), 
										 (btnReset, 'left', 5, btn25)],
						attachPosition = [(btn100, 'right', 5, 20),
										  (btn75, 'right', 5, 40),
										  (btn50, 'right', 5, 60), 
										  (btn25, 'right', 5, 80)])
		
		gutCheck_int_field_slider_row_layout = cmds.formLayout(numberOfDivisions = 100)
		self.gutCheck_grade_intField = cmds.intField( minValue=0, maxValue=150, step=1 , width = 36, 
													changeCommand = lambda *args: self.gutCheck_update('field'))
		self.gutCheck_grade_slider = cmds.intSlider( min=-100, max=0, value=0, step=1, 
													changeCommand = lambda *args: self.gutCheck_update('slider'), dragCommand = lambda *args: self.gutCheck_update('slider'))
		cmds.setParent('..')

		cmds.formLayout(gutCheck_int_field_slider_row_layout, edit = True,
			attachForm = [(self.gutCheck_grade_intField, 'left', 0),(self.gutCheck_grade_slider, 'right', 0)],
			attachControl = [(self.gutCheck_grade_slider, 'left', 5, self.gutCheck_grade_intField)]
			)

		gut_check_commit_button = cmds.button(label = 'Commit', command = self.gutCheckSet)
		cmds.setParent('..')

		cmds.formLayout(self.gutCheckWindow, edit = True, 
			attachForm = [(quick_set_formLayout, 'left', 0), (quick_set_formLayout, 'top', 0), (quick_set_formLayout, 'right', 0),
			(gutCheck_int_field_slider_row_layout, 'left', 0), (gutCheck_int_field_slider_row_layout, 'right', 10),
			(gut_check_commit_button, 'left', 0), (gut_check_commit_button, 'right', 0)],
			attachControl = [(gutCheck_int_field_slider_row_layout, 'top', 5, quick_set_formLayout),(gut_check_commit_button, 'top', 2, gutCheck_int_field_slider_row_layout)]
			)
		
	# facilitate the quick set gut check - set the int field to the quick set value and update
	def quick_set(self, value):
		cmds.intField(self.gutCheck_grade_intField, edit = True, value = value)
		self.gutCheckSet()

	def quick_reset(self, *args):
		self.reset()
		self.gutCheckReset()

	def gutCheck_update(self, controlType):
		self.log('gut check update')
		if controlType == 'slider':
			value = cmds.intSlider(self.gutCheck_grade_slider, query = True, value = True)
			cmds.intField(self.gutCheck_grade_intField, edit = True, value = -value)
		elif controlType == 'field':
			value = cmds.intField(self.gutCheck_grade_intField, query = True, value = True)
			cmds.intSlider(self.gutCheck_grade_slider, edit = True, value = -value)

	def gutCheckSet(self, *args):
		self.log('gut check set')
		value = cmds.intField(self.gutCheck_grade_intField, query = True, value = True)
		for sub in self.subcategories:
			sub.gutCheck_update(value)

		self.gutCheckReset()

	def gutCheckReset(self, *args):
		self.log('gut check reset!')
		cmds.intField(self.gutCheck_grade_intField, edit = True, value = 0)
		self.gutCheck_update('field')
		# print('toggleCollapseGutCheck_state: {}'.format(self.configDict['manage states']['collapse gut check']))
		cmds.frameLayout(self.gutCheckFrameLayout, edit = True, collapse = self.configDict['manage states']['collapse gut check'])
		cmds.frameLayout(self.mainFrameLayout, edit = True, collapse = False)

	def gutCheckCancel(self, *args):
		self.log('gut check cancel')
		self.enable()

	def autoProGo(self):
		self.log('defaults: {}'.format(self.defaults))
		self.log('defaults.findall("auto"): {}'.format(self.defaults.findall('auto')[0]))
		self.log('!!! autoText: {}'.format(self.defaults.findall('auto')[0].text))
		if self.defaults.findall('auto')[0].text :
			for sub in self.subcategories:
				try:
					self.runAuto(self.defaults, sub)
				except RuntimeError as e:
					cmds.warning('Error running automation. Skipping section: {}\n{}'.format(sub.title, e))

			self.updatePGS()

	def runAuto(self, defaultsFromXML, single_subcat, auto = False):
		# this section handles all the automation linking on the subcategories
		subcatXMLElement = single_subcat.subcatXML
		if not auto:
			try:
				self.log("Lets try")
				self.log(defaultsFromXML.find('auto').text)
				self.log('subcatXMLElement:')
				sub_title1 = subcatXMLElement.get('title')
				if sub_title1 == None:
					sub_title1 = subcatXMLElement.find('title').text
				self.log('subcat title: %s' % sub_title1) 
				# self.log(subcatXMLElement.find('auto').text)
				self.log("did those last two print?")
				subcat_auto = None
				if subcatXMLElement.find('auto') != None:
					subcat_auto = subcatXMLElement.find('auto').text
				if subcat_auto == '' or subcat_auto == None:
					subcat_auto = False
				if (defaultsFromXML.find('auto').text == 'True') and subcat_auto:
					self.log('auto.text is %s' % subcatXMLElement.find('auto').text)
					auto = True
			except AttributeError as e:
				self.log('AttributeError for Auto test: \n{}'.format(e))
				# cmds.warning('AttributeError: {}'.format(sys.exc_info()[2].tb_lineno))
				cmds.warning('AttributeError: {}: Line {}'.format(e,sys.exc_info()[2].tb_lineno))
				pass

		if auto:
			self.log(subcatXMLElement.find('auto').text)
			autoScriptName = subcatXMLElement.find('auto').text
			self.log('auto is True!!!')
			import pabuito_auto as autoRun
			# reload(autoRun)
			# autoScripts = dir(autoRun)
			folder_name = defaultsFromXML.find('auto').get('folder')
			if folder_name != None:
				autoRun = getattr(autoRun, folder_name)
			autoScripts = dir(autoRun)
			self.log('Methods in auto run are \n %s' % autoScripts)
			defaultMethods = defaultsList = ['__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__']
			autoScriptModules = []
			for method in autoScripts:
				if method not in defaultMethods:
					autoScriptModules.append(method)
			self.log('autoScriptModules: %s' % autoScriptModules)
			self.log('autoScriptName: %s' % autoScriptName)

			# print('auoScriptModules:')
			# for mod in autoScriptModules:
			# 	print(mod)
				
			if autoScriptName in autoScriptModules:
				self.log('Found AutoScript!')
				returnDict = getattr(getattr(autoRun, autoScriptName), autoScriptName)(self.defaults)
				self.log(returnDict)
				sub_title = subcatXMLElement.get('title')
				if sub_title == None:
					sub_title = subcatXMLElement.find('title').text
				returnDict['section_title'] = sub_title
				self.log('section_title: %s' % returnDict['section_title'])
				single_subcat.this_is_the_grade(returnDict)
			else:
				self.log('Failed to find autoScriptName')
				cmds.warning('Failed to find autoScriptName: {}'.format(autoScriptName))

		else:
			self.log('FALSE FALSE FALSE')

	def update_maincategory(self, section, *args):
		self.log('updating %s' % section)
		if section == 'highnotes':
			self.current_highnote_comment_text = cmds.scrollField(self.highnote_comments, query = True, text = True)

	def update(self):
		self.current_highnote_comment_text = cmds.scrollField(self.highnote_comments, query = True, text = True)
		for subcat in self.subcategories:
			subcat.update()

	def check_grade_status(self):
		self.log('checking %s section grade status' % self.title)
		currentGrade = 0
		catWeightAndValue = []
		for subcat in self.subcategories:
			catWeightAndValue.append((subcat.weight, subcat.current_grade_value))
		for cat in catWeightAndValue:
			currentGrade += ((float(cat[0])/100)*float(cat[1]))
		return (self.title, self.weight, currentGrade)

	def what_is_the_grade(self):
		self.log('collect grades from subsections')
		return_list = []
		return_list.append(self.title)
		# return_list.append(self.weight)

		# update highnotes before returning
		self.update_maincategory("highnotes")

		return_list.append(self.current_highnote_comment_text)
		# sectionGradeTotal = 0
		subGradeList = []
		for sub in self.subcategories:
			subGradeList.append(sub.what_is_the_grade())
			# self.log('Grade weight and value: {} * {}'.format(sub.what_is_the_grade()['grade_value'], sub.what_is_the_grade()['section_weight']))
		# 	sectionGradeTotal += (sub.what_is_the_grade()['grade_value'] * (float(sub.what_is_the_grade()['section_weight'])/100.0))
		# return_list.append(sectionGradeTotal)
		return_list.append(subGradeList)
		return return_list

	def this_is_the_grade(self, gradeList):
		sectionGrades = gradeList
		i = 0
		for item in sectionGrades:
			self.log('index {} of sectionGrades: {}'.format(i, item))
			i+=1
		self.log('\n\nStill needs to set high notes\n\n')
		cmds.scrollField(self.highnote_comments, edit = True, text = sectionGrades[2])
		self.update_maincategory('highnotes')
		self.log('section[3]:\n{}'.format(sectionGrades[4]))
		for sub in self.subcategories:
			for index in sectionGrades[4]:
				if sub.title == index['section_title']:
					sub.this_is_the_grade(index)

	def are_you_complete(self):
		incomplete_titles = []
		for sub in self.subcategories:
			self.log("Testing sub for complete-ness: %s" % sub.title)
			if not sub.is_complete:
				self.log('adding {} to incomplete_titles'.format(sub.title))
				incomplete_titles.append(sub.title)
				# return False
		self.log('incomplete_titles: \n{}'.format(incomplete_titles))
		return incomplete_titles
		# return True
	
	def clear_category_comments(self, *args):
		cmds.scrollField(self.highnote_comments, edit = True, text = '')
		self.update_maincategory('highnotes')

	def reset(self, *args):
		self.log('resetting main section')
		cmds.scrollField(self.highnote_comments, edit = True, text = '')
		# cmds.frameLayout(self.mainFrameLayout, edit = True, collapse = True)
		# self.disable()

		# print('toggleCollapseGutCheck_state: {}'.format(self.configDict['manage states']['collapse gut check']))
		# print("Category Title: {}".format(self.title))
		
		# P3 Update - commented out
		# if self.gutCheck == 'True':
		# 	cmds.frameLayout(self.gutCheckFrameLayout, edit = True, collapse = self.configDict['manage states']['collapse gut check'])

		for sub in self.subcategories:
			sub.reset()
		self.update_maincategory('highnotes')

		cmds.scrollLayout(self.mainCategoryRootScrollLayout, edit = True, scrollPage = "up")
		self.log('Main section {} reset'.format(self.title))

	def log(self, message, prefix = '.:main_category_class::', hush = True):
		"""
		print stuff yo!
		"""
		if not hush:
			print("%s: %s" % (prefix, message))