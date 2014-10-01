from libc.stdint cimport uint64_t as U64

ctypedef char BOARD_WIDTH_T
ctypedef char COLOUR_T

cpdef U64 get_occ(U64 bs, BOARD_WIDTH_T ind)
cpdef U64 set_occ(U64 bs, BOARD_WIDTH_T ind, U64 occ)
cpdef int match_five_in_a_row(U64 bs, BOARD_WIDTH_T move_ind, COLOUR_T colour)
cpdef int match_enclosed_four(U64 bs, BOARD_WIDTH_T move_ind, COLOUR_T colour)
cpdef match_capture_left(U64 bs, BOARD_WIDTH_T ind, COLOUR_T colour)
cpdef match_capture_right(U64 bs, BOARD_WIDTH_T ind, COLOUR_T colour)
cpdef get_capture_indices(bs, ind, colour)
cpdef match_threat_left(U64 bs, BOARD_WIDTH_T ind, colour)
cpdef match_threat_right(U64 bs, BOARD_WIDTH_T ind, colour)
cpdef process_takes(U64 bs, BOARD_WIDTH_T ind, BOARD_WIDTH_T strip_min, BOARD_WIDTH_T strip_max, us, int inc)
cpdef process_threats(U64 bs, BOARD_WIDTH_T ind, BOARD_WIDTH_T strip_min, BOARD_WIDTH_T strip_max, us, int inc)
cpdef process_enclosed_fours(U64 bs, BOARD_WIDTH_T move_ind, us, int inc)

# Only used for testing:
cpdef get_occ_list(bs, min_ind, max_ind)
