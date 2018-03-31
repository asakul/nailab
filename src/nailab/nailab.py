
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk, GObject
from gi.repository import GtkSource

from nailab.ui.applicationwindow import ApplicationWindow

def main():
    GObject.type_register(GtkSource.View)

    builder = Gtk.Builder()
    builder.add_from_file('ui/nailab.glade')

    ApplicationWindow(builder)

    Gtk.main()

if __name__ == '__main__':
    main()
