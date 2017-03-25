class IconState(object):
    def __init__(self, icon, start_frame, name, **kwargs):
        self.width = icon.tile_width
        self.height = icon.tile_height
        self.name = name

        self.attr_frames = kwargs.get('frames', 1)
        self.attr_dirs = kwargs.get('dirs', 1)
        self.attr_loop = kwargs.get('loop', False)
        self.attr_delay = kwargs.get('delay')
        self.attr_movement = kwargs.get('movement', False)
        self.total_frames = self.attr_dirs * self.attr_frames

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

        icon = src.__dict__.get('icon')
        if icon:
            src.__dict__['icon_state'] = icon.icon_states[state_name]
        else:
            src.__dict__['icon_state'] = state_name

    def __get__(self, src, cls):
        # print 'src', src, 'cls', cls

        icon = src.__dict__.get('icon')
        icon_state = src.__dict__.get('icon_state', '')
        if icon and icon_state:
            icon_state = icon_state.name
        return icon_state
