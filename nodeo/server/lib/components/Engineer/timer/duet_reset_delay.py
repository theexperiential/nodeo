params = op('params')
for i in range(6, 10):
	setattr(params.par, 'value{}'.format(i), args[0])
# this fixes the pairing so that the correct
# glsl is rendered
if args[0]:
	correctVal = args[0] # for A (engine 1)
else:
	correctVal = 1 - args[0] # for B (engine 2)
params.par.value11 = correctVal # index abba