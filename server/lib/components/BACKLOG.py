     .-.     .-.     .-.     .-.     .-.     .-.     .-.
`._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'

=======
BACKLOG
=======

------------------------------------------------------------

Content ()

X paintWaves not loading
X dystopiaStudy not loading
X golde remove green
X flex -> optimize for RT (sliceSliceStudy)
- darkTimesStudy not loading (lel)
X thumbnails for transitions
- thumbnails/more toxes for streams

------------------------------------------------------------

COMP ()

X occasional GLSL flicker on output still (fixed?)
- call SetNames() when adding/removing items from playlist
- timer needs fixes for transition timing

UI ()

-src
	- time in both min/sec

-media src
	- fix search bug (drop onto playlist from search fails index reCalc)
		add character-by-character search
	- movie thumbnail generator has issues inside of Engine COMP
	X update durations
	- if dragging > total num items than playlister into playlister, ignore items after ==

-playlist src
	X parse transitions
	- parse audio
	X update durations
	- update trans durations

	- make seg len unit (sec/min) global: affects both playlister and medialister
	
	- if playlist is changes length, confirm 
		that current position has number after it. if not, reset to 0.
		if cleared, always reset to zero.

-audio player
	X play/pause
	X volume
	X mute button (akin to 'Live' button)
	X output dev toggle
	X stream/file/autoplay menu
	X time elapsed/remaining display
	X audio levels preview
	- ffwd/rwd btn functionality

-C channel [pip]
	X pip button
	- stream pip placement (tx, ty, scale, rotation) 
		[good candidate for exposed pars]
	- bug after dragged in (repeats playlist item)
	
-MSTR FX
	- sharpen
	- animate btns (0,1,2,3)

------------------------------------------------------------
ROADMAP (to 1.0)

- json settings
- json playlists
- expose pars for toxes to GUI
- text modules
- vote on artwork
- artist/title/avatar lwr3rds
- basic tags logic (for duet triggering / smart shuffle)

------------------------------------------------------------
DONE ()

X Duet functionality
X crossfade between A/B

X Encoder recording panel
	X basic implementation
	X functionality/rec btn

X Misc
	X Add reloading txt to HUD stats on EngineReload()

X video player
	X display prev/next scene names
	X transition segment duration (moved to media backlog)

X maximize window layouts (quad/fullscreen)

X settings tab
	X folder preferences (for mediums)

X playlists
	X tab functionality
	X drag and drop different segment types onto each playlist item (trans/audio)

X stator
	X video types = Tox/Dfx/Mov
	X load movs

X engines
	X clear video (switch to blank.tox) buttons
	X reload engine buttons
	X automatically relaunch every 24 hrs (to stop mem leaks)

-Playlists
	X add
	X delete
	X rename
	X switch between
	X lock/unlock
	X play (export lock)
	X sort alphabetical/shuffle/manual functionality
	X if deleted file, retain touch session & recreate file (check if file exists?)
	