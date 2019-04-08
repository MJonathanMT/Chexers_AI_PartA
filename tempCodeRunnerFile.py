with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: Search for and output winning sequence of moves
    # ...
    # fill board with -1 values
    ran = range(-3, +3 + 1)
    board_dict = {}
    distance_dict = {}
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        distance_dict[qr] = -1

    # import data to three lists
    colour_in_play = data['colour']
    play_pieces = data['pieces']
    block_pieces = data['blocks']