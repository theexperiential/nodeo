![Nodeo Logo](/src/img/nodeo-logo.svg)
# :framed_picture: + :bulb: = nodeo
### A generative art gallery for everyone

:pencil2: This is a Public Alpha *under active development* 

:floppy_disk: TouchDesigner 2020.**24520** \
:desktop_computer: Windows 10 64-bit

---

![Nodeo Screenshot](/src/img/nodeo-capture.png)

---

#### :film_projector: Why I am building this
I am building nodeo to enable everyone to display and/or perform an unlimited number of generative scenes for their streams, permanent installations and live events. The aim is stable, aesthetic and customizable 24/7 delivery of TouchDesigner components and Notch blocks to external displays and/or apps/platforms (such as OBS/Twitch) via NDI. 

The name is a combination of *node* and *video,* as a good share of generative artwork is created in node-based environments.

#### :book: How to use

Download or clone the entire repo. Inside of the [server](/server) folder is the nodeo main toe file. Open it on a reasonably powerful computer. (Windows i7 / GTX 1080 eq. or better Desktop is recommended)

---

### :mailbox_with_mail: Releases

#### 2020.5.246

* Duration handling improvements
* Minor bug fixes

#### 2020.5.227
* Overhauled Engine + composite system so it is separately threaded from the UI. This greatly improves performance and enables UI interactions without impacting NDI output frame rates.
* Many minor bug fixes
* Various minor improvements
* Blackout button improved (thanks @drmbt)
* Audio options expanded (thanks @drmbt)

#### 2020.2.2180
* Initial public release

---

### :sparkle: System Outline
(*) = *on the roadmap but not implemented yet* \
(**) = *in progress*
	
#### I. 	Nodeo acts as a train.

It has four engine (COMP) cars.

Each Engine is composed of a rotor (Base COMP) that processes video,
and a separate Snd Base COMP that processes audio.

An Engineer (Base COMP) drives the train.

#### II. Segments act as train cars.

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
    
#### III. A Segment Cycle acts as triad of connected train cars.

Three segments make up a Segment Cycle:
Video (Gen/Mov/Stream), Transition (Gen/Mov), and Audio.

Each row in a Playlist is considered a Segment Cycle.

#### IV. An Active Playlist acts as Conductor of the train.

You may switch the Active Playlist by pulsing the Activate button 
(a small white play button directly to the right of the playlist tabs). 

Segments may also be made Active to an Engine by dragging and dropping
them onto an Engine Preview, from either a Playlist source or Media source.

### :cinema: Structural Overview

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

### Credits

Many thanks to the following devs and artists for their contributions, which made nodeo possible:

* [Derivative](https://derivative.ca)
* [Elburz](https://interactiveimmersive.io)
* [Tim Franklin](https://github.com/franklin113)
* [paketa12](https://patreon.com/paketa12)
* [Alpha Moonbase](https://alphamoonbase.de/)
* [Richard Burns](https://github.com/Richard-Burns)
* [Vasily](https://github.com/Ajasra)
* [Panda](https://anitakucharczyk.com)

:radioactive: Full documentation is in progress.