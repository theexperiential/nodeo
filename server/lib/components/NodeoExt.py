class Nodeo:
	"""
	nodeo is a 24/7 streaming media server that showcases node-based art.
	written @ TEC, with generous support from members of the Touch community.
	tec.design

	* = on the roadmap but not implemented yet
	** = in progress
	
	I. 	Nodeo acts as a train.

			It has four engine (COMP) cars.

			Each Engine is composed of a rotor (Base COMP) that processes video,
			and a separate Snd Base COMP that processes audio.

			An Engineer (Base COMP) drives the train.
	
	II. Segments act as train cars.

			Each carries a temporal fragments of a type of media.

			Segment Types/Sub-types:
			1. Video (Scene)
				a. Generative (tox and dfx*)
				b. Movie (mov**)
				c. Stream** (NDI)
			2. Transition
				a. Generative (tox and dfx*)
				b. Movie (mov**)
			3. Audio (wav, aiff and stream) 
			4. Text*
		
	III. A Segment Cycle acts as triad of connected train cars.
	
			Three segments make up a Segment Cycle:
			Video (Gen/Mov/Stream), Transition (Gen/Mov), and Audio.

			Each row in a Playlist is considered a Segment Cycle.
	
	IV. An Active Playlist acts as Conductor of the train.

		You may switch the Active Playlist by pulsing the Activate button 
		(a small white play button directly to the right of the playlist tabs). 
	
		Segments may also be made Active to an Engine by dragging and dropping
		them onto an Engine Preview, from either a Playlist source or Media source.


	Nodeo
		SRC (Segments/Segment Cycles)
		|---Media
		|		Segment Type [Gen, Mov, Trans, etc.]
		|			Segment
		|			Segment
		|---Playlist 1, 2, 3...
		|		Segment Cycle [Vid, Trans, Snd]
		|		Segment Cycle
		|		Segment Cycle
		|
		IN (Engine Previews)
		|---A, B
		|		Playlist ABBA Channels
		|---C
		|		Stream (aux) Channel
		|---D
		|		Trans Channel
		|
		OUT (Engine Composite)
		|---NDI Out
		|
		PAR
		|---VideoBar
		|		Basic video playback controls/monitoring
		|---MstrFX
		|		Basic color controls
		|---Modules
		|		Settings (Init)
		|			Folder location preferences
		|		Curves
		|			Advanced real-time color grading
		|		Encoder (Out)
		|			Basic output video recording
		|---AudioBar
		|		Basic audio playback controls
		|---AudioLevels
		|		Basic audio monitoring

		

	"""
	def __init__(self, ownerComp):
		# internal refs
		self.myOp = ownerComp
		self.Engineer = self.myOp.op('Engineer')
		self.Comp = self.myOp.op('comp')
		self.External = self.myOp.op('external')

		self.quadHeading = self.myOp.op('quad_heading')
		
		self.start = self.myOp.op('start_your_engines')
		self.engines = self.myOp.findChildren(type=engineCOMP, depth=1)

		# external refs
		self.params = self.Engineer.op('timer/params')

	def AbortSequence(self):
		for i in range(1,5):
			setattr(self.quadHeading.par, 'Engine{}tox'.format(i), self.myOp.par.Defaulttox)

	def IgnitionSequence(self):
		# start with quad heading off
		self.quadHeading.par.power = 0

		# don't cook the templates!
		for operator in self.External.findChildren(type=COMP, depth=1):
			operator.allowCooking = False

		# re-launch quad heading engine (this is a stability patch, hopefully fixed in future TD build)
		powerOnEngine = "op('quad_heading').par.power = 1"
		reloadEngine = "op('quad_heading').par.reload.pulse()"

		run(powerOnEngine, delayFrames = 3 * me.time.rate) # power on
		run(reloadEngine, delayFrames = 4 * me.time.rate) # reload

		# inform nodeo that it has just been intialized
		self.myOp.store('armed_for_playback', True)

		# disable output
		self.myOp.par.Output = False

		# update quad heading pars
		self.myOp.UpdateQuadHeadingParams()

	def UpdateQuadHeadingParams(self):
		# get pars from nodeo custom pars and pass them into quad_heading
		self.quadHeading.par.Statortox = self.myOp.par.Statortox
		self.quadHeading.par.Defaulttox = self.myOp.par.Defaulttox
		self.quadHeading.par.Width = self.myOp.par.Width
		self.quadHeading.par.Height = self.myOp.par.Height
		self.quadHeading.par.Output = self.myOp.par.Output
		self.quadHeading.par.Ndiout = self.myOp.par.Ndiout
		self.quadHeading.par.Ndiname = self.myOp.par.Ndiname
		self.quadHeading.par.Bugimagefile = self.myOp.par.Bugimagefile

		# unify resolutions from global Width and Height pars
		for i in range (1,5):
			setattr(self.quadHeading.par, 'Engine{}width'.format(i), self.myOp.par.Width)
			setattr(self.quadHeading.par, 'Engine{}height'.format(i), self.myOp.par.Height)

	def ReloadEngine(self, engineNumber):
		# hacky af, need to replace following block
		if engineNumber == 1:
			self.quadHeading.par.Engine1reload.pulse()
		elif engineNumber == 2:
			self.quadHeading.par.Engine2reload.pulse()
		elif engineNumber == 3:
			self.quadHeading.par.Engine3reload.pulse()
		else:
			self.quadHeading.par.Engine4reload.pulse()

		#setattr(self.quadHeading.par, 'Engine{}reload'.format(engineNumber), pulse())

	def ClearEngine(self, engineNumber):
		#op('engine' + str(engineNumber)).par.Tox = self.getFolderPath('defaulttox')
		setattr(self.quadHeading.par, 'Engine{}tox'.format(engineNumber), 'blank.tox')