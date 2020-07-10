class QuadHeadingExt:
	"""
	QuadHeadingExt description
	"""
	def __init__(self, ownerComp):
		# internal refs
		self.myOp = parent()
		self.extension = self.myOp.op('ext')
		self.start = self.myOp.op('start_your_engines')
		self.engines = self.myOp.findChildren(type=engineCOMP, depth=1)
		self.inComp = self.myOp.op('in_comp')
		self.textport = self.myOp.op('fifo1')
		self.errors = self.myOp.op('error1')
		self.filer = self.myOp.op('Filer')
		self.bugFiler = self.myOp.op('comp/bug/Filer')

	def getFolderPath(self, folder):
		if folder == 'defaulttox':
			folderPath = project.folder + '/' + parent().par.Defaulttox
		return folderPath

	def AbortSequence(self):
		# turn all engines off
		for engine in self.engines:
			engine.par.power = 0
			#self.textport.appendRow(['abort', engine])

		# clear any errors from previous session / alternate engine
		self.errors.par.clear.pulse()

	def IgnitionSequence(self):
		# start engines
		for engine in self.engines:
			engine.par.power = 0

			self.textport.appendRow(['pre', engine.par.file])

			engine.par.file = 'stator.tox'

			self.textport.appendRow(['post', engine.par.file])

			#engine.par.file.expr = "op('Filer').par.Relfilepath0" #'stator.tox' #self.myOp.par.Statortox

			engineNumber = tdu.digits(engine)
			self.start.run(engine, 0, delayFrames = engineNumber * me.time.rate) # power on
			self.start.run(engine, 1, delayFrames = (engineNumber + 0.5) * me.time.rate) # reload
			
	def ReloadEngine(self, engine):
		op('engine' + str(engine)).par.reload.pulse()

	def ClearEngine(self, engineNumber):
		op('engine' + str(engineNumber)).par.Tox = self.getFolderPath('defaulttox')

	def UpdateEngine(self, engineNumber):
		engineComp = op('engine' + str(engineNumber))
		

		#self.textport.appendRow(['ok', engineComp.par.Tox])

		# connect engine outputs
		engineComp.outputConnectors[0].connect(op('out' + str(engineNumber)).inputConnectors[0])
		engineComp.outputConnectors[0].connect(op('comp').inputConnectors[engineNumber - 1])
		engineComp.outputConnectors[1].connect(op('rename' + str(engineNumber)).inputConnectors[0])

		engineComp.par.Medium = getattr(parent().par, 'Engine{}medium'.format(engineNumber))
		engineComp.par.Tox = getattr(parent().par, 'Engine{}tox'.format(engineNumber))
		engineComp.par.Dfx = getattr(parent().par, 'Engine{}dfx'.format(engineNumber))
		engineComp.par.Mov = getattr(parent().par, 'Engine{}mov'.format(engineNumber))
		engineComp.par.Width = getattr(parent().par, 'Engine{}width'.format(engineNumber))
		engineComp.par.Height = getattr(parent().par, 'Engine{}height'.format(engineNumber))
		engineComp.par.Fps = getattr(parent().par, 'Engine{}fps'.format(engineNumber))
		engineComp.par.Title = getattr(parent().par, 'Engine{}title'.format(engineNumber))
		engineComp.par.Artist = getattr(parent().par, 'Engine{}artist'.format(engineNumber))
		engineComp.par.Year = getattr(parent().par, 'Engine{}year'.format(engineNumber))

	def UpdateBug(self):
		self.bugFiler.par.Filepath0 = parent().par.Bugimagefile

	# def SwapEnginePathsForSave(self, time):
	# 	for i in range(1,5):
	# 		if time == 'pre':
	# 			state = 'stator.tox'
	# 		else: # post
	# 			state = 'lib/components/external/stator.tox'
	# 		op('engine' + str(i)).par.Tox = state
