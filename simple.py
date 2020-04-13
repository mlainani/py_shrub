# set           Set operational options
#
#     date          Set system date and time
#
#       <MMDDhhmm>    Set system date and time
#       <MMDDhhmmYY>
#       <MMDDhhmmCCYY>
#       <MMDDhhmmCCYY.ss>
#       ntp           Set system date and time from NTP server (default: 0.pool.ntp.org)
#
#
#
#
#
# show          Show system information
#
#   date          Show system time and date
#
#     utc           Show system date and time as Coordinated Universal Time
#
#       maya          Show UTC date in Maya calendar format
#
#
#   system        Show system information
#
#
#     uptime        Show how long the system has been up
import sys
import tty

cmds = ['set date ntp', 'show date', 'show date utc', 'show date utc maya', 'show system uptime']

dict = {'set': 'Set operational options', 'show': 'Show system information'}

# for keyword in dict.keys():
#     description = dict[keyword]
#     print("%s - %s" % (keyword, description))

prompt = "# "
prompt_len = len(prompt)

def read_line():
    tty.setraw(sys.stdin)
    # sys.stdout.write(prompt)
    # sys.stdout.flush()

    input = ""
    index = 0
    while True:
        char = ord(sys.stdin.read(1))

        if char == 3: # CTRL-C
            sys.exit(0)

        # elif char == 9: # TAB
        #     for keyword in dict.keys():
        #         description = dict[keyword]
        #         print("%s - %s" % (keyword, description))
        #         sys.stdout.write("\u001b[1000D")

        elif char in {10, 13}: # Enter
            sys.stdout.write(u"\u001b[1000D")
            print("\nEchoing... %s" % input)
            return

        elif char == 27:
            next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
            if next2 == 68: # Left
                index = max(0, index - 1)
            elif next2 == 67: # Right
                index = min(len(input), index + 1)

        elif 32 <= char <= 126:
            input = input[:index] + chr(char) + input[index:]
            index += 1

        sys.stdout.write(u"\u001b[1000D")
        sys.stdout.write(input)
        sys.stdout.flush()


while True:
    read_line()