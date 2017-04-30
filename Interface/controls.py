import copy
from collections import OrderedDict
from . import menu

class Align:
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"
    CENTER = "center"


class Orientation:
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    BOTH = "both"
    NONE = "none"


class BorderType:
    SUNKEN = "sunken"
    LINE = "line"
    NONE = "none"


class ButtonType:
    PUSHBUTTON = "pushbutton"
    PUSHBOX = "pushbox"
    CHECKBOX = "checkbox"
    RADIO = "radio"


class BarDirection:
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    CLOCKWISE = "clockwise"
    COUNTERCLOCKWISE = "counterclockwise"


class ImageMode:
    CENTER = "center"
    STRETCH = "stretch"
    TILE = "tile"


class Lock:
    NONE = "none"
    LEFT = "left"
    RIGHT = "right"





class Macro:
    command = ""
    is_disabled = False
    map_to = ""
    name = None  # no default


class Control:
    anchor1 = None
    anchor2 = None
    background_color = "#FFF"
    border = None
    drop_zone = False
    flash = 0
    focus = False
    font_family = ""
    font_size = 0
    font_style = ""
    id = None  # is readonly, no default
    is_disabled = False
    is_transparent = False
    is_visible = True
    on_size = ""
    pos = 0, 0
    right_click = False
    size = 0, 0
    text_color = "#000"
    type = None  # is readonly, no default

    parent = None

    def __init__(self, element):
        self.id = element['id']
        self.parent = element.get('parent')
        attributes = element['attributes']
        for k, v in attributes.items():
            setattr(self, k, v)

        self._qt5_code = []
        self._qt5_name = ''

    def __repr__(self):
        d = copy.deepcopy(self.__dict__)
        del d['parent']
        return '{} {}'.format(self.__class__.__name__, d)

    def to_qt5(self):
        return ''


class Main(Control):
    alpha = 255
    can_close = True
    can_minimize = True
    can_resize = True
    can_scroll = None
    icon = ""
    image = ""
    image_mode = ImageMode.STRETCH
    is_default = False
    is_minimized = False
    is_maximized = False
    is_pane = False
    keep_aspect = False
    macro = ""
    menu = None
    on_close = ""
    statusbar = True  # False in documentation, but it cannot be true
    title = ""
    titlebar = True
    transparent_color = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = []


class Window(Main):
    is_pane = False

    def _add_qt5_code(self, text, *args, method=True):
        prefix = '        '
        if method:
            prefix += '{}.'.format(self._qt5_name)

        text = prefix + text.format(*args)
        self._qt5_code.append(text)

    def to_qt5(self):
        self._qt5_name = 'MainWindow'

        if self.title:
            self._add_qt5_code('setWindowTitle("{}")', self.title)
        if self.size != (0, 0):
            width, height = self.size
            if self.statusbar:
                height += 39
            self._add_qt5_code('setBaseSize({}, {})', width, height)

        widget_name = 'self.centralWidget'
        self._add_qt5_code('{} = QtWidgets.QWidget({})', widget_name, self._qt5_name, method=False)
        self._add_qt5_code('setCentralWidget({})', widget_name)

        if self.statusbar:
            self._add_qt5_code('', method=False)
            self._add_qt5_code('self.statusBar = QtWidgets.QStatusBar({})', self._qt5_name, method=False)
            self._add_qt5_code('setStatusBar(self.statusBar)')
            self._add_qt5_code('self.statusBar.showMessage("water")', method=False)
            self._add_qt5_code('self.statusBar.setFixedHeight(15)', method=False)

        if self.menu:
            self._add_qt5_code('', method=False)
            self._add_qt5_code('self.menuBar = QtWidgets.QMenuBar({})'.format(self._qt5_name), method=False)
            self._add_qt5_code('self.menuBar.setGeometry(QtCore.QRect(0, 0, 640, 21))', method=False)
            self._add_qt5_code('self.menuBar.setObjectName("menuBar")', method=False)

            self._add_qt5_code('', method=False)
            for group in self.menu.groups:
                self._add_qt5_code('self.{}Group = QtWidgets.QActionGroup({})'.format(group, self._qt5_name), method=False)

            for category in self.menu.categories.values():
                category_id = 'menu' + category.id
                self._add_qt5_code('', method=False)
                self._add_qt5_code('self.{} = QtWidgets.QMenu(self.menuBar)'.format(category_id), method=False)
                self._add_qt5_code('self.{0}.setObjectName("{0}")'.format(category_id), method=False)
                for element in category.elements:
                    print(element)
                    if isinstance(element, menu.Separator):
                        self._add_qt5_code('self.{}.addSeparator()'.format(category_id), method=False)
                    elif isinstance(element, menu.Action):
                        element_id = 'action' + element.id
                        self._add_qt5_code('', method=False)
                        if element.group:
                            self._add_qt5_code('self.{} = QtWidgets.QAction(self.{}Group)'.format(element_id, element.group), method=False)
                        else:
                            self._add_qt5_code('self.{} = QtWidgets.QAction(self.{})'.format(element_id, category_id), method=False)
                        self._add_qt5_code('self.{0}.setObjectName("{0}")'.format(element_id), method=False)
                        self._add_qt5_code('self.{}.addAction(self.{})'.format(category_id, element_id), method=False)
                        self._add_qt5_code('self.{}.setText("{}")'.format(element_id, element.name), method=False)
                        if element.can_check:
                            self._add_qt5_code('self.{}.setCheckable(True)'.format(element_id), method=False)
                        if element.is_checked:
                            self._add_qt5_code('self.{}.setChecked(True)'.format(element_id), method=False)

                # zastanawiam sie czy to nie moze byc wyzej
                self._add_qt5_code('', method=False)
                self._add_qt5_code('self.menuBar.addAction(self.{}.menuAction())'.format(category_id), method=False)
                self._add_qt5_code('self.{}.setTitle("{}")'.format(category_id, category.name), method=False)


            self._add_qt5_code('setMenuBar(self.menuBar)')

        for children in self.children:
            self._add_qt5_code('', method=False)
            for text in children.to_qt5():
                self._add_qt5_code(text, method=False)

        return '\n'.join(self._qt5_code)


class Pane(Main):
    is_pane = True


class Label(Control):
    align = Align.CENTER
    image = ""
    image_mode = ImageMode.STRETCH
    keep_aspect = False
    stretch = False  # deprecated
    text = ""
    text_wrap = False


class Button(Control):
    button_type = ButtonType.PUSHBUTTON
    command = ""
    group = ""
    image = ""
    is_checked = False
    is_flat = False
    text = ""
    idx = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Button.idx += 1
        self.idx = Button.idx

    def _add_qt5_code(self, text, *args, method=True):
        prefix = ''
        if method:
            prefix += '{}.'.format(self._qt5_name)

        text = prefix + text.format(*args)
        self._qt5_code.append(text)

    def to_qt5(self):
        self._qt5_name = 'self.pushButton'
        if self.idx > 1:
            self._qt5_name += '_{}'.format(self.idx)

        self._add_qt5_code('{} = PushButton(self.centralWidget)', self._qt5_name, method=False)
        if self.button_type == ButtonType.PUSHBOX:
            self._add_qt5_code('setCheckable(True)')

        self._add_qt5_code('setChecked({})', self.is_checked)

        if self.text:
            self._add_qt5_code('setText("{}")', self.text)

        if self.anchor1:
            self._add_qt5_code('setAnchor1({}, {})', *self.anchor1)

        if self.anchor2:
            self._add_qt5_code('setAnchor2({}, {})', *self.anchor2)

        if self.anchor1 or self.anchor2:
            self._add_qt5_code('MainWindow.resized.connect({}.windowResizeEvent)', self._qt5_name, method=False)

        self._add_qt5_code('setBaseGeometry({}, {}, {}, {})', *self.pos, *self.size)
        return self._qt5_code


class Input(Control):
    allow_html = False
    command = ""
    is_password = False
    multi_line = False
    no_command = False
    text = ""

    idx = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Input.idx += 1
        self.idx = Input.idx


    def _add_qt5_code(self, text, *args, method=True):
        prefix = ''
        if method:
            prefix += '{}.'.format(self._qt5_name)

        text = prefix + text.format(*args)
        self._qt5_code.append(text)

    def to_qt5(self):
        self._qt5_name = 'self.lineEdit'
        if self.idx > 1:
            self._qt5_name += '_{}'.format(self.idx)

        self._add_qt5_code('{} = Input(self.centralWidget)', self._qt5_name, method=False)

        if self.text:
            self._add_qt5_code('setText("{}")', self.text)

        if self.anchor1:
            self._add_qt5_code('setAnchor1({}, {})', *self.anchor1)

        if self.anchor2:
            self._add_qt5_code('setAnchor2({}, {})', *self.anchor2)

        if self.anchor1 or self.anchor2:
            self._add_qt5_code('MainWindow.resized.connect({}.windowResizeEvent)', self._qt5_name, method=False)

        self._add_qt5_code('setBaseGeometry({}, {}, {}, {})', *self.pos, *self.size)
        return self._qt5_code

class Output(Control):
    enable_http_images = False
    image = ""
    link_color = "#00F"
    max_lines = 1000
    style = ""
    visited_color = "#F0F"


class Browser(Control):
    auto_format = True
    on_hide = ""
    show_history = False
    show_url = False
    use_title = False


class Map(Control):
    drop_zone = True
    icon_size = 0
    letterbox = True
    on_hide = ""
    style = ""
    text_mode = False
    view_size = 0
    zoom = 0


class Info(Control):
    drop_zone = True
    highlight_color = "#0F0"
    multi_line = True
    on_hide = ""
    on_tab = ""
    prefix_color = None
    suffix_color = None
    tab_background_color = None
    tab_font_family = None
    tab_font_size = 0
    tab_text_color = None


class Child(Control):
    is_vert = False
    left = None
    lock = Lock.NONE
    right = None
    show_splitter = True
    splitter = 50


class Tab(Control):
    current_tab = ""
    multi_line = True
    on_tab = ""
    tab_font_style = ""
    tabs = ""


class Grid(Control):
    cell_span = 1, 1
    cells = 0, 0
    current_cell = 0, 0
    drop_zone = True
    enable_http_images = False
    highlight_color = "#0F0"
    is_list = False
    line_color = "#C0C0C0"
    link_color = "#00F"
    show_lines = Orientation.BOTH
    show_names = True
    small_icons = False
    style = ""
    visited_color = "#F0F"


class Bar(Control):
    angle1 = 0
    angle2 = 180
    bar_color = None
    dir = BarDirection.EAST
    is_slider = False
    on_change = ""
    value = 0
    width = 10
