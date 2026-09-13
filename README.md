# 找貓

手機遊戲「找貓」（Queens / Star Battle 類型）的解題器。

## 規則

1. 每種顏色區域恰好一隻貓
2. 每行、每列恰好一隻貓
3. 貓咪不能相鄰（包含斜角的八個方向）

## 使用方式

需要 Python 3，沒有其他相依套件。

```bash
python3 cat_solver.py puzzles/level25.txt
```

輸出：

```
唯一解

--- 解 1 ---
G G G G 🐱 B B B B B
R 🐱 T G G G G G B B
T T T 🐱 G M M B B B
T T Y L G M B 🐱 D B
Y Y Y L L 🐱 B D D D
Y L 🐱 L M M B B D D
Y L Y L M L 🐱 L D D
Y L L L L L D D 🐱 D
🐱 L L L L L D D D O
L L D D D D D D D 🐱
貓咪位置 (列, 欄)，從 1 開始：
(1, 5), (2, 2), (3, 4), (4, 8), (5, 6), (6, 3), (7, 7), (8, 9), (9, 1), (10, 10)
```

加上 `--all` 會列出所有解，可用來檢查題目是否唯一解。

## 盤面格式

純文字檔，每行一列，每格一個字元代表顏色，`#` 開頭的行是註解。
盤面必須是正方形，顏色種類數要等於邊長。範例見 `puzzles/level25.txt`。

## 解法

回溯法（backtracking）：逐列嘗試放貓，只保留欄未用、顏色未用、
且不與上一列的貓相鄰的位置，走不通就退回。10×10 的盤面瞬間完成。
