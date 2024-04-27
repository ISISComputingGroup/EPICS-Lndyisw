# Do equivalent of Scripts\snmpsim-command-responder.exe but cannot use this as exe
# embeds path to python on build server within it
import re
import sys
from snmpsim.commands.responder import main
if __name__ == '__main__':
    sys.argv[0] = 'snmpsim-command-responder'
    sys.exit(main())
