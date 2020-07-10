if args[0] == 'MEDIALISTER1':
	listerScenes = parent.gui.op('SRC3/MEDIA/MEDIALISTER1')
else:
	listerScenes = parent.gui.op('SRC3/PLAYLISTS/PLAYLISTER1')

if 'preview_engine1' in args[7]:
	op.Engineer.CueNextScene(listerScenes.par.Selectedrows, 1)
elif 'preview_engine2' in args[7]:
	op.Engineer.CueNextScene(listerScenes.par.Selectedrows, 2)
elif 'preview_engine3' in args[7]:
	op.Engineer.CueNextScene(listerScenes.par.Selectedrows, 3)