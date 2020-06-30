# nodeo (ALPHA)
### nodeo is a 24/7 streaming media server that showcases node-based art.

NOTE: This is currently under development.

(*) = on the roadmap but not implemented yet
(**) = in progress
	
## I. 	Nodeo acts as a train.

It has four engine (COMP) cars.

Each Engine is composed of a rotor (Base COMP) that processes video,
and a separate Snd Base COMP that processes audio.

An Engineer (Base COMP) drives the train.

## II. Segments act as train cars.

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
    
## III. A Segment Cycle acts as triad of connected train cars.

Three segments make up a Segment Cycle:
Video (Gen/Mov/Stream), Transition (Gen/Mov), and Audio.

Each row in a Playlist is considered a Segment Cycle.

## IV. An Active Playlist acts as Conductor of the train.

You may switch the Active Playlist by pulsing the Activate button 
(a small white play button directly to the right of the playlist tabs). 

Segments may also be made Active to an Engine by dragging and dropping
them onto an Engine Preview, from either a Playlist source or Media source.

## V. Structural Overview

* Nodeo
    1. SRC (Segments/Segment Cycles)
        * Media
            *Segment Type [Gen, Mov, Trans, etc.]
                *Segment
                *Segment
        * Playlist 1, 2, 3...
            * Segment Cycle [Vid, Trans, Snd]
            * Segment Cycle
            * Segment Cycle
    2. IN (Engine Previews)
        * A, B
            * Playlist ABBA Channels
        * C
            * Stream (aux) Channel
        * D
            * Trans Channel
    3. OUT (Engine Composite)
        * NDI Out
    4. PAR
        * VideoBar
            * Basic video playback controls/monitoring
        * MstrFX
            * Basic color controls
        * Modules
            * Settings (Init)
                * Folder location preferences
            * Curves
                Advanced real-time color grading
            * Encoder (Out)
                Basic output video recording
        * AudioBar
            Basic audio playback controls
        * AudioLevels
            Basic audio monitoring
