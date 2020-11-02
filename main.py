from functools import partial
import signal

from pywayland import lib
from wlroots import lib as wlrLib
from pywayland.server import Display

from wlroots.backend import Backend
from wlroots.renderer import Renderer

from wlroots.wlr_types import (
    Compositor,
    XdgShell,
    OutputLayout,
    Cursor,
    XCursorManager,
    Seat
)

# from simpleAccess import SimpleAccessWM
from keyboardAdditions import SimpleAccessWM
# wlrLib.wlr_layer
def signalInt(display, signalNumber, frame):
    print("SIGINT Received")
    display.terminate()

def main():
    with Display() as display:
        signal.signal(signal.SIGINT, partial(signalInt, display))
        with Backend(display) as backend:
            renderer = Renderer(backend, display)
            compositor = Compositor(display, renderer)
            xdgShell = XdgShell(display)
            with OutputLayout() as outputLayout, Cursor(outputLayout) as cursor,XCursorManager(24) as xCursorManager, Seat(display, "seat0") as seat:
                wm = SimpleAccessWM(
                    display, backend, renderer, xdgShell, outputLayout, cursor, xCursorManager, seat
                    )
                # 
                backend.start()
                display.run()
                display.destroy()
            # with OutputLayout() as outputLayout:

main()