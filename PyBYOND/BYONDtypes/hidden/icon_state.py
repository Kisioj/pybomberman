import time

class IconState(object):
    def __init__(self, icon, start_frame, name, **kwargs):
        self.width = icon.tile_width
        self.height = icon.tile_height
        self.name = name

        self._frames_count = kwargs.get('frames', 1)
        self.attr_dirs = kwargs.get('dirs', 1)
        self.attr_loop = kwargs.get('loop', -1)  # -1 = infinite, how many times loop through animation TODO
        self.attr_rewind = kwargs.get('rewind', False)  # TODO
        self.delay = kwargs.get('delay', [])
        self.total_delay = sum(self.delay)
        self.attr_movement = kwargs.get('movement', False)
        self.total_frames = self.attr_dirs * self._frames_count

        frames_to_start = start_frame
        frames_left = self.total_frames
        frames = []
        for tile_y in xrange(0, icon.height / self.height):
            for tile_x in xrange(0, icon.width / self.width):
                if frames_to_start == 0:
                    if frames_left > 0:
                        frames_left -= 1
                        rect = (tile_x * self.width, tile_y * self.height, self.width, self.height)
                        frames.append(icon.image.subsurface(rect))
                else:
                    frames_to_start -= 1

        self.frames = [[] for _ in xrange(self.attr_dirs)]
        for i, frame in enumerate(frames):
            idx = i % self.attr_dirs
            self.frames[idx].append(frame)

        # print name, kwargs


class IconStateDescriptor(object):
    def __set__(self, src, state_name):
        # print 'src', src, 'state_name', state_name

        if src._icon:
            src._icon_state = src._icon.icon_states[state_name]
            src._frame_no = 0
            src._last_time = time.time()


    def __get__(self, src, cls):
        # print 'src', src, 'cls', cls
        if isinstance(src._icon_state, IconState):
            return src._icon_state.name
        else:
            return src._icon_state