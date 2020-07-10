# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	# use par.eval() to get current value
	if 0 < par < 5:
		parent.gui.Layout('MONO', str(par))
	elif 9 > par > 4:
		parent.gui.Layout('DUO', par - 4)
	elif par == 0:
		parent.gui.Layout('QUAD', 0)
	else:
		parent.gui.par.Layout = 0
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
	