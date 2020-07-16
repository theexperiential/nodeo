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
	# midnight refresh for engine that's not playing
	if channel.name == 'hour' and val == 0:
		engineToReload = (1 - op.Engineer.par.Abba) + 1
		parent.Nodeo.ReloadEngine(engineToReload)

		print('Reloaded Engine ', engineToReload)

		segmentInterval = op.Engineer.fetch('segment_interval')
		progress = op.Engineer.fetch('timer_video')
		secondsRemaining = (1.0 - progress) * segmentInterval
		reloadOtherIn = secondsRemaining + op.Engineer.fetch('trans_interval') + 3 # add 3 to be safe

		reloadOtherEngine = 'parent.Nodeo.ReloadEngine({} + 1)'.format(op.Engineer.par.Abba)
		run(reloadOtherEngine, delayFrames = reloadOtherIn * me.time.rate)

		printSecond = "print('Reloaded Engine ', {}".format(op.Engineer.par.Abba + 1)
		run(printSecond, delayFrames = reloadOtherIn * me.time.rate)

	return
	