# Steam Controller On-Screen Keyboard


## Dependencies

* GNU / Linux
* Python 3
* [PyGame](http://pygame.org/)
* [Standalone Steam Controller Driver](https://github.com/ynsta/steamcontroller)

## Usage

```$ python scosk.py ```

Creates a pygame window with a virtual keyboard. To initialize, ensure the steam controller and connected and communicating with your computer. As you press the clickpad, a keyboard press event should occur on the currently focused screen.

## TODO

* Refactor with event controller
* mimic official Steam design
* pop up on screen away from mouse, on-top and unfocused (may require talking to X or the window manager)
* integrate with [sc-desktop](https://github.com/ynsta/steamcontroller/blob/master/scripts/sc-desktop.py)

## Notes

I've only tested from within a tiling window manager. I as the author, assume no liability for what you do with this program.
