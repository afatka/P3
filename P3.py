"""
 This class controls the main window of the P3 Grading System. It deals with tabbing the main sections as well as holding all the relavent information. 

"""
# P3 Version 1.0

import maya.cmds as cmds
import xml.etree.ElementTree as etree
from P3 import cat_class as category_class
import os
import errno
import textwrap
import random
import json

from . import pyperclip
import importlib
importlib.reload(category_class)


class P3(object):

	def __init__(self, xmlFileLocation):

		version = 2403
		self.development = False

		self.fail_message = [
			('A P3 Section is not complete', 'Ok'),
			('You haven\'t completed the tool. Dummy', 'Ok'),
			('Please finish grading before cycling to the next file', 'Ok'),
			('What a dingus...You\'re not finished yet', 'Ok'),
			('What did the error say?', 'I can read...'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			('A P3 Section is not complete', 'Ok'),
			]


		self.xmlFile = xmlFileLocation
		if xmlFileLocation.endswith('.xml'):
			self.log('xml is an xml \n\n')
			self.xml_elementTree = etree.ElementTree(file = self.xmlFile)
		else:
			cmds.error('Unknown file type loaded.')

		self.xml_elementRoot = self.xml_elementTree.getroot()

		self.xml_elementDefaults = self.xml_elementRoot.find('defaults')
		self.xml_elementMainCategories = self.xml_elementRoot.findall('category')

		# self.validateXML()

		# 5/3/23 get title validation information (Student Name field validation)
		self.title_validation = self.xml_elementDefaults.find('title_field_validation')
		if self.title_validation != None:
			self.validation_state = self.title_validation.get('state')
			if self.validation_state == None or self.validation_state == 'False':
				self.validation_state = False
			elif self.validation_state == 'True':
				self.validation_state = True
		else:
			self.validation_state = False

		try:
			print('title_validation: {}'.format(self.title_validation))
			print('none: {}'.format(self.title_validation.get('chicken')))
			print('state: {}'.format(self.validation_state))
			print('regex: {}'.format(self.title_validation.text))
		except:
			pass

		# self.windowWidth = 350
		subcategoryHeight = 250 #780
		windowBufferHeight = 55
		self.windowHeight = 500 #825
		windowTitle = os.path.basename(self.xmlFile).split('.')[0]

		self.uiPadding = 2

		self.outputModel = 'root'
		# if self.xml_elementDefaults.find('auto').text == 'True':
		# 	self.log('Auto Defaults: True')
		# 	self.runAuto = True
		# 	autoLabel = 'RunAuto - On'
		# else:
		# 	self.log('Auto Defaults: False')
		# 	self.runAuto = False
		# 	autoLabel = 'RunAuto - Off'

		#if P3 window exists delete it
		if (cmds.window('P3Window', exists = True)):
			cmds.deleteUI('P3Window')
		# if preferences exist, delete them
		if self.development:
			if (cmds.windowPref('P3Window', exists = True)):
				cmds.windowPref('P3Window', remove = True)

		# paths
		self.directories = { "root_dir" : os.path.dirname(__file__)}
		self.directories["icon_dir"] = os.path.join(self.directories['root_dir'], "icons")
		self.jsonConfigLocation = os.path.join(self.directories['root_dir'], 'config.json')

		# configs
		self.configs = {}
		self.loadConfigsFromJson()

		self.icons = { "history_icon" : os.path.join(self.directories['icon_dir'], self.configs['icon names']['history_icon'])}

		# title field
		self.titleFieldContent = ''

		P3_window = cmds.window('P3Window', title = 'P3 (v.{1}): {0}'.format(windowTitle,version), iconName = 'P3', height = self.windowHeight)
		cmds.formLayout('rootLayout', numberOfDivisions = 100)
		cmds.formLayout('topRow', numberOfDivisions = 100)
		##This is the top button area

		iconbuttonsize = 32
		cmds.iconTextButton ('queueButton', style = "iconOnly", image1 = self.icons['history_icon'], enable = True, width = iconbuttonsize, height = iconbuttonsize )
		if self.configs['manage states']['copy html']:
			cmds.button('copyFeedbackButton', label = "Copy HTML Text", command = lambda x: self.finished_grading(True))
		else:
			cmds.button('copyFeedbackButton', label = "Copy Plain Text", command =  lambda x: self.finished_grading(False))
		# cmds.textField('titleField', placeholderText = "Student Name", )

		# titleFieldMenu = cmds.popupMenu(parent = 'titleField', button = 3)
		# cmds.menuItem(parent = titleFieldMenu, label = 'Paste', command = self.pasteTitle)
		# cmds.menuItem(parent = titleFieldMenu, label = 'Trim Path', command = self.trimTitle)
		# cmds.menuItem(parent = titleFieldMenu, label = 'Clear', command = self.resetTitle)
		# cmds.menuItem(parent = titleFieldMenu, label = 'Validate Title', command = self.toggle_validate_title_field)

		self.settings_menu = cmds.popupMenu(parent = 'queueButton', button = 1)
		cmds.menuItem(parent = self.settings_menu, label = "Reset Tool", command = self.resetTool)
		cmds.menuItem(parent = self.settings_menu, label = 'Toggle HTML/Plain Text Copy', command = self.toggleCopy)
		cmds.menuItem(parent = self.settings_menu, label = "On Copy", divider = True)
		cmds.menuItem('ResetTitleOnCopy', parent = self.settings_menu, label = "Reset Title", checkBox = self.configs['manage states']['reset title on copy'], command = self.toggleResetTitleOnCopy)
		cmds.menuItem('ResetOnCopy',parent = self.settings_menu, label = "Reset Categories", checkBox = self.configs['manage states']['reset on copy'], command = self.toggleResetOnCopy)
		cmds.menuItem(parent = self.settings_menu, label = "Settings", divider = True)
		cmds.menuItem('TitleisRequired',parent = self.settings_menu, label = "Title is Required", checkBox = self.configs['manage states']['title is required'], command = self.toggleTitleIsRequired)
		# cmds.menuItem('CollapseGutCheck', parent = self.settings_menu, label = "Collapse Gut Check on Set/Reset", checkBox = self.configs['manage states']['collapse gut check'], command = self.toggleCollapseGutCheck) # P3 Update comment out

		cmds.menuItem(parent = self.settings_menu, divider = True)
		cmds.menuItem(parent = self.settings_menu, divider = True)
		cmds.menuItem(parent = self.settings_menu, label = "Reset All Configs to Defaults", command = self.resetConfigsToDefaults)

		# self.queue_menu = cmds.popupMenu(parent = 'queueButton', button = 1)
		# cmds.menuItem(parent = self.queue_menu, divider = True, dividerLabel = "Copy Recent")

		# self.history_queue_items = [['1.',""], ['2.',""], ['3.',""], ['4.',""], ['5.',""]]
		# self.history_queue_menuItems = []
		# self.history_queue_menuItems.append(cmds.menuItem(parent = self.queue_menu, label = self.history_queue_items[0][0]))
		# self.history_queue_menuItems.append(cmds.menuItem(parent = self.queue_menu, label = self.history_queue_items[1][0]))
		# self.history_queue_menuItems.append(cmds.menuItem(parent = self.queue_menu, label = self.history_queue_items[2][0]))
		# self.history_queue_menuItems.append(cmds.menuItem(parent = self.queue_menu, label = self.history_queue_items[3][0]))
		# self.history_queue_menuItems.append(cmds.menuItem(parent = self.queue_menu, label = self.history_queue_items[4][0]))

		##End top button area
		cmds.setParent('topRow')
		cmds.setParent('rootLayout')

		# attach buttons to form
		topMostMargin = 5
		bottomMostMargin = 5
		leftMostMargin = 10
		rightMostMargin = 10
		centerHorizontalMargin = 10
		centerVerticalMargin = 5

		# cmds.formLayout( 'topRow', edit=True, 
		#     attachForm=[('queueButton', 'top', topMostMargin), ('queueButton', 'left', leftMostMargin), 
		#     			('copyFeedbackButton', 'top', topMostMargin), ('copyFeedbackButton', 'right', rightMostMargin),
		#     			('titleField', 'bottom', bottomMostMargin), ('titleField', 'right', rightMostMargin)],
		#     attachControl = [('copyFeedbackButton', 'left', centerHorizontalMargin, 'queueButton'),
		#     				('titleField', 'left', centerHorizontalMargin, 'queueButton'), ('titleField', 'top', centerVerticalMargin, 'copyFeedbackButton')])

		cmds.formLayout( 'topRow', edit=True, 
		    attachForm=[('queueButton', 'top', topMostMargin), ('queueButton', 'left', leftMostMargin), 
		    			('copyFeedbackButton', 'top', topMostMargin), ('copyFeedbackButton', 'right', rightMostMargin),
		    			('copyFeedbackButton', 'bottom', bottomMostMargin)],
		    attachControl = [('copyFeedbackButton', 'left', centerHorizontalMargin, 'queueButton')])

		# attach top row layout to root layout
		cmds.formLayout('rootLayout', edit = True, attachForm = [('topRow', 'top', 0), ('topRow', 'left', 0), ('topRow', 'right', 0)])

		cmds.formLayout('bodyFormLayout', numberOfDivisions = 100)

		gradeSectionsFormLayoutVar = cmds.formLayout(numberOfDivisions = 100)

		cmds.formLayout('scroll_formLayout', numberOfDivisions = 100)	

		#set up the tab layout for the main categories
		self.mainCategories = []
		cmds.formLayout('tab_formLayout', numberOfDivisions = 100)
		self.pgs_tabLayout = cmds.tabLayout('pgs_tabLayout',  height = subcategoryHeight,  childResizable = True)
		cmds.formLayout('tab_formLayout', edit = True, 
			attachForm=[('pgs_tabLayout', 'top', 0), ('pgs_tabLayout', 'left', 0), ('pgs_tabLayout', 'bottom', 0), ('pgs_tabLayout', 'right', 0) ],
			)


		#create main category sections
		for category in self.xml_elementMainCategories:
			self.mainCategories.append(category_class.MainCategoryGradeSection(category, self.xml_elementDefaults, self.configs))
			cmds.setParent(self.pgs_tabLayout)

		#make all main categories children of the tab layout
		for tab in self.mainCategories:
			cmds.tabLayout(self.pgs_tabLayout, edit = True, tabLabel = (tab.mainCategoryRootScrollLayout, tab.title))

		cmds.setParent('scroll_formLayout')
		cmds.formLayout('scroll_formLayout', edit = True, attachForm = [
			('tab_formLayout', 'left', self.uiPadding),
			('tab_formLayout', 'right', self.uiPadding),
			('tab_formLayout', 'top', self.uiPadding),
			('tab_formLayout', 'bottom', self.uiPadding)
			])

		cmds.setParent(gradeSectionsFormLayoutVar)
		cmds.formLayout(gradeSectionsFormLayoutVar, edit = True, attachForm = [
			('scroll_formLayout', 'left', self.uiPadding),
			('scroll_formLayout', 'right', self.uiPadding),
			('scroll_formLayout', 'top', self.uiPadding),
			('scroll_formLayout', 'bottom', self.uiPadding)
			])


		cmds.setParent('bodyFormLayout')

		cmds.formLayout('bodyFormLayout', edit = True, attachForm = [
			(gradeSectionsFormLayoutVar, 'top', self.uiPadding),
			(gradeSectionsFormLayoutVar, 'left', self.uiPadding),
			(gradeSectionsFormLayoutVar, 'top', self.uiPadding),
			(gradeSectionsFormLayoutVar, 'right', self.uiPadding),
			(gradeSectionsFormLayoutVar, 'bottom', self.uiPadding)
			])


		cmds.setParent('..')#main column Layout
		cmds.formLayout('rootLayout',edit = True, 
			attachForm = [
			('topRow', 'left', self.uiPadding),('topRow', 'right', self.uiPadding), ('topRow', 'top', self.uiPadding),
			('bodyFormLayout', 'left', self.uiPadding), ('bodyFormLayout', 'right', self.uiPadding),
			('bodyFormLayout', 'bottom', self.uiPadding)
			],
			attachControl = [
			('bodyFormLayout', 'top', self.uiPadding, 'topRow'),
			])

		# assign view category commands to buttons in categories
		# for cat in self.mainCategories:
		# 	cat.set_previous_category_button_command(self.view_previous_category)
		# 	cat.set_next_category_button_command(self.view_next_category)

		cmds.showWindow( P3_window )

		# self.enable();

	def view_next_category(self, *args):
		tab_count = self.get_tab_count()
		current_tab = self.get_tab_index()
		if current_tab + 1 <= tab_count:
			self.set_tab_index(current_tab + 1)
		else:
			self.set_tab_index(1)

	def view_previous_category(self, *args):
		tab_count = self.get_tab_count()
		current_tab = self.get_tab_index()
		if current_tab - 1 > 0:
			self.set_tab_index(current_tab - 1)
		else:
			self.set_tab_index(tab_count)

	def get_tab_index(self):
		return cmds.tabLayout(self.pgs_tabLayout, query = True, selectTabIndex = True)

	def set_tab_index(self, index):
		cmds.tabLayout(self.pgs_tabLayout, edit = True, selectTabIndex = index)

	def get_tab_count(self):
		return len(cmds.tabLayout(self.pgs_tabLayout, query = True, childArray = True))

	def loadConfigsFromJson(self, *args):
		try:
			with open(self.jsonConfigLocation, 'r') as jsonFile:
				jsonConfig = json.load(jsonFile)

			self.validateConfigs(jsonConfig)
		except Exception as e:
			cmds.warning(e)
			cmds.warning("Creating Default Configs")
			self.resetConfigsToDefaults()
		
	def validateConfigs(self, jsonConfig, *args):

		self.configs = jsonConfig

		# validate colors
		if 'colors' not in self.configs:
			self.configs['colors'] = {"default color" : (0.26666666666666666, 0.26666666666666666, 0.26666666666666666),
				  	  				 "incomplete color" : (0.36666666666666666, 0.26666666666666666, 0.26666666666666666),
				  	 				 "complete color" : (0.26666666666666666, 0.36666666666666666, 0.26666666666666666),
				  					 "dim" : (0.26666666666666666, 0.26666666666666666, 0.26666666666666666)}

		if 'default color' not in self.configs['colors']:
			self.configs['colors']['default color'] = (0.26666666666666666, 0.26666666666666666, 0.26666666666666666)

		if 'incomplete color' not in self.configs['colors']:
			self.configs['colors']['incomplete color'] = (0.36666666666666666, 0.26666666666666666, 0.26666666666666666)

		if 'complete color' not in self.configs['colors']:
			self.configs['colors']['complete color'] = (0.26666666666666666, 0.36666666666666666, 0.26666666666666666)

		if 'dim' not in self.configs['colors']:
			self.configs['colors']['default color'] = (0.26666666666666666, 0.26666666666666666, 0.26666666666666666)

		if 'icon names' not in self.configs:
			self.configs['icon names'] = {"history_icon" : "history_75.png"}

		if 'icons' not in self.configs:
			self.configs['icons'] = {'history_icon' : os.path.join(self.directories['icon_dir'], self.configs['icon names']['history_icon'])}

		if 'manage states' not in self.configs:
			self.configs['manage states'] = {'copy html' : True,
											'reset on copy' : True,
											'reset title on copy' : True,
											'title is required' : True,
											'collapse gut check' : True}

		if 'copy html' not in self.configs['manage states']:
			self.configs['manage states']['copy html'] = True

		if 'reset on copy' not in self.configs['manage states']:
			self.configs['manage states']['reset on copy'] = True

		if 'reset title on copy' not in self.configs['manage states']:
			self.configs['manage states']['reset title on copy'] = True

		if 'title is required' not in self.configs['manage states']:
			self.configs['manage states']['title is required'] = True

		if 'collapse gut check' not in self.configs['manage states']:
			self.configs['manage states']['collapse gut check'] = True

	def saveConfigToJson(self, *args):
		jsonConfig = json.dumps(self.configs, indent = 4)

		with open(self.jsonConfigLocation, 'w') as jsonFile:
			jsonFile.write(jsonConfig)

		# print('saved to json')

	def resetConfigsToDefaults(self, *args):
		print('reset all configs')

		self.configs = {}

		self.configs['colors'] = {"default color" : (0.26666666666666666, 0.26666666666666666, 0.26666666666666666),
			  	  				 "incomplete color" : (0.36666666666666666, 0.26666666666666666, 0.26666666666666666),
			  	 				 "complete color" : (0.26666666666666666, 0.36666666666666666, 0.26666666666666666),
			  					 "dim" : (0.26666666666666666, 0.26666666666666666, 0.26666666666666666)}

		self.configs['icon names'] = {"history_icon" : "history_75.png"}

		self.configs['manage states'] = {'copy html' : True,
										'reset on copy' : True,
										'reset title on copy' : True,
										'title is required' : True,
										'collapse gut check' : True}

		self.saveConfigToJson()

		try:
			# Update UI to reflect defaults
			cmds.button('copyFeedbackButton', edit = True, label = "Copy HTML Text", command =  lambda x: self.finished_grading(True))

			self.setMenuItemBox('ResetTitleOnCopy', True)
			self.setMenuItemBox('ResetOnCopy', True)
			self.setMenuItemBox('TitleisRequired', True)
			self.setMenuItemBox('CollapseGutCheck', True)
		except Exception as e:
			print(e)

	def setMenuItemBox(self, checkBoxTitle, checkBoxValue, *args):
		cmds.menuItem(checkBoxTitle, edit = True, checkBox = checkBoxValue)

	def do_nothing(*args):
		pass

	def toggleCopy(self, *args):

		if self.configs['manage states']['copy html']:
			self.configs['manage states']['copy html'] = False
			cmds.button('copyFeedbackButton', edit = True, label = "Copy Plain Text", command = lambda x: self.finished_grading(False))
		else:
			self.configs['manage states']['copy html'] = True
			cmds.button('copyFeedbackButton', edit = True, label = "Copy HTML Text", command =  lambda x: self.finished_grading(True))

		self.saveConfigToJson()

	def toggleResetOnCopy(self, *args):

		if self.configs['manage states']['reset on copy']:
			self.configs['manage states']['reset on copy'] = False
		else:
			self.configs['manage states']['reset on copy'] = True

		self.saveConfigToJson()

	def toggleResetTitleOnCopy(self, *args):

		if self.configs['manage states']['reset title on copy']:
			self.configs['manage states']['reset title on copy'] = False
		else:
			self.configs['manage states']['reset title on copy'] = True

		self.saveConfigToJson()

	def toggleTitleIsRequired(self, *args):

		if self.configs['manage states']['title is required']:
			self.configs['manage states']['title is required'] = False
		else:
			self.configs['manage states']['title is required'] = True

		self.saveConfigToJson()

	def toggleCollapseGutCheck(self, *args):

		if self.configs['manage states']['collapse gut check']:
			self.configs['manage states']['collapse gut check'] = False
		else:
			self.configs['manage states']['collapse gut check'] = True

		self.saveConfigToJson()

	# def validateXML(self):
	# 	self.log('Validate XML')
	# 	error_list = []
	# 	cat_weights = 0
	# 	eq = self.xml_elementDefaults.find('gradeEquation').text
	# 	self.log('equation: {}'.format(eq))
	# 	cats_to_validate = 0
	# 	for cat in self.xml_elementMainCategories:

	# 		cat_title = cat.get('title')
	# 		if cat_title == None:
	# 			cat_title = cat.find('title').text

	# 		cat_weight = cat.get('weight')
	# 		if cat_weight == None:
	# 			cat_weight = cat.find('weight').text

	# 		if eq.count(cat_title[:3]) != 1:
	# 			self.log('title: {}'.format(cat_title[:3]))
	# 			self.log('count: {}'.format(eq.count(cat_title[:3])))
	# 			error_list.append('{} \nnot present in equation exactly once.'.format(cat_title))

	# 		ignore_validation = cat.find('ignore_validation')
	# 		if ignore_validation != None:
	# 			if ignore_validation.text.lower() == 'true':
	# 				ignore_validation = True
	# 		else:
	# 			ignore_validation = False

			
	# 		if not ignore_validation:
	# 			cat_weights += float(cat_weight)
	# 			cats_to_validate += 1
	# 		else:
	# 			cmds.warning('Category: {} ignored in validation.'.format(cat_title))

	# 		subcat_weights = 0
	# 		subs_to_validate = 0
	# 		for subcat in cat.findall('subcategory'):

	# 			sub_title = subcat.get('title')
	# 			if sub_title == None:
	# 				sub_title = subcat.find('title').text

	# 			sub_weight = subcat.get('weight')
	# 			if sub_weight == None:
	# 				sub_weight = subcat.find('weight').text


	# 			ignore_validation = subcat.find('ignore_validation')
	# 			if ignore_validation != None:
	# 				if ignore_validation.text.lower() == 'true':
	# 					ignore_validation = True
	# 			else:
	# 				ignore_validation = False

	# 			if not ignore_validation:
	# 				subcat_weights += float(sub_weight)
	# 				subs_to_validate += 1
	# 			else:
	# 				cmds.warning('Subcategory: {} ignored in validation.'.format(sub_title))
					
	# 		self.log('total subcat weighting: {}'.format(subcat_weights))

	# 		if (subcat_weights != 100) and (subs_to_validate != 0):
	# 			error_list.append('{} \nsubweights incorrect. Total weights: {}'.format(cat_title, subcat_weights))
	# 			cmds.warning('Subcategory weighting incorrect!\n{} total subcategory weighting: {}'.format(
	# 				cat_title, subcat_weights))
	# 			error_list.append('\n')

	# 	for box in self.xml_elementRoot.findall('grade_box'):
	# 		self.log('box: {}'.format(box.get('title')))
	# 		if box.get('title') == 'Late':
	# 			if eq.count(box.get('title')) != 1:
	# 				error_list.append('{} Grade Box\nnot present in equation exactly once'.format(box.get('title')))
	# 		elif eq.count(box.get('title')[:3]) != 1:
	# 			error_list.append('{} Grade Box\nnot present in equation exactly once'.format(box.get('title')))

	# 	self.log('total cat weighting: {}'.format(cat_weights))
	# 	if (cat_weights != 100) and (cats_to_validate != 0): 
	# 		error_list.append('\nCategory weights incorrect. Total weights: {}'.format(cat_weights))
	# 		cmds.warning('Category Weighting Incorrect!\nTotal category weight: {}'.format(cat_weights))

	# 	if len(error_list) >= 1:
	# 		self.log('len(error_list): {}'.format(len(error_list)))
	# 		self.log('error_list: {}'.format(error_list))
	# 		msg = ''
	# 		for i in error_list:
	# 			msg += '{}\n'.format(i)

	# 		prelist = ['Oh Snap!', 'Stop the ship!', 'Well butter my biscuits!',
	# 					'I better fix that!', 'Oopsie daisy!', "Yup, that's about right"]
	# 		button_list = random.sample(prelist, 2)
	# 		button_list.append('Continue Anyway')
	# 		random.shuffle(button_list)
	# 		dialog = cmds.confirmDialog( 
	# 				title="PGS XML Validation Error", 
	# 				message = msg , 
	# 				button =button_list, 
	# 				defaultButton = 'Oh Snap!', 
	# 				cancelButton = 'Stop the ship!',
	# 				dismissString = 'Stop the ship!')
	# 		if dialog != 'Continue Anyway':
	# 			cmds.error('\nPGS XML Validation Error!\n{}'.format(msg))

	# def enable(self):
	# 	for cat in self.mainCategories:
	# 		cat.enable()

	def toolIsComplete(self):
		self.incomplete_cats = []

		if self.configs['manage states']['title is required'] and not self.titleIsComplete():
			self.incomplete_cats.append(("Student Name", ["Please enter the student's name."]))
		for cat in self.mainCategories:
			inc_cats = cat.are_you_complete()
			if inc_cats != []:
				self.incomplete_cats.append((cat.title, inc_cats))
		return self.incomplete_cats

	def wordwrap(self, inputText, wrapWidth = 50):
		return textwrap.wrap(inputText, wrapWidth)

	def validate_filename_func(self, directoryDict):
		# print('\n\n{}\n\n'.format(directoryDict))
		if os.path.isfile(directoryDict['textDirectory'] + directoryDict['filename'] + '.txt') or \
		   os.path.isfile(directoryDict['pickleDirectory'] + directoryDict['filename'] + '.pgs'):
			# print('\n\nFILE EXISTS!!!\n\n')
			handle_file = cmds.confirmDialog( 
				title='File Exists', 
				message='Overwrite or Iterate file?', 
				button=['Overwrite','Iterate'], 
				defaultButton='Overwrite',  
				dismissString='Iterate' )
			# print('\n\n{}\n\n'.format(handle_file))
			if handle_file == 'Overwrite':
				# print('Overwrite selected')
				if os.path.isfile(directoryDict['textDirectory'] + directoryDict['filename'] + '.txt'):
					os.remove(directoryDict['textDirectory'] + directoryDict['filename'] + '.txt')
					# print('deleted text doc')
				if os.path.isfile(directoryDict['pickleDirectory'] + directoryDict['filename'] + '.pgs'):
					os.remove(directoryDict['pickleDirectory'] + directoryDict['filename'] + '.pgs')
					# print('deleted pgs file')
				return directoryDict['filename']
			if handle_file == 'Iterate':
				# print('Iterate Selected')
				# print('textDict: {}\nfilename: {}'.format(directoryDict['textDirectory'] , directoryDict['filename']))
				if os.path.isfile(directoryDict['textDirectory'] + directoryDict['filename'] + '.txt') or \
				   os.path.isfile(directoryDict['pickleDirectory'] + directoryDict['filename'] + '.pgs'):
					the_file = directoryDict['filename']
					iter = 1
					# print('os.path.isfile: {}'.format((directoryDict['textDirectory'] + the_file + '.txt')))
					while os.path.isfile(directoryDict['textDirectory'] + the_file + '.txt') or \
					   os.path.isfile(directoryDict['pickleDirectory'] + the_file + '.pgs'):
						if iter > 1:
							the_file = the_file.rsplit('_', 1)[0]
						the_file += '_{:02d}'.format(iter)
						# print('the_file: {}'.format(the_file))
						# print('os.path.isfile: {}'.format((directoryDict['textDirectory'] + the_file + '.txt')))
						iter += 1
					return the_file 
		else:
			return directoryDict['filename']

	def finished_grading(self, generate_with_HTML, *args):

		feedback = ""

		feedback = self.generate_feedback(generate_with_HTML)

		self.copy_feedback(feedback)

		# title = self.get_title_field()

		# self.manage_history_queue(title, feedback)

		if self.configs['manage states']['reset on copy']:
			self.resetCategories()

		# if self.configs['manage states']['reset title on copy']:
		# 	self.resetTitle()

	# def get_title_field(self):
	# 	return cmds.textField('titleField', query = True, text = True).strip()

	def validate_title_field(self):
		pass

	def toggle_validate_title_field(self):
		pass

	def manage_history_queue(self, title, feedback, *args):
		self.history_queue_items.insert(0, [title, feedback])
		self.history_queue_items.pop()

		self.update_history_queue_menuItems()

	def update_history_queue_menuItems(self, *args):
		for index, menuItem in enumerate(self.history_queue_menuItems):
			cmds.menuItem(menuItem, edit = True, label = self.history_queue_items[index][0], command = lambda x, i = index : self.copy_feedback(self.history_queue_items[i][1]))

	def copy_feedback(self, feedback):
		pyperclip.copy(feedback)
		cmds.warning("Text copied successfully.")

	# generate feedback without any grade/math stuff - just custom comments no defaults
	def generate_feedback(self, generate_with_HTML, *args):

		gathered_grades = self.gatherGrades()
		# title = cmds.textField('titleField', query = True, text = True).strip()

		grades_list = []
		# if generate_with_HTML: # There has to be a better way...?
		# 	# grades_list = ["<h2>{}: <i>{}%</i></h2>".format(os.path.basename(self.xmlFile).split('.')[0], self.categoryGrades.gradeTotal())]
		# 	if title != "":
		# 		grades_list.extend(["Grading for: <b>{}</b>".format(title)])
		# 	# grades_list.extend(["<hr>\n"])
		# else:
		# 	# grades_list = ["{}: {}%".format(os.path.basename(self.xmlFile).split('.')[0], self.categoryGrades.gradeTotal())]
		# 	if title != "":
		# 		grades_list.extend(["Grading for: {}".format(title)])
		# 	grades_list.extend(["\n"])

		for section in gathered_grades:

			# section[0] is the category title
			# section[1] is highnotes
			# section[2] is a list of the subcategories

			# grades_list.extend(["section 0: {}".format(section[0])])
			# grades_list.extend(["section 2: {}".format(section[1])])
			# grades_list.extend(["section 4: {}".format(section[2])])

			# category title
			if generate_with_HTML:
				grades_list.extend(["<h2>{}</h2>".format(section[0])])
				# grades_list.extend(["<i>Instructor Grading Comments</i>"])
				grades_list.extend(["<hr>"])
			else:
				grades_list.extend(["{}".format(section[0])])

			# highnotes / category comments
			if section[1].strip() != "":
				# highnote comments
				grades_list.extend(["{}".format(section[1])])

			# subcategory sections
			for subcat in section[2]:
				if subcat["comment_text"].strip() != "":
					# title and grade value
					if generate_with_HTML:
						grades_list.extend(["<h3>{}:</h3>".format(subcat["section_title"])])
					else:
						grades_list.extend(["{}:".format(subcat["section_title"])])
					
					# add comments
					grades_list.extend(subcat["comment_text"].split("\n"))
					grades_list.extend([""])

		return "\n".join(grades_list)


	# obsolete as of P3
	def generate_feedback_P2(self, generate_with_HTML, *args):

		gathered_grades = self.gatherGrades()
		title = cmds.textField('titleField', query = True, text = True).strip()


		if generate_with_HTML: # There has to be a better way...?
			grades_list = ["<h2>{}: <i>{}%</i></h2>".format(os.path.basename(self.xmlFile).split('.')[0], self.categoryGrades.gradeTotal())]
			if title != "":
				grades_list.extend(["<b>{}</b>".format(title)])
			grades_list.extend(["<hr>\n"])
		else:
			grades_list = ["{}: {}%".format(os.path.basename(self.xmlFile).split('.')[0], self.categoryGrades.gradeTotal())]
			if title != "":
				grades_list.extend(["{}".format(title)])
			grades_list.extend(["\n"])

		for section in gathered_grades:

			# section[0] is the category title
			# section[1] is the category weight
			# section[2] is highnotes
			# section[3] is the category score
			# section[4] is a list of the subcategories

			# grades_list.extend(["section 0: {}".format(section[0])])
			# grades_list.extend(["section 1: {}".format(section[1])])
			# grades_list.extend(["section 2: {}".format(section[2])])
			# grades_list.extend(["section 3: {}".format(section[3])])
			# grades_list.extend(["section 4: {}".format(section[4])])

			if section[0] == "grade_boxes_internal":
				for grade_box in section[4]:
					if generate_with_HTML:
						grades_list.extend(["{} <i>{}</i>".format(grade_box['default_comments_text'], grade_box['grade_value'])])
					else:
						grades_list.extend(["{} {}".format(grade_box['default_comments_text'], grade_box['grade_value'])])
			else:
				# category title and score
				if generate_with_HTML:
					grades_list.extend(["<h2>{} <i>{}%</i></h2>".format(section[0], int(section[3]))]) # added int to drop decimal
				else:
					grades_list.extend(["{} {}%".format(section[0], int(section[3]))])

				# highnotes
				if section[2].strip() != "":

					# highnote intro
					try:
						category_comment_text_intro = self.xml_elementDefaults.find('category_comments_intro').text
						if category_comment_text_intro != None: 
							grades_list.extend([x.strip() for x in category_comment_text_intro.split("\n")])
					except AttributeError:
						pass

					# highnote comments
					grades_list.extend(["{}".format(section[2])])

				# subcategory sections
				for subcat in section[4]:
					# title and grade value
					if generate_with_HTML:
						grades_list.extend(["<b>{}:</b> <i>{}%</i>".format(subcat["section_title"], int(subcat["grade_value"]))]) # added int to drop decimal
					else:
						grades_list.extend(["{}: {}%".format(subcat["section_title"], int(subcat["grade_value"]))]) # added int to drop decimal

					# default comments
					if subcat["default_comments_text"].strip() != "":

						# highnote intro
						try:
							default_textIntro = self.xml_elementDefaults.find('default_comment_intro').text
							if default_textIntro != None: 
								grades_list.extend([x.strip() for x in default_textIntro.split("\n")])
						except AttributeError:
							pass

						# add default comments
						grades_list.extend([x.strip() for x in subcat["default_comments_text"].split("\n")])

					# comments
					if subcat["comment_text"].strip() != "":

						# comment intro
						try:
							comment_textIntro = self.xml_elementDefaults.find('comment_intro').text
							if comment_textIntro != None: 
								grades_list.extend([x.strip() for x in comment_textIntro.split("\n")])
						except AttributeError:
							pass

						# add comments
						grades_list.extend(subcat["comment_text"].split("\n"))

					grades_list.extend([""])

			if generate_with_HTML:
				grades_list.extend(["<hr>"])
			else:
				grades_list.extend(["\n"])

		if generate_with_HTML:
			grades_list.extend(["<h2>{}: <i>{}%</i></h2>".format(os.path.basename(self.xmlFile).split('.')[0], self.categoryGrades.gradeTotal())])
		else: 
			grades_list.extend(["{}: {}%".format(os.path.basename(self.xmlFile).split('.')[0], self.categoryGrades.gradeTotal())])

		return "\n".join(grades_list)
		
	def gatherGrades(self):
		gradesForPickle = []
		for cat in self.mainCategories:
			gradesForPickle.append(cat.what_is_the_grade())
		for index in gradesForPickle:
			self.log('Grades from cat {} : {}'.format(index[0], index))
			self.log('\n\n{}\n\n'.format(index))
		return gradesForPickle

	def resetTitle(self, *args):
		cmds.textField('titleField', edit = True, text = '')

	def titleIsComplete(self, *args):
		if self.getTitle() == "":
			print("title: {}".format(self.getTitle()))
			return False
		else:
			return True

	def getTitle(self):
		return cmds.textField('titleField', query = True, text = True)

	def setTitle(self, text, *args):
		print(r"Title: {}".format(text))
		cmds.textField('titleField', edit = True, text = text)

	def trimTitle(self, *args):
		self.setTitle(os.path.basename(self.getTitle()))

	def pasteTitle(self, *args):
		self.setTitle(pyperclip.paste())

	def resetTool(self, *args):
		self.resetTitle()
		self.resetCategories()

	def resetCategories(self, *args):
		self.log('reset PGS grade tool')
		for cat in self.mainCategories:
			cat.reset()

	def update(self):
		for cat in self.mainCategories:
			cat.update()

	def log(self, message, prefix = '.:P3 Grading System::'):
		"""
		print stuff yo!
		"""
		if self.development:
			print("%s: %s" % (prefix, message))


