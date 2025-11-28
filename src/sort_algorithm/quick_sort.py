# quick sort
# クイックソート

import matplotlib.pyplot as plt
import numpy as np

# --- 日本語フォント設定（前回成功した設定を再利用）---
plt.rcParams['font.family']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['font.sans-serif']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# --------------------------------------------------------


# データ配列を初期化
N = 30
data = np.random.randint(1, 100, N)


def draw_bars(arr, low, high, pivot_idx, current_idx, is_sorted=False):
    """
    棒グラフを描画するヘルパー関数
    """
    plt.clf()

    # 基本色を設定（未ソート部分はグレー、最終ソート済部分は緑）
    colors = ['gray'] * len(arr)

    # 探索範囲を薄いオレンジで強調
    for i in range(low, high + 1):
        colors[i] = 'lightcoral'

    # ピボットを赤で強調
    if low <= pivot_idx <= high:
        colors[pivot_idx] = 'red'

    # 現在のインデックス（パーティション中の比較対象）を青で強調
    if low <= current_idx <= high:
        colors[current_idx] = 'blue'

    # 完全にソート済みの要素を緑で強調
    if is_sorted:
        colors = ['limegreen'] * len(arr)

    plt.bar(range(len(arr)), arr, color=colors)
    plt.title(
        f"Quick Sort Visualization\n"
        f"Elements: {len(arr)} | Comparing: {current_idx}"
        )
    plt.xticks([])  # X軸のラベルは非表示
    plt.pause(0.1)  # 描画の一時停止 (アニメーション速度)


def quick_sort_visualized(arr, low, high):
    """
    クイックソートの本体（可視化ステップを含む）
    """
    if low < high:
        # パーティション実行
        p_idx = partition(arr, low, high)

        # パーティション後、ピボット位置で一度描画を停止
        draw_bars(arr, low, high, p_idx, -1)
        plt.pause(0.5)

        # 左側のサブ配列を再帰的にソート
        quick_sort_visualized(arr, low, p_idx - 1)

        # 右側のサブ配列を再帰的にソート
        quick_sort_visualized(arr, p_idx + 1, high)


def partition(arr, low, high):
    """
    パーティション操作（Lomutoパーティションスキームを使用）
    """
    pivot = arr[high]  # 配列の最後の要素をピボットとして選択
    i = low - 1  # 適切な位置に配置されるピボットのインデックス

    # ピボットの選択を可視化
    draw_bars(arr, low, high, high, -1)

    for j in range(low, high):
        # 現在比較中のインデックスを可視化
        draw_bars(arr, low, high, high, j)

        if arr[j] <= pivot:
            i += 1
            # スワップが発生した場合は可視化
            arr[i], arr[j] = arr[j], arr[i]
            draw_bars(arr, low, high, high, j)
            plt.pause(0.05)  # スワップが起こるたびに短いポーズ

    # ピボットを最終的な位置に配置
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    # ピボットが定位置に置かれた状態を可視化
    return i + 1


# 実行
plt.figure(figsize=(8, 5))
quick_sort_visualized(data, 0, N - 1)

# 最終ソート済みの状態を描画してウィンドウを保持
draw_bars(data, 0, 0, -1, -1, is_sorted=True)
plt.title("Quick Sort Completed")
plt.show()
