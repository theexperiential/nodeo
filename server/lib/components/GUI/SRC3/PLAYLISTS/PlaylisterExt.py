"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

class PlaylisterExt:
	"""
	Switch between, create, rename, edit, clear and destroy playlists.
	"""
	def __init__(self, ownerComp):
		self.myOp = ownerComp
		self.media = parent.gui.op('SRC3/MEDIA')
		self.activeMedia = self.media.op('active')

		self.Playlists = op('Playlists')
		self.playlist = op('in')
		self.merged = op('merged')
		self.playlister = op('PLAYLISTER1')
		self.config = op('listerConfig/colDefine')
		self.active = op('active')
		self.playlistWrite = op('fileout1')
		self.playlistFolder = op('folder_playlists')

		self.tabs = self.myOp.op('TOPBAR/TABS')
		self.selectedTab = self.tabs.par.Value0
		self.editing = self.tabs.op('folderTabs/tab' + str(int(self.selectedTab)) + '/editing')
		
		self.Renamer = self.myOp.op('RENAMER')
		self.Deleter = self.myOp.op('DELETER')
		self.Resetter = self.myOp.op('RESETTER')

		self.instructions = self.myOp.op('bg/instructions')
		self.divs = self.myOp.findChildren(name='div*')

		# sorting
		self.typesToSort = ['Vidsort', 'Transsort', 'Sndsort']
		self.sortBys = ['Alphabetical', 'Shuffle', 'Manual']

		self.Vidsort = self.myOp.op('Vidsort')
		self.Transsort = self.myOp.op('Transsort')
		self.Sndsort = self.myOp.op('Sndsort')

		self.Vidbackup = self.myOp.op('Vidsort_backup')
		self.Transbackup = self.myOp.op('Transsort_backup')
		self.Sndbackup = self.myOp.op('Sndsort_backup')

		self.Vidswitch = self.myOp.op('Vidsort_switch')
		self.Transwitch = self.myOp.op('Transsort_switch')
		self.Sndswitch = self.myOp.op('Sndsort_switch')

		# trans src table
		self.trans = op.Engineer.op('Trans/out1')

	def selectEndTab(self):
		self.tabs.par.Value0 = self.Playlists.numRows - 2

	def CheckIfPlaylistFileExists(self, playlistName):
		playlistName += '.py'
		for row in range(1, self.playlistFolder.numRows):
			if playlistName == str(self.playlistFolder[row, 'name']):
				return True

	def UpdatePlaylists(self):
		playlistNames = ''
		playlistLabels = ''
		for row in range(1, self.Playlists.numRows):
			playlistName = self.Playlists[row, 'name']
			playlistNames += playlistName + ' '
			playlistLabel = self.Playlists[row, 'label']
			playlistLabels += "'" + playlistLabel + "' "

		self.tabs.par.Menunames = playlistNames
		self.tabs.par.Menulabels = playlistLabels

	def NewPlaylist(self):
		playlistNum = tdu.digits(self.Playlists[self.Playlists.numRows-1,'name']) + 1

		newPlaylistName = 'playlist{}'.format(playlistNum)
		newPlaylistLabel = 'New Playlist {}'.format(playlistNum)
		self.Playlists.appendRow( \
			[newPlaylistName, newPlaylistLabel, 'False', self.myOp.par.Vidsort, \
			self.myOp.par.Transsort, self.myOp.par.Sndsort, tdu.rand(absTime.frame)])

		self.selectEndTab()

	def FinishRenamingPlaylist(self, enteredText):
		self.Playlists[int(self.selectedTab) + 1, 'label'] = enteredText
		self.SelectPlaylistTab(10, 5, 'rename', self.Playlists[self.myOp.par.Selectedplaylist, 'name'])

	def StartRenamingPlaylist(self):
		self.Renamer.par.Textentrydefault = self.Playlists[int(self.selectedTab) + 1, 'label']
		self.Renamer.par.Open.pulse()

	def FinishDeletingPlaylist(self):
		if self.Playlists.numRows > 2:
			self.Playlists.deleteRow(str(self.selectedTab))

		self.selectEndTab()

		# change active playlist to last playlist if active playlist no longer exists
		if self.Playlists.numRows - 2 < self.myOp.par.Activeplaylist:
			self.myOp.par.Activeplaylist = self.Playlists.numRows - 2

	
	def StartDeletingPlaylist(self):
		if self.Playlists.numRows == 2:
			self.Deleter.par.Text = 'You must have at least one playlist.'
		else:
			self.Deleter.par.Text = 'Playlist will be deleted! Continue?'

		self.Deleter.par.Open.pulse()


	def FinishResettingPlaylist(self):
		self.playlist.setSize(1, 9)
		self.playlist.replaceRow(0, \
			['VidName', 'VidDur', 'TransName', 'TransDur', 'SndName', 'SndDur', 'Delete', 'VidPath', 'TransPath', 'SndPath'])

	def StartResettingPlaylist(self):
		self.Resetter.par.Open.pulse()

	def insertNewRow(self, mediaType, srcDat, indices, dropPos):
		# if snd or trans dropped into null space (below rows), ignore them
		if mediaType == 'Snd' and dropPos == -1:
			pass
		elif mediaType == 'Trans' and dropPos == -1:
			pass
		else:
			# if dropped into null space (below rows), append to end instead of replacing nothing
			if dropPos == -1:
				dropPos = self.playlist.numRows - 1

			# trans default is xDissolve
			transDur = 1.0
			transName = 'XD'
			transPath = 'XD'

			# if trans mode is shuffle, randomly add transition 

			# snd defaults
			sndDur = 100.0
			sndName = 'sndName'
			sndPath = 'sndPath'

			if dropPos == self.playlist.numRows:
				dropPos -= 1

			indices = sorted(indices, reverse=True)
			for i in indices:
				vidName = op(srcDat)[i, 'Name']
				vidPath = op(srcDat)[i, 'Path']
				vidDur = op(srcDat)[i, 'Duration']
				# if no vid dur is assigned, set it to the current segment interval
				if not vidDur:
					vidDur = op.Engineer.par.Segmentinterval

				self.playlist.appendRow( \
					[vidName, vidDur, transName, transDur, sndName, sndDur, 'x', \
					 vidPath, transPath, sndPath], dropPos)

	def replaceCellsInRow(self, mediaType, srcDat, indices, dropPos):
		for i in indices:
			dropPos += 1
			self.playlist[dropPos, '{}Name'.format(mediaType)] = op(srcDat)[i, 'Name']
			self.playlist[dropPos, '{}Path'.format(mediaType)] = op(srcDat)[i, 'Path']
			self.playlist[dropPos, '{}Dur'.format(mediaType)] = op(srcDat)[i, 'Duration']

	def PreDrop(self):
		if self.myOp.par.Dropinsertorreplace:
			self.playlister.par.Drophighlight = 3 # row
		else:
			self.playlister.par.Drophighlight = 1 # above row

	def Drop(self, srcLister, dropPos):
		# table to reference from
		srcDat = self.activeMedia

		# need to redo this for when search is active; rows get messed up. maybe search by row name via dat?
		#===================================

		selectedRows = str(op(str(srcLister)).par.Selectedrows)
		indices = sorted([int(i) for i in selectedRows.split()])

		# detect dropped media type
		mediaType = self.media.par.Selectedmediatype

		if mediaType == 'Gen' or mediaType == 'Mov': # gen and mov are both vids
			mediaType = 'Vid'

		if self.myOp.par.Dropinsertorreplace and dropPos != -1: # replace
			self.replaceCellsInRow(mediaType, srcDat, indices, dropPos)
		else: # insert
			self.insertNewRow(mediaType, srcDat, indices, dropPos)

		# save changes
		self.WritePlaylist(5)

	def DeleteRow(self, row):
		self.playlist.deleteRows(row)

	def SelectPlaylistTab(self, readDelay, writeDelay, event, lastTab):
		# do not re-shuffle when switching tabs
		self.myOp.par.Reshuffleonsort = False

		# lock active if selected playlist is different than active playlist
		if self.myOp.par.Selectedplaylist != self.myOp.par.Activeplaylist:
			self.active.lock = True
		else:
			run("op('{}').lock = False".format(self.active), delayFrames=10)

		# switch playlist input table
		self.playlist.par.file = parent.Nodeo.par.Settings + '/playlists/' + self.Playlists[self.myOp.par.Selectedplaylist + 1, 'label'] + '.py'
		# check if playlist file doesn't exist
		if not self.CheckIfPlaylistFileExists(self.Playlists[self.myOp.par.Selectedplaylist + 1, 'label']) and event != 'rename':
			self.FinishResettingPlaylist()

		self.ReadPlaylist(readDelay)
		self.WritePlaylist(writeDelay)

		self.checkIfPlaylistIsLocked()

		# load playlist sort button states
		for typeToSort in self.typesToSort:
			setattr(self.myOp.par, typeToSort, self.Playlists[self.myOp.par.Selectedplaylist + 1, typeToSort])
	
	def ReadPlaylist(self, delay):			
		run("op('{}').par.loadonstartpulse.pulse()".format(self.playlist), delayFrames=delay)

	def WritePlaylist(self, delay):
		run("op('{}').par.write.pulse()".format(self.playlistWrite), delayFrames=delay)

	def checkIfPlaylistIsLocked(self):
		if self.Playlists[self.myOp.par.Selectedplaylist + 1, 'locked'] == True:
			self.playlister.par.Dragtoreorderrows = False
			self.myOp.par.Selectedplaylistlocked = True
		else:
			self.playlister.par.Dragtoreorderrows = True
			self.myOp.par.Selectedplaylistlocked = False

	def LockPlaylist(self, lock):
		self.Playlists[self.myOp.par.Selectedplaylist + 1, 'locked'] = lock
		self.checkIfPlaylistIsLocked()

	def ActivatePlaylist(self):
		self.myOp.par.Activeplaylist = self.myOp.par.Selectedplaylist

	def Instructions(self):
		if self.playlist.numRows == 1:
			self.instructions.par.display = True
			for operator in self.divs:
				operator.par.display = False
		else:
			self.instructions.par.display = False
			for operator in self.divs:
				operator.par.display = True

	def locker(self, typeToSort, lock):		
		# prep cols in lister that need to be enabled/disabled
		if 'Vid' in typeToSort:
			configCols = [1,2,3,4]
			# self.playlister.par.Selectablerows = 1 - lock
		elif 'Trans' in typeToSort:
			configCols = [5,6,7]
		elif 'Snd' in typeToSort:
			configCols = [8,9,10]

		# lock interaction of those cols
		for col in configCols:
			self.config[10, col] = 1 - lock
			self.config[12, col] = 1 - lock

		#self.myOp.op(typeToSort + '_switch').par.index = lock
		self.myOp.op(typeToSort + '_backup').lock = lock

	def ReShuffle(self):
		print('reshuffled')
		self.Playlists[self.myOp.par.Selectedplaylist + 1, 'Seed'] = tdu.rand(absTime.frame)

	def Sorter(self, typeToSort, sortBy):
		# record selected type to playlist table
		self.Playlists[self.myOp.par.Selectedplaylist + 1, typeToSort] = sortBy

		if sortBy == self.sortBys[0]: # alphabetical
			order = 0
			sortmethod = 1
			self.locker(typeToSort, True)
		elif sortBy == self.sortBys[1]: # shuffle
			order = 3
			sortmethod = 1
			
			if self.myOp.par.Reshuffleonsort:
				self.ReShuffle()
			#self.myOp.op(typeToSort).par.seed = self.Playlists[self.myOp.par.Selectedplaylist + 1, 'Seed']

			self.locker(typeToSort, True)
		elif sortBy == self.sortBys[2]: # manual
			order = 0
			sortmethod = 5 # preserve input order
			self.locker(typeToSort, False)

		self.myOp.op(typeToSort).par.order = order
		self.myOp.op(typeToSort).par.sortmethod = sortmethod

		# reset re-shuffle for next shuffle button press
		self.myOp.par.Reshuffleonsort = True
