#!/usr/bin/env python3
"""找貓解題器 (Queens / Star Battle 類型謎題)

規則：
  1. 每種顏色區域恰好一隻貓
  2. 每行、每列恰好一隻貓
  3. 貓咪不能相鄰（包含斜角的八個方向）

盤面格式：純文字，每行一列，每格一個字元代表顏色，
'#' 開頭的行是註解，空白行會被忽略。例如 4x4：

    AABB
    ACBB
    CCDD
    CCDD

用法：
    python3 cat_solver.py puzzles/level25.txt
    cat puzzles/level25.txt | python3 cat_solver.py
    python3 cat_solver.py puzzles/level25.txt --all   # 列出所有解（預設最多找 2 組，用來判斷唯一解）
"""
import sys
from typing import List, Tuple

Board = List[str]
Solution = List[Tuple[int, int]]  # [(row, col), ...] 每列一隻貓


def parse_board(text: str) -> Board:
    rows = [line.strip() for line in text.splitlines()]
    rows = [r for r in rows if r and not r.startswith("#")]
    if not rows:
        raise ValueError("盤面是空的")
    n = len(rows)
    for i, r in enumerate(rows):
        if len(r) != n:
            raise ValueError(f"第 {i + 1} 列有 {len(r)} 格，但盤面有 {n} 列，必須是正方形")
    colors = {c for r in rows for c in r}
    if len(colors) != n:
        raise ValueError(f"盤面有 {n} 列，但顏色只有 {len(colors)} 種，兩者必須相等")
    return rows


def solve(board: Board, limit: int = 2) -> List[Solution]:
    """回溯法：逐列放貓，找到 limit 組解就停（limit=0 表示找全部）。"""
    n = len(board)
    solutions: List[Solution] = []
    used_cols = set()
    used_colors = set()
    placed: Solution = []

    def backtrack(row: int) -> bool:
        if row == n:
            solutions.append(list(placed))
            return limit != 0 and len(solutions) >= limit
        for col in range(n):
            color = board[row][col]
            if col in used_cols or color in used_colors:
                continue
            # 只需檢查上一列：同列已由 used_cols 排除，斜角相鄰只會發生在相鄰的列
            if placed and abs(placed[-1][1] - col) <= 1:
                continue
            placed.append((row, col))
            used_cols.add(col)
            used_colors.add(color)
            if backtrack(row + 1):
                return True
            placed.pop()
            used_cols.discard(col)
            used_colors.discard(color)
        return False

    backtrack(0)
    return solutions


def render(board: Board, solution: Solution, cat: str = "🐱") -> str:
    cells = set(solution)
    n = len(board)
    return "\n".join(
        " ".join(cat if (r, c) in cells else board[r][c] for c in range(n))
        for r in range(n)
    )


def main(argv: List[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    find_all = "--all" in argv
    text = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()

    try:
        board = parse_board(text)
    except ValueError as e:
        print(f"盤面格式錯誤：{e}", file=sys.stderr)
        return 2

    solutions = solve(board, limit=0 if find_all else 2)
    if not solutions:
        print("無解")
        return 1

    if find_all:
        print(f"共 {len(solutions)} 組解")
    elif len(solutions) == 1:
        print("唯一解")
    else:
        print("解不唯一（至少 2 組），以下列出前 2 組")

    for i, sol in enumerate(solutions, 1):
        print(f"\n--- 解 {i} ---")
        print(render(board, sol))
        print("貓咪位置 (列, 欄)，從 1 開始：")
        print(", ".join(f"({r + 1}, {c + 1})" for r, c in sol))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
