
def main():
    import startup
    startup.run()

import logging, sys

if __name__ == "__main__":
    '''
    import pstats, cProfile
    cProfile.runctx("main()", globals(), locals(), "Profile.prof")

    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("cumulative").print_stats(20) # or "time"
    #s.strip_dirs().sort_stats("time").print_stats(20)
    '''
    formatter = logging.Formatter("[%(asctime)s.%(msecs)03d][%(levelname)s][%(message)s]",
                                          "%H:%M:%S")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    sys._kivy_logging_handler = console

    main()

