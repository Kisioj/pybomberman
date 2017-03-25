# directions
NORTH = 1
SOUTH = 2
EAST = 4
WEST = 8
NORTHEAST = 5
NORTHWEST = 9
SOUTHEAST = 6
SOUTHWEST = 10
UP = 16
DOWN = 32

SOUTH_INDEX = 0
NORTH_INDEX = 1
EAST_INDEX = 2
WEST_INDEX = 3

# eye and sight
BLIND = 1
SEE_MOBS = 4
SEE_OBJS = 8
SEE_TURFS = 16
SEE_SELF = 32
SEE_INFRA = 64
SEE_PIXELS = 256
SEE_THRU = 512
SEE_BLACKNESS = 1024
SEEINVIS = 2
SEEMOBS = 4
SEEOBJS = 8
SEETURFS = 16
MOB_PERSPECTIVE = 0
EYE_PERSPECTIVE = 1
EDGE_PERSPECTIVE = 2

# layers
FLOAT_LAYER = -1
AREA_LAYER = 1
TURF_LAYER = 2
OBJ_LAYER = 3
MOB_LAYER = 4
FLY_LAYER = 5
EFFECTS_LAYER = 5000
TOPDOWN_LAYER = 10000
BACKGROUND_LAYER = 20000
FLOAT_PLANE = -32767


# map formats
TOPDOWN_MAP = 0
ISOMETRIC_MAP = 1
SIDE_MAP = 2
TILED_ICON_MAP = 32768

# gliding
NO_STEPS = 0
FORWARD_STEPS = 1
SLIDE_STEPS = 2
SYNC_STEPS = 3

# appearance flags
LONG_GLIDE = 1
RESET_COLOR = 2
RESET_ALPHA = 4
RESET_TRANSFORM = 8
NO_CLIENT_COLOR = 16
KEEP_TOGETHER = 32
KEEP_APART = 64
PLANE_MASTER = 128
TILE_BOUND = 256

TRUE = 1
FALSE = 0

MALE = "male"
FEMALE = "female"
NEUTER = "neuter"
PLURAL = "plural"

MOUSE_INACTIVE_POINTER = 0
MOUSE_ACTIVE_POINTER = 1
MOUSE_DRAG_POINTER = 3
MOUSE_DROP_POINTER = 4
MOUSE_ARROW_POINTER = 5
MOUSE_CROSSHAIRS_POINTER = 6
MOUSE_HAND_POINTER = 7
MOUSE_LEFT_BUTTON = 1
MOUSE_RIGHT_BUTTON = 2
MOUSE_MIDDLE_BUTTON = 4
MOUSE_CTRL_KEY = 8
MOUSE_SHIFT_KEY = 16
MOUSE_ALT_KEY = 32

CONTROL_FREAK_ALL = 1
CONTROL_FREAK_SKIN = 2
CONTROL_FREAK_MACROS = 4

MS_WINDOWS = "MS Windows"
UNIX = "UNIX"

# sound
SOUND_MUTE = 1
SOUND_PAUSED = 2
SOUND_STREAM = 4
SOUND_UPDATE = 16

# icons
ICON_ADD = 0
ICON_SUBTRACT = 1
ICON_MULTIPLY = 2
ICON_OVERLAY = 3
ICON_AND = 4
ICON_OR = 5
ICON_UNDERLAY = 6

# matrix
MATRIX_COPY = 0
MATRIX_MULTIPLY = 1
MATRIX_ADD = 2
MATRIX_SUBTRACT = 3
MATRIX_INVERT = 4
MATRIX_ROTATE = 5
MATRIX_SCALE = 6
MATRIX_TRANSLATE = 7
MATRIX_INTERPOLATE = 8
MATRIX_MODIFY = 128

# animation easing
LINEAR_EASING = 0
SINE_EASING = 1
CIRCULAR_EASING = 2
CUBIC_EASING = 3
BOUNCE_EASING = 4
ELASTIC_EASING = 5
BACK_EASING = 6
QUAD_EASING = 7
EASE_IN = 64
EASE_OUT = 128

# animation flags
ANIMATION_END_NOW = 1
ANIMATION_LINEAR_TRANSFORM = 2
ANIMATION_PARALLEL = 4

# blend mode
BLEND_DEFAULT = 0
BLEND_OVERLAY = 1
BLEND_ADD = 2
BLEND_SUBTRACT = 3
BLEND_MULTIPLY = 4