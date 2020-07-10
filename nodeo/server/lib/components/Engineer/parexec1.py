# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	# use par.eval() to get current value
	
	if par.name == 'Abba':
		parent().SwitchAbba(par.eval())
	elif par.name == 'Duet':
		parent().CueDuet(par)
	elif par.name == 'Duetspeed':
		pass
	elif par.name == 'Bug':
		parent().Bug('null')
	elif par.name == 'Segmentunit' or par.name == 'Segmentinterval':
		parent().UpdateSegDur(parent().par.Segmentunit, parent().par.Segmentinterval, prev)
		parent().UpdateTimerLength('trans')
	
	elif par.name == 'Next' and par:
		parent().CueSkipScene('next')
	elif par.name == 'Prev' and par:
		parent().CueSkipScene('prev')
	
	elif par.name == 'Transitiontotalsec':
		parent().UpdateTimerLength('trans')


	# Mov
	elif par.name == 'Mov' or par.name == 'Previewres1' \
	or par.name == 'Previewres2' or par.name == 'Previewframelocation':
		parent().UpdateMovPars(par.name, par)

	return

def onPulse(par):		
	if par.name == 'Reset':
		parent().ResetPlayback()
		
	return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	