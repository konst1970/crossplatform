#
# Controller
#

import model
import view

if __name__ == "__main__":

    view.view_init()

    m = model.model()

    #
    # Event loop
    #
    while(1):
        view.view_command(">>>")

        cmd = input()
        if cmd == 'C':
            view.view_create()
            name = input()
            model.create(name)
            view.view_created()

        if cmd == 'R':
            view.view_read(model.read())

        if cmd == 'U':
            view.view_update()
            old = input()
            new = input()
            model.update(old, new)
            view.view_read(model.read())

        if cmd == 'D':
            view.view_delete()
            name = input()
            model.delete(name)
            view.view_read(model.read())

        if cmd == 'E':
            break
