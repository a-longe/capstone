import drag_n_drop_test as engine

def test_example() -> None:
    assert True

def test_get_and_set_fen() -> None:
    with open('random_fens.txt') as file_handler:
        for fen in file_handler:
            fen = fen.strip()
            board.setup_board(fen)
            assert board.get_fen() == fen