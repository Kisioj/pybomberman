from ... import internals
from .icon import IconDescriptor
from .icon_state import IconStateDescriptor


class MappableMeta(type):
    _icon = None
    _icon_state = None
    icon = IconDescriptor()
    icon_state = IconStateDescriptor()

    def __new__(mcs, name, bases, dct):
        print '-----------------------------------'
        print "Allocating memory for class", name
        print mcs
        print bases
        print dct
        dct['superpartia'] = 10

        icon = dct.get('icon')
        if isinstance(icon, str):  # choc lepiej by bylo spradzic chyba czy nie jest IconDescriptorem
            dct['icon'] = IconDescriptor()

        icon_state = dct.get('icon_state')
        if isinstance(icon_state, str):
            dct['icon_state'] = IconStateDescriptor()

        cls = super(MappableMeta, mcs).__new__(mcs, name, bases, dct)
        if isinstance(icon, str):
            cls.icon = icon
        if isinstance(icon_state, str):
            cls.icon_state = icon_state

        return cls

    def __init__(cls, name, bases, dct):
        # print '-----------------------------------'
        # print "Initializing class", name
        # print cls
        # print bases
        # print dct

        # icon = dct.get('icon', '')
        # if icon and isinstance(icon, str):
        #     cls.icon = icon
        #
        # icon_state = dct.get('icon_state', '')
        # if isinstance(icon_state, str):
        #     cls.icon_state = icon_state


        # cls.icon = IconDescriptor()
        # cls.icon_state = IconStateDescriptor()

        # dct['icon'] = IconDescriptor()
        # dct['icon_state'] = IconStateDescriptor()
        # if dct.get('icon'):
        #     del dct['icon']
        # if dct.get('icon_state'):
        #     del dct['icon_state']

        # import pdb; pdb.set_trace()
        # print cls.icon
        # if cls.__name__ == 'Box':
        #     del cls.icon
        # cls.__dict__.update({'icon': IconDescriptor()})
        # setattr(cls, 'icon', IconDescriptor())
        dct['x'] = 12
        super(MappableMeta, cls).__init__(name, bases, dct)
        internals.mappable_types[name] = cls, {}
