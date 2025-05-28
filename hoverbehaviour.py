from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget

class HoverBehavior(object):
    hovered = BooleanProperty(False)
    border_point = []

    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        self._binded = False
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        self.bind(pos=self.update_hover_area,
                  size=self.update_hover_area)

    def update_hover_area(self, *args):
        if not self._binded:
            Window.bind(mouse_pos=self.on_mouse_pos)
            self._binded = True

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass
