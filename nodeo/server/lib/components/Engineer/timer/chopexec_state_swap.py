# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

def onOffToOn(channel, sampleIndex, val, prev):	
	return

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):

	# fire duet 33% of the time
	chance = tdu.rand(absTime.frame)
	if chance < 0.25:
		fireDuet = True
	else:
		fireDuet = False
	
	run('op.Engineer.par.Duet = {}'.format(fireDuet), delayFrames=op.Engineer.par.Pairdelaysec * me.time.rate)
	
	if op.Engineer.fetch('skip_scene'):
		op.Engineer.ClearSkipScene()
	
	return
	