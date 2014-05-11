
def main():
    import startup
    startup.run()

if __name__ == '__main__':
    '''
    import pstats, cProfile
    cProfile.runctx("main()", globals(), locals(), "Profile.prof")

    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("cumulative").print_stats(20) # or "time"
    #s.strip_dirs().sort_stats("time").print_stats(20)
    '''
    main()

