"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

class MediaExt:
	"""
	MediaExt manages media source types and segments.
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.myOp = ownerComp
		self.mediaLister = self.myOp.op('MEDIALISTER1')
		self.listerConfig = self.myOp.op('listerConfig/colDefine')
		self.search = self.myOp.op('SEARCH')
		self.searchField = self.search.op('stringField0/field')
		self.dragType = self.myOp.op('BTN_DRAGTYPE')

	def swapPreviews(self, tab):
		if tab != 'Snd':
			self.listerConfig['topPath', 'Preview'] = '../../previews/*' # + tab + '/*'
			self.listerConfig['width', 'Preview'] = 74
		else:
			self.listerConfig['topPath', 'Preview'] = '../../../icons/snd/out2'
			self.listerConfig['width', 'Preview'] = 42

	def lockDropReplace(self, lock):
		if lock:
			self.myOp.store('initial_drop_state', bool(self.myOp.par.Dropinsertorreplace))
			self.myOp.par.Dropinsertorreplace = True
			self.myOp.par.Lockdropreplace = True
			self.dragType.par.display = False 
		else:
			initialDropState = self.myOp.fetch('initial_drop_state')
			self.myOp.par.Dropinsertorreplace = initialDropState
			self.myOp.par.Lockdropreplace = False
			self.dragType.par.display = True

	def SwitchMedialisterTab(self, tab):
		# don't conflict switching tabs with current media bin, if a segment was just dragged to an engine
		op.Engineer.SwitchSourceToParse(op('../PLAYLISTS/PLAYLISTER1'))
		# switch input dat to selected tab
		self.mediaLister.par.Inputtabledat = op.Engineer.op(str(tab) + '/out1')


		# snd and trans types can only replace existing segments, not appended/inserted between them
		if tab == 'Snd' or tab == 'Trans':
			self.lockDropReplace(True)
		else:
			self.lockDropReplace(False)

		self.swapPreviews(tab)

	def Search(self, start, filterString):
		if start:
			self.searchField.setKeyboardFocus(selectAll=True)
			self.searchField.op('level_slash').par.opacity = 0

			self.mediaLister.par.Filtercols = 2
			try:
				self.mediaLister.par.Filterstring = filterString
			except:
				pass
			parent.Medialister.par.Searchactive = True
		else:
			self.search.par.Value0 = ''
			self.searchField.op('level_slash').par.opacity = 1
			parent.Medialister.par.Searchactive = False

	def UpdateSegmentLength(self, length):
		return

	def KeepDuration(self, row):
		inDat = self.mediaLister.par.Inputtabledat
		dur = op(inDat).op('../duration')
		print(row)
		dur[row, 0] = 0.0
		parent.gui.par.Refreshmedialister.pulse()