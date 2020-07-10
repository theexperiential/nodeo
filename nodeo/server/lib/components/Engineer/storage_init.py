parent().unstore('*')

parent().store('current_engine_number', 1)
parent().store('current_medium', 'generative')
parent().store('current_index', 0)

parent().store('duet_speed', False)
parent().store('duet_shape_index', 0)
parent().store('pair', False)
parent().store('pair_anim_sec', parent().par.Pairanimsec)

parent().store('manual_drop', False)
parent().store('movRows', 1)
parent().store('skip_to_next_cue', True)
parent().store('skip_scene', False)

parent().store('segment_interval', parent().par.Segmentinterval)
parent().store('segment_unit', 'sec')

parent().store('segment_interval_audio', op.Snd.par.Segmentinterval)

parent().store('timer_video', op('timer/timer_video')['timer_fraction'])
parent().store('timer_audio', op('Snd/timer_audio')['timer_fraction0'])




#parent().unstore('matte_index')