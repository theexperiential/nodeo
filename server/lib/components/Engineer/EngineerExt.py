import random

class Engineer:
	"""
	Engineer operates the playback of video, audio and transition (VAT) medias.

	Video is either a tox scene (generative art), a movie/still file, or a stream component.
	Audio is controlled by the AudioPlayer sub component. It is either an audio file or stream.
	Transition is either a tox scene or movie/still file.

	"""
	def __init__(self, ownerComp):
		self.myOp = ownerComp

		self.quadHeading = parent.Nodeo.op('quad_heading')

		# pars
		self.switchType = self.myOp.fetch('segment_unit')
		self.switchInterval = self.myOp.par.Segmentinterval
		self.abba = self.myOp.par.Abba
		self.duet = self.myOp.par.Duet
		self.pip = self.myOp.par.Pip
	
		self.engine4 = parent.Nodeo.op('engine4')

		self.engineMov = self.myOp.op('engine_Mov')

		# timer
		self.params = self.myOp.op('timer/params')
		self.stateSwap = self.myOp.op('timer/state_swap')['cycles']
		self.timer = self.myOp.op('timer/timer_video')
		self.timerSegments = self.myOp.op('timer/timer_video_segments')
		self.duetFractionReset = self.myOp.op('timer/duet_reset_delay')
		self.fractionAnims = self.myOp.op('timer/fraction_anims')
		self.triggerTransGate = self.myOp.op('timer/trigger_trans_gate')

		# playlist
		self.VidParser = self.myOp.op('VidParser')
		self.selectedPlaylist = self.VidParser.op('select1')
		self.playlistTotal = self.selectedPlaylist.numRows - 1

		# generative
		self.Gen = self.myOp.op('Gen')
		self.genDur = self.Gen.op('duration')

		# movie
		self.Mov = self.myOp.op('Mov')
		self.movPreviewLoader = self.Mov.op('preview_loader')
		self.movFolder = self.Mov.op('folder_mov')
		self.movFolderPreviews = self.Mov.op('folder_mov_previews')
		self.movMakePreview = self.Mov.op('trigger1')

		# transitions
		self.Trans = self.myOp.op('Trans')
		self.transitions = self.Trans.op('folder_trans')
		self.selectEngine4 = self.Trans.op('select_engine4')
		self.playlistTrans = self.Trans.op('playlist_trans')

		# comp
		self.trans = self.myOp.op('../comp/glsl_mattes_trans')

		# GUI
		self.gui = parent.Nodeo.op('GUI')
		self.deck = self.gui.op('PAR4/VIDEO_BAR/ABBA')
		self.duip = self.gui.op('PAR4/VIDEO_BAR/DUIP')

		self.media = self.gui.op('SRC3/MEDIA')
		self.mediaLister = self.media.op('MEDIALISTER1')
		self.mediaActive = self.media.op('active')
		
		self.playlists = self.gui.op('SRC3/PLAYLISTS')
		self.playLister = self.playlists.op('PLAYLISTER1')
		self.playlistActive = self.playlists.op('active')

	def clamp(self, num, minValue, maxValue):
   		return max(min(num, maxValue), minValue)

	def GetRandInt(self, minInt, maxInt):
		randomInt = random.randint(minInt,maxInt)
		return randomInt

	def ToBOrNotToB(self, val):
		if val % 2:
			return False
		else:
			return True

	def calcPlaylistTotal(self):
		total = self.selectedPlaylist.numRows - 1
		return total

	def ResetPlayback(self):
		# re-init storage
		self.myOp.op('storage_init').run()

		# blackout output
		parent.Nodeo.par.Output = False

		# reset for init playback
		self.timer.par.initialize.pulse()
		self.myOp.par.Abba = False # a = 1, b = 2
		self.myOp.par.Duet = False

		self.CueNextScene(2, 2) # b
		self.CueNextScene(1, 1) # a, current index

	def FirstPlay(self):
		self.ResetPlayback()

		#start timer
		self.timer.par.start.pulse()
		
		# enable output if disabled
		parent.Nodeo.par.Output = True

		parent.Nodeo.store('armed_for_playback', False)

	def matchFractionIndex(self, val):
		# this fixes the pairing so that the correct
		# glsl channel is rendered
		if val:
			correctVal = val # for A (engine 1)
		else:
			correctVal = 1 - val # for B (engine 2)
		self.params.par.value11 = correctVal # index abba

	def SwitchAbba(self, val):
		self.matchFractionIndex(val)

		self.duetFractionReset.run(val) # update duet fractions if necessary

		engineNumber = val + 1
		self.myOp.store('current_engine_number', engineNumber)
		self.myOp.store('current_index', getattr(self.myOp.par, 'Enginenowindex{}'.format(engineNumber))) # update current (playing) index			
			
		#self.toggleDuetPair()

	def duetFraction(self, i, chance):
		rand = random.random()

		if i == 6 or i == 7: # horizontal/vertical
			rand = 0.5

		elif i == 8: # square
			if chance < 3:
				rand = self.clamp(rand, 0.15, 0.19)
			else:
				rand = 0.175

		elif i == 9: # circle
			if chance < 7:
				rand = self.clamp(rand, 0.15, 0.18)
			else:
				offset = random.random()
				offset = self.clamp(offset, 0.02, 0.06)
				threeChances = random.randint(0,9)
				rand = 0.1
				if threeChances < 7 and threeChances > 3:
					pass
				elif threeChances < 3 :
					rand += offset
				else:
					rand -= offset

		return rand
	
	def duetSpeed(self, index, speed):
		self.fractionAnims.op('speed_limit' + str(index)).par.value0 = (speed * 0.005)
		self.fractionAnims.op('speed' + str(index)).par.resetpulse.pulse()

	def duetShapeIndex(self):
		index = self.GetRandInt(0,3)
		while index == self.myOp.fetch('duet_shape_index'):
			index = self.GetRandInt(0,3)

		self.myOp.store('duet_shape_index', index)

		return index

	def toggleDuetPair(self, val):
		self.myOp.store('pair', val) # toggle pair

	def DuetSwitchAbba(self):
		# if a instead of b is now on display, switch abba automatically
		fractions = ['x', 'y', 'z', 'w']
		currentFraction = self.params['index_duet_shape']
		currentFractionVal = self.params['fraction_' + fractions[int(currentFraction)]]
		
		if self.myOp.par.Abba: # on B, so fraction must = index abba
			pass
		else: # on A, so fraction = 1 - index abba (opposite)
			self.myOp.par.Abba = 1 - self.myOp.par.Abba

	def Duet(self, duo, pair, index, chance, parMatteIndex):
		self.myOp.par.Pairanimsec = self.myOp.fetch('pair_anim_sec')
		if duo: # turn on duet
			fraction = self.duetFraction(parMatteIndex, chance)
			setattr(self.params.par, 'value{}'.format(parMatteIndex), fraction) # set fraction
			
			if chance > 8:
				self.myOp.store('duet_speed', True)
				self.duetSpeed(index, 1)
			
		else: # turn off duet
			index = int(self.myOp.par.Index1) # may need to update this?
			parMatteIndex = int(self.myOp.fetch('duet_shape_index') + 6) # fetch current matte index
			setattr(self.params.par, 'value{}'.format(parMatteIndex), pair) # reset fraction
			
			self.myOp.store('duet_speed', False)
			self.duetSpeed(index, 0)

			self.duetFractionReset.run(pair, delayFrames=self.myOp.par.Pairanimsec * me.time.rate)
			self.matchFractionIndex(self.myOp.par.Abba)

			run('op.Engineer.DuetSwitchAbba()', delayFrames = 1 * me.time.rate)

		
		self.toggleDuetPair(duo)

	def CueDuet(self, duo):
		self.myOp.store('pair_anim_sec', int(self.myOp.par.Pairanimsec))
		pair = self.myOp.fetch('pair')
		if duo:
			self.duetFractionReset.run(pair)
			index = self.duetShapeIndex()
			chance = self.GetRandInt(1,19)
			parMatteIndex = int(index + 6)
			setattr(self.params.par, 'value{}'.format(parMatteIndex), pair)
			run('op.Engineer.Duet({},{},{},{},{})'.format(duo, pair, index, chance, parMatteIndex), delayFrames = 10)
		else:
			run('op.Engineer.Duet({},{},{},{},{})'.format(duo, pair, False, False, False), delayFrames = 10)

	def UpdateTimerLength(self, segment):
		if segment == 'trans':
			self.timerSegments[2,0] = self.myOp.par.Transitiontotalsec * self.timer.par.speed
		elif segment == 'content':
			duration = self.myOp.fetch('segment_interval')
			# if empty duration is returned, default to seg length
			if not duration:
				duration = self.myOp.par.Segmentinterval

			engineNumber = self.myOp.fetch('current_engine_number')
			
			if self.switchType == 'sec':
				self.timer.par.speed = self.timer.par.length / duration
			elif self.switchType == 'min':
				self.timer.par.speed = self.timer.par.length / duration
			elif self.switchType == 'persong':
				trackLengthFrames = op.audio.op('current_track')[1,0]
				subLength = trackLengthFrames / self.switchInterval / me.time.rate
				self.timer.par.speed = 30 / subLength

	def SetNames(self, timeslot, engineNumber, index):
		name = self.VidParser.op('select_engine' + str(engineNumber) + '_name_{}'.format(timeslot))
		# engine prev/now/next names
		setattr(self.myOp.par, 'Engine{}{}'.format(engineNumber, timeslot), name[0,0])
		# engine prev/now/next indices
		setattr(self.myOp.par, 'Engine{}index{}'.format(timeslot, engineNumber), index)

	def indexCalc(self, timeslot, index):
		if timeslot == 'next':
			if index < self.calcPlaylistTotal():
				index += 1
			else:
				index = 1
				# shuffle deck on loopback
				self.playlists.ReShuffle()

		elif timeslot == 'prev':
			if index > 1:
				index -= 1
			else:
				index = self.calcPlaylistTotal()
		#print(timeslot, index, self.myOp.fetch('manual_drop'))
		return index

	def SwitchSourceToParse(self, source):
		# switch between media or playlist drag-and-drop source
		if source == self.playLister:
			self.selectedPlaylist.par.dat = self.playlistActive
			nameColVals = 'VidName VidDur'
			pathColVals = 'VidPath'
		elif source == self.mediaLister:
			self.selectedPlaylist.par.dat = self.mediaActive
			nameColVals = 'Name Duration'
			pathColVals = 'Path'
			
		# switch cols for name/dur/path
		for operator in self.VidParser.findChildren(name='*name*'):
			operator.par.colnames = nameColVals
		for operator in self.VidParser.findChildren(name='*path*'):
			operator.par.colnames = pathColVals

	def fetchCurrentIndex(self):
		currentIndex = self.myOp.fetch('current_index')
		return currentIndex

	def storeCurrentIndex(self, operation):
		currentIndex = self.fetchCurrentIndex()
		if operation == 'add':
			newIndex = currentIndex + 1
		elif operation == 'loopback':
			newIndex = 1
		elif operation == 'sub':
			newIndex = currentIndex - 1
		elif operation == 'equal':
			newIndex = currentIndex

		self.myOp.store('current_index', newIndex)

	def LoadEngine(self, engineNumber, index, timeslot):
		# calculate index
		index = self.indexCalc(timeslot, index)

		# determine segment to be loaded (index determines name and path)
		name = self.VidParser.op('select_engine' + str(engineNumber) + '_name_{}'.format(timeslot))
		name.par.rowindexstart = index
		name.par.rowindexend = index

		relPath = self.VidParser.op('select_engine' + str(engineNumber) + '_path_{}'.format(timeslot))[0,0]
		if relPath:
			absPath = project.folder + '/' + relPath
		else:
			print("Please add a segment to the playlist to play.")

		if timeslot == 'now':
			engine = ('engine' + str(engineNumber))
			# load the segment into the engine
			if '.tox' in absPath:
				setattr(self.quadHeading.par, 'Engine{}tox'.format(engineNumber), absPath)
				setattr(self.quadHeading.par, 'Engine{}mov'.format(engineNumber), '')
				medium = 0
			# TO-DO: dfx capabilities (medium 2)
			##############################
			elif '.mov' in absPath or '.mp4' in absPath:
				setattr(self.quadHeading.par, 'Engine{}tox'.format(engineNumber), '')
				setattr(self.quadHeading.par, 'Engine{}mov'.format(engineNumber), absPath)
				medium = 2

			setattr(self.quadHeading.par, 'Engine{}medium'.format(engineNumber), medium)

			# TO-DO: add a tickline that slides left to right as duration progresses
			# self.playLister.par.Selectedrows = index

			if engineNumber is not 3 and not self.myOp.fetch('manual_drop'):
				#update current playing segment (row)
				self.playlists.par.Activesegmentrow = index
				self.myOp.store('current_index', index)

				# store duration for current interval
				self.myOp.store('segment_interval', name[0,1])

			# set previous index
			prevIndex = index - 1
			if index == 0:
				prevIndex = self.calcPlaylistTotal()

		# add names to pars for gui refs
		self.SetNames(timeslot, engineNumber, index)

		if engineNumber is not 3:
			# update timer duration
			self.UpdateTimerLength('content')

	def CueNextScene(self, index, manual):
		# determine whether cue scene originates from mediaLister or playLister
		try:
			if str(self.mediaLister) in str(index.owner):
				self.SwitchSourceToParse(self.mediaLister)
			else:
				self.SwitchSourceToParse(self.playLister)
		except:
			self.SwitchSourceToParse(self.playLister)


		# convert cue scene index to int if necessary
		index = int(index)
		print('Prev Index: ', index)

		# increment current index, if not skipping a scene
		if not self.myOp.fetch('skip_scene') and not manual and not self.myOp.fetch('manual_drop'):
			# go to beginning (loopback)
			if index == self.calcPlaylistTotal():
				self.storeCurrentIndex('loopback')
			else:
				self.storeCurrentIndex('add')
			index = self.fetchCurrentIndex()

		print('Next Index: ', index)

		# load next item for engine 1 or 2
		timeslots = ['now', 'next', 'prev']
		for timeslot in timeslots:
			if self.abba and not manual:
				engineNumber = 1
				#self.LoadEngine(engineNumber, index, timeslot)
			elif not self.abba and not manual:
				engineNumber = 2
				#self.LoadEngine(engineNumber, index, timeslot)
			if manual == 1 or manual == 2:
				engineNumber = manual
			
			if manual != 3:
				self.LoadEngine(engineNumber, index, timeslot)
		
		if manual == 3: # stream loader
			self.LoadEngine(manual, index, 'now')

		# determine if this is a manually cued scene (drag and drop) or not
		if self.abba + 1 == manual:
			self.myOp.store('manual_drop', False)
		else:
			self.myOp.store('manual_drop', bool(manual))

		# only store new engine number if an automatic abba switch;
		# if it's a manual drag, current engine # should not update
		if not self.myOp.fetch('manual_drop'):
			self.myOp.store('current_engine_number', engineNumber)

	def CheckInSegmentBlock(self, dropPos):
		# setup defs
		timeslots = ['now', 'next', 'prev']
		if self.abba:
			engineNumber = 1
		else:
			engineNumber = 2
		dropPos += 1

		index = self.fetchCurrentIndex()
		currentPos = getattr(self.myOp.par, 'Enginenowindex{}'.format(self.myOp.par.Abba+1))
		if dropPos <= currentPos and not self.playlists.par.Dropinsertorreplace:
			self.storeCurrentIndex('add')

			for timeslot in timeslots:
				index = self.indexCalc(timeslot, index)
				self.SetNames(timeslot, engineNumber, index)

		elif dropPos + 1 == currentPos:
			self.SetNames(timeslots[1], engineNumber, index)

	def CueNextTrans(self):
		# go to trans timer segment
		self.timer.goTo(segment=1)

		# prepare the transition shape index 
		self.params.par.value13 = self.GetRandInt(0,3)

		# update the total time interval for trans
		self.myOp.store('trans_interval', self.myOp.par.Transitiontotalsec)

		# get trans from playlister
		numRows = self.playlistTrans.numRows - 1
		currentScene = self.fetchCurrentIndex()
		if currentScene == 1:
			currentScene = self.calcPlaylistTotal()
		else:
			if self.myOp.par.Prev:
				pass
			else:
				currentScene -= 1

		self.selectEngine4.par.rowindexstart = currentScene
		self.selectEngine4.par.rowindexend = currentScene
		
		# update prev/now/next names ? tbd
		#self.myOp.par.Engine4next = self.selectEngine4[0,0]

		# check if XD (cross dissolve)
		if self.selectEngine4[0,0] == 'XD':
			self.myOp.store('duet_shape_index', 4)
			self.params.par.value3 = 0 
		else:
			print('not xd')
			self.params.par.value3.expr = "op('trigger_trans_gate')['timer_fraction']"
			# load trans
			relPath = self.selectEngine4[0,1]
			self.quadHeading.par.Engine4tox = project.folder + '/' + relPath
			self.myOp.par.Engine4now = self.selectEngine4[0,0]


	def ClearTrans(self):
		self.quadHeading.par.Engine4tox = parent.Nodeo.par.Defaulttox
		self.myOp.par.Engine4now = 'blank.tox'
		self.timer.par.start.pulse()

	def CueSkipScene(self, direction):
		# reset source to playlist if media was last triggered
		self.SwitchSourceToParse(self.playLister)

		currentScene = self.fetchCurrentIndex()

		if direction == 'next':
			self.timer.goTo(segment=1)
			self.myOp.par.Duet = False
			self.triggerTransGate.par.triggerpulse.pulse()
			if not self.myOp.fetch('manual_drop'): # only adjust current scene if not manually set
				if currentScene < self.calcPlaylistTotal():
					currentScene += 1
				else:
					currentScene = 1 # loopback

		elif direction == 'prev':
			# first try to reset video timer if elapsed more than 10% into scene
			if self.myOp.fetch('timer_video') > 0.1:
				self.timer.par.start.pulse()
				self.ClearSkipScene()
			else:
				self.timer.goTo(segment=1)
				self.myOp.par.Duet = False
				self.triggerTransGate.par.triggerpulse.pulse()
				if not self.myOp.fetch('manual_drop'): # only adjust current scene if not manually set
					if currentScene > 1:
						currentScene -= 1
					else:
						currentScene = self.calcPlaylistTotal() # flashforward to last element

		# update python storage
		self.myOp.store('current_index', currentScene)
		self.myOp.store('skip_scene', True)

	def ClearSkipScene(self):
		#self.timer.par.start.pulse()
		# reset prev/next
		parent().par.Prev = False
		parent().par.Next = False
		self.myOp.store('skip_scene', False)

	def UpdateSegDur(self, switchType, switchInterval, prevSwitchType):
		if switchType == 'jockey':
			self.timer.par.play = False
		else:
			self.timer.par.play = True

		if switchType == 'min' and prevSwitchType == 'sec':
			self.myOp.par.Segmentinterval = self.switchInterval / 60
		elif switchType == 'sec' and prevSwitchType == 'min':
			self.myOp.par.Segmentinterval = self.switchInterval * 60

		if switchType == 'sec':
			multiplier = 1
		elif switchType == 'min':
			multiplier = 60

		if self.myOp.par.Segmentmode == 'Global':
			for row in range(1, self.genDur.numRows):
				self.genDur[row,'duration'] = switchInterval * multiplier
		elif self.myOp.par.Segmentmode == 'Selected':
			selectedRows = str(self.mediaLister.par.Selectedrows)
			selectedRows = selectedRows.split()
			for row in selectedRows:
				self.genDur[int(row),'duration'] = switchInterval * multiplier

		self.myOp.store('segment_unit', str(switchType))

	def SetHUDVisible(self, par):
		for operator in self.gui.findChildren(name='HUD*'):
			if par:
				operator.par.display = True
			else:
				operator.par.display = False

	def UpdateMovPars(self, parName, parVal):
		if parName != 'Mov':
			setattr(self.engineMov.par, '{}'.format(parName), str(parVal))
		else:
			val = project.folder + '/' + parent.Nodeo.par.Mov \
			if not ':' in str(parent.Nodeo.par.Mov) else parent.Nodeo.par.Mov
			setattr(self.engineMov.par, '{}'.format(parName), val)

	def Bug(self, par):
		logoEnabled = self.myOp.par.Bug

		if logoEnabled:
			if 'nBumpr' in par:
				self.params.par.value5 = 0
			else:
				self.params.par.value5 = 0.5
		else:
			self.params.par.value5 = 0