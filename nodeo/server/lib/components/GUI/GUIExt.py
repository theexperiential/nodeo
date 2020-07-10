class GUI:
	"""
	GUI layouts are triggered by pulsing one of the four center square buttons 
	in the middle of the GUI. Each corresponds to it's relevant quadrant.

	1. quad (default/normal)
		left or right click in fullscreen or duo layouts to re-init
	2. fullscreen (mono) of a single quadrant
		left click to init
	3. duos (two quadrants together)
		right click to init
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.myOp = ownerComp
		self.RootComps = self.myOp.findChildren(type=containerCOMP, depth=1)

	def DetermineAnchorsQuad(self, comp, order):
		if comp.digits == order[0] or comp.digits == order[2]: # left side
			left = 0
			right = 0.5
		else:
			left = 0.5
			right = 1

		if comp.digits == order[2] or comp.digits == order[3]: # bottom side
			top = 0.5
			bottom = 0
		else:
			top = 1
			bottom = 0.5

		self.DetermineAnchors(comp, top, right, bottom, left)

		comp.par.display = True

		# reset button state, just in case
		if 'preview' not in str(comp):
			comp.op('buttonToggle_fullscreen').par.Value0 = False

	def DetermineAnchorsDuo(self, selectedComp, duoComps):
		if selectedComp == 1:
			anchors = [[1,1,0.5,0],[0.5,1,0,0]]
		elif selectedComp == 2:
			anchors = [[1,1,0.5,0],[0.5,1,0,0]]
		elif selectedComp == 3:
			anchors = [[0.5,1,0,0],[1,1,0.5,0]]
		else:
			anchors = [[1,1,0,0.5],[1,0.5,0,0]]

		for i in range(0,2):
			duoComps[i][0].par.topanchor = anchors[i][0]
			duoComps[i][0].par.rightanchor = anchors[i][1]
			duoComps[i][0].par.bottomanchor = anchors[i][2]
			duoComps[i][0].par.leftanchor = anchors[i][3]

	def DetermineAnchors(self, comp, top, right, bottom, left):
		comp.par.topanchor = top
		comp.par.rightanchor = right
		comp.par.bottomanchor = bottom
		comp.par.leftanchor = left

	def Layout(self, layout, selectedComp):
		# enable all quadrants
		for comp in self.RootComps:
			comp.par.display = True
			pass

		if layout == 'QUAD':
			for comp in self.RootComps:
				self.DetermineAnchorsQuad(comp, [1,2,3,4])

		elif layout == 'DUO':
			duos = [[1,2,3,4],[2,4,1,3],[3,1,2,4],[4,3,1,2]]

			for comp in self.RootComps:
				if selectedComp == comp.digits:
					duo = duos[comp.digits-1]
					duoComps = []
					# sort duos
					for i in range(0,4):
						row = self.myOp.findChildren(type=containerCOMP, depth=1, name='*{}'.format(duo[i]))
						duoComps.append(row)
					
					duoComps[0][0].par.display = True
					duoComps[1][0].par.display = True
					duoComps[2][0].par.display = False
					duoComps[3][0].par.display = False
				
			self.DetermineAnchorsDuo(selectedComp, duoComps)

		else: # layout == MONO
			for comp in self.RootComps:
				if selectedComp not in str(comp):
					comp.par.display = False # hide unselected quads
					pass
				else:
					self.DetermineAnchors(comp, 1, 1, 0, 0) # fullscreen the selected quad
