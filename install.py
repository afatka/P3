#! /usr/bin/env python
#install Pabuito

import maya.cmds as cmds
import maya.mel as mel
import os
def install():

	#ask the user to install pabuito2 on the active shelf or a new shelf
	install_type = cmds.confirmDialog( 
		title='Install P2', 
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
		install_shelf = 'P2'
		i = 1 
		while True:
			if install_shelf not in shelves:
				break
			else: 
				install_shelf = 'P2' + str(i)
				i += 1
		cmds.shelfLayout(install_shelf, parent = parent_shelfTabLayout)

	#Pabuito2 shelf maker button
	cmds.shelfButton(parent = install_shelf,
		annotation = 'P2 Shelf Maker', 
		image1 = os.path.join(icon_dir, 'p2sm.png'),
		command = """
#P2 shelf maker
from P2 import P2ShelfMaker as p2sm
import importlib
importlib.reload(p2sm)

with p2sm.P2ShelfMaker() as p2sm:
	print('P2SM Running')
		""",
		sourceType = 'python', 
		label = 'P2SM'
		)

	#Pabuito2 Pickle Loader Button
# 	cmds.shelfButton(parent = install_shelf,
# 		annotation = 'Pabuito2 Pickle Loader', 
# 		image1 = os.path.join(icon_dir, 'ppl.png'),
# 		command = """
# #Pabuito2 Pickle Loader
# import maya.cmds as cmds
# PGSFile = cmds.fileDialog2(caption = 'Please select project file', fileMode = 1, fileFilter = "PGS (*.pgs)")[0]

# from pabuito2 import pabuitoGradingSystem_HTML as pgs
# pgsGUI = pgs.pabuitoGradingSystem_HTML(PGSFile)
# 		""",
# 		sourceType = 'python',
# 		label = 'PPL'
# 		)


	shelfDirectory = cmds.internalVar(userShelfDir = True) + 'shelf_' + install_shelf
	cmds.saveShelf(install_shelf, shelfDirectory)

	cmds.confirmDialog( 
		title='Install Complete', 
		message='P2 Install Complete!', 
		button=['Awesome'] )

	#this is a fix for a Maya issue 'provided' from Gary Fixler > in the comments MAR 2012
	# http://www.nkoubi.com/blog/tutorial/how-to-create-a-dynamic-shelf-plugin-for-maya/
	
	topLevelShelf = mel.eval("global string $gShelfTopLevel; $temp = $gShelfTopLevel;") 
	shelves = cmds.shelfTabLayout(topLevelShelf, query=True, tabLabelIndex=True)
	for index, shelf in enumerate(shelves):
		cmds.optionVar(stringValue=('shelfName%d' % (index+1), str(shelf)))


install()
		