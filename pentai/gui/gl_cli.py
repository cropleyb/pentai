
import kivy.uix.listview as lv_m
import kivy.uix.button as b_m
from kivy.properties import ObjectProperty, ListProperty

from kivy.uix.gridlayout import GridLayout

class ListItemButton(lv_m.SelectableView, b_m.Button):
    ''':class:`~kivy.uix.listview.ListItemButton` mixes
    :class:`~kivy.uix.listview.SelectableView` with
    :class:`~kivy.uix.button.Button` to produce a button suitable for use in
    :class:`~kivy.uix.listview.ListView`.
    '''

    selected_color = ListProperty([1., 0., 0., 1])
    '''
    :attr:`selected_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [1., 0., 0., 1].
    '''

    deselected_color = ListProperty([0., 1., 0., 1])
    '''
    :attr:`selected_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [0., 1., 0., 1].
    '''

    def __init__(self, **kwargs):
        super(ListItemButton, self).__init__(**kwargs)

        # Set Button bg color to be deselected_color.
        self.background_color = self.deselected_color

    def select(self, *args):
        self.background_color = self.selected_color
        if isinstance(self.parent, CompositeListItem):
            self.parent.select_from_child(self, *args)

    def deselect(self, *args):
        self.background_color = self.deselected_color
        if isinstance(self.parent, CompositeListItem):
            self.parent.deselect_from_child(self, *args)

    def select_from_composite(self, *args):
        self.background_color = self.selected_color

    def deselect_from_composite(self, *args):
        self.background_color = self.deselected_color

    def __repr__(self):
        return '<%s text=%s>' % (self.__class__.__name__, self.text)

class CompositeListItem(lv_m.SelectableView, GridLayout):
    ''':class:`~kivy.uix.listview.CompositeListItem` mixes
    :class:`~kivy.uix.listview.SelectableView` with :class:`GridLayout` for a
    generic container-style list item, to be used in
    :class:`~kivy.uix.listview.ListView`.
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''ListItem sublasses Button, which has background_color, but
    for a composite list item, we must add this property.

    :attr:`background_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [1, 1, 1, 1].
    '''

    selected_color = ListProperty([1., 0., 0., 1])
    '''
    :attr:`selected_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [1., 0., 0., 1].
    '''

    deselected_color = ListProperty([.33, .33, .33, 1])
    '''
    :attr:`deselected_color` is a :class:`~kivy.properties.ListProperty` and
    defaults to [.33, .33, .33, 1].
    '''

    representing_cls = ObjectProperty(None)
    '''Which component view class, if any, should represent for the
    composite list item in __repr__()?

    :attr:`representing_cls` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    def __init__(self, **kwargs):
        self.rows = 1
        super(CompositeListItem, self).__init__(**kwargs)

        # Example data:
        #
        #    'cls_dicts': [{'cls': ListItemButton,
        #                   'kwargs': {'text': "Left"}},
        #                   'cls': ListItemLabel,
        #                   'kwargs': {'text': "Middle",
        #                              'is_representing_cls': True}},
        #                   'cls': ListItemButton,
        #                   'kwargs': {'text': "Right"}]

        # There is an index to the data item this composite list item view
        # represents. Get it from kwargs and pass it along to children in the
        # loop below.
        index = kwargs['index']

        for cls_dict in kwargs['cls_dicts']:
            cls = cls_dict['cls']
            cls_kwargs = cls_dict.get('kwargs', None)

            if cls_kwargs:
                cls_kwargs['index'] = index

                if 'selection_target' not in cls_kwargs:
                    cls_kwargs['selection_target'] = self

                if 'text' not in cls_kwargs:
                    cls_kwargs['text'] = kwargs['text']

                if 'is_representing_cls' in cls_kwargs:
                    self.representing_cls = cls

                self.add_widget(cls(**cls_kwargs))
            else:
                cls_kwargs = {}
                cls_kwargs['index'] = index
                if 'text' in kwargs:
                    cls_kwargs['text'] = kwargs['text']
                self.add_widget(cls(**cls_kwargs))

    def select(self, *args):
        self.background_color = self.selected_color

    def deselect(self, *args):
        self.background_color = self.deselected_color

    def select_from_child(self, child, *args):
        for c in self.children:
            if c is not child:
                c.select_from_composite(*args)

    def deselect_from_child(self, child, *args):
        for c in self.children:
            if c is not child:
                c.deselect_from_composite(*args)

    def __repr__(self):
        if self.representing_cls is not None:
            return '<%r>, representing <%s>' % (
                self.representing_cls, self.__class__.__name__)
        else:
            return '<%s>' % (self.__class__.__name__)
