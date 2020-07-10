# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	# use par.eval() to get current value
	if par.name == 'Vidsort' or par.name == 'Transsort' or par.name == 'Sndsort':
		run('parent.Playlister.Sorter(args[0], args[1])', par.name, par, delayFrames = 5)
	return

def onPulse(par):
	return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	