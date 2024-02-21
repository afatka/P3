#! /usr/bin/env python
#install Pabuito

import maya.cmds as cmds
import maya.mel as mel
import os
def install():

	#ask the user to install pabuito2 on the active shelf or a new shelf
	install_type = cmds.confirmDialog( 
		title='Install P3', 
		message='Install to new shelf or active shelf?', 
		button=['New','Active'], 
		defaultButton='New', 
		cancelButton='New', 
		dismissString='New' )

	icon_dir = os.path.join(os.path.dirname(__file__), 'icons')
	parent_shelfTabLayout = mel.eval("global string $gShelfTopLevel; $temp = $gShelfTopLevel;") 
	shelves = cmds.tabLayout(parent_shelfTabLayout, query = True, childArray = True)
	if install_type == 'Active':
		for shelf in shelves:
		    if cmds.shelfLayout(shelf, query = True, visible = True):
		        install_shelf = shelf
	if install_type == 'New':
		install_shelf = 'P3'
		i = 1 
		while True:
			if install_shelf not in shelves:
				break
			else: 
				install_shelf = 'P3' + str(i)
				i += 1
		cmds.shelfLayout(install_shelf, parent = parent_shelfTabLayout)

	#Pabuito2 shelf maker button
	cmds.shelfButton(parent = install_shelf,
		annotation = 'P3 Shelf Maker', 
		image1 = os.path.join(icon_dir, 'P3sm.png'),
		command = """
#P3 shelf maker
from P3 import P3ShelfMaker as P3sm
import importlib
importlib.reload(P3sm)

with P3sm.P3ShelfMaker() as P3sm:
	print('P3SM Running')
		""",
		sourceType = 'python', 
		label = 'P3SM'
		)


	shelfDirectory = cmds.internalVar(userShelfDir = True) + 'shelf_' + install_shelf
	cmds.saveShelf(install_shelf, shelfDirectory)

	cmds.confirmDialog( 
		title='Install Complete', 
		message='P3 Install Complete!', 
		button=['Awesome'] )

	#this is a fix for a Maya issue 'provided' from Gary Fixler > in the comments MAR 2012
	# http://www.nkoubi.com/blog/tutorial/how-to-create-a-dynamic-shelf-plugin-for-maya/
	
	topLevelShelf = mel.eval("global string $gShelfTopLevel; $temp = $gShelfTopLevel;") 
	shelves = cmds.shelfTabLayout(topLevelShelf, query=True, tabLabelIndex=True)
	for index, shelf in enumerate(shelves):
		cmds.optionVar(stringValue=('shelfName%d' % (index+1), str(shelf)))


install()
		