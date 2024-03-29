"""
Maya Shelf Button Creator

Created by Adam  Fatka : 2015 : adam.fatka@gmail.com
"""

import maya.cmds as cmds
import maya.mel as mel
import os.path

class P3ShelfMaker(object):

	def __init__(self):
		self.development = True

	def __enter__(self):
		# print('file: {}'.format(__file__))
		# print('dirname: {}'.format(os.path.dirname(__file__)))
		# print('icon path: {}'.format(os.path.join(os.path.dirname(__file__), 'icons', 'P3.png')))
		shelfTabLayout = mel.eval("global string $gShelfTopLevel; $temp = $gShelfTopLevel;") 
		shelves = cmds.tabLayout(shelfTabLayout, query = True, childArray = True)
		for shelf in shelves:
			if cmds.shelfLayout(shelf, query = True, visible = True):
				parentShelf = shelf

		icon_count = 1
		shelfBtns = cmds.shelfLayout(parentShelf, query = True, childArray = True)
		for btn in shelfBtns:
			cmd = cmds.shelfButton(btn, query = True, command = True)
			if 'P3.P3(\'' in cmd:
				icon_count += 1


		xmlFile = cmds.fileDialog2(caption = 'Please select project xml', fileMode = 1, fileFilter = "XML (*.xml)")[0]
		annotation = 'P3 - ' + str(xmlFile.rsplit('/', 1)[-1].rsplit('.',1)[0])
		commandBlock = "import P3.P3 as P3\nimport maya.cmds as cmds\nP3GUI = P3.P3('{}')".format(xmlFile)
		
		print("icon count: {}".format(icon_count))
		icon = os.path.join(os.path.dirname(__file__), 'icons', 'P3_{:02d}.png'.format(icon_count))
		print("Icon: {}".format(icon))
		if not os.path.isfile(icon):
			icon = os.path.join(os.path.dirname(__file__), 'icons', 'P3.png')

		cmds.shelfButton( parent = parentShelf, annotation = annotation, image1 =icon, command = commandBlock, sourceType = 'python' )

		shelfDirectory = cmds.internalVar(userShelfDir = True) + 'shelf_P3'
		cmds.saveShelf(parentShelf, shelfDirectory)

		return self


	def __exit__(self, *args):
		self.log('exit')
		# for arg in args:
		# 	self.log(arg)

	def log(self, message, prefix = 'P3 Shelf Maker - '):
		if self.development:
			print(('{}{}'.format(prefix, message)))




