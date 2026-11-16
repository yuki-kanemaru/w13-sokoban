"""sokoban_exercise.py の動作確認テスト。

実行方法:
    python -m unittest -v test_sokoban
"""

import unittest

import sokoban_exercise as game

# 各ステージのクリア手順。1文字が1手に対応する。
LEVEL_SOLUTIONS = ["w", "wsaw", "wwwdwaaaawasss", "awsdddw"]


class NewBoardTest(unittest.TestCase):
    def test_rejects_uneven_rows(self):
        with self.assertRaises(ValueError):
            game.new_board("####\n#  #\n###")

    def test_rejects_two_players(self):
        with self.assertRaises(ValueError):
            game.new_board("#####\n#@.@#\n#$  #\n#####")

    def test_rejects_crate_goal_mismatch(self):
        with self.assertRaises(ValueError):
            game.new_board("#####\n#@.. #\n#$   #\n#    #\n#####")


class MoveTest(unittest.TestCase):
    def test_wall_and_outside_are_blocked(self):
        board = game.new_board("#####\n#@$.#\n#####")
        self.assertFalse(game.can_enter(board, (0, 1)))
        self.assertFalse(game.can_enter(board, (-1, 1)))
        self.assertTrue(game.can_enter(board, (2, 1)))

    def test_move_into_wall_keeps_state(self):
        board = game.new_board("#####\n#@  #\n# $.#\n#####")
        self.assertFalse(game.apply_move(board, "w"))
        self.assertEqual(board["hero"], (1, 1))
        self.assertEqual(board["steps"], 0)
        self.assertEqual(board["past"], [])

    def test_unknown_key_is_ignored(self):
        board = game.new_board("#####\n#@$.#\n#####")
        self.assertFalse(game.apply_move(board, "x"))
        self.assertEqual(board["steps"], 0)

    def test_push_into_wall_fails(self):
        board = game.new_board("######\n#@$#.#\n#    #\n######")
        self.assertFalse(game.apply_move(board, "d"))
        self.assertEqual(board["hero"], (1, 1))
        self.assertEqual(board["crates"], {(2, 1)})

    def test_push_into_crate_fails(self):
        board = game.new_board("#######\n#@$$..#\n#     #\n#######")
        self.assertFalse(game.apply_move(board, "d"))
        self.assertEqual(board["crates"], {(2, 1), (3, 1)})

    def test_push_moves_crate_and_counts_step(self):
        board = game.new_board("#####\n#@$.#\n#####")
        self.assertTrue(game.apply_move(board, "d"))
        self.assertEqual(board["hero"], (2, 1))
        self.assertEqual(board["crates"], {(3, 1)})
        self.assertEqual(board["steps"], 1)
        self.assertTrue(game.completed(board))


class UndoTest(unittest.TestCase):
    def test_step_back_restores_state(self):
        board = game.new_board("#####\n#@$.#\n#####")
        game.apply_move(board, "d")
        game.step_back(board)
        self.assertEqual(board["hero"], (1, 1))
        self.assertEqual(board["crates"], {(2, 1)})
        self.assertEqual(board["steps"], 0)

    def test_step_back_without_history_does_nothing(self):
        board = game.new_board("#####\n#@$.#\n#####")
        game.step_back(board)
        self.assertEqual(board["hero"], (1, 1))
        self.assertEqual(board["steps"], 0)


class ProgressTest(unittest.TestCase):
    def test_remaining_crates_ignores_goal_crates(self):
        board = game.new_board("######\n#@$*.#\n######")
        self.assertEqual(game.remaining_crates(board), 1)
        self.assertFalse(game.completed(board))

    def test_all_levels_are_solvable(self):
        self.assertEqual(len(game.MAP_TEXT), len(LEVEL_SOLUTIONS))
        for index, (level, solution) in enumerate(
            zip(game.MAP_TEXT, LEVEL_SOLUTIONS), start=1
        ):
            board = game.new_board(level)
            for key in solution:
                self.assertTrue(
                    game.apply_move(board, key), f"ステージ{index}の{key}で移動できない"
                )
            self.assertTrue(game.completed(board), f"ステージ{index}がクリアできない")


if __name__ == "__main__":
    unittest.main()
