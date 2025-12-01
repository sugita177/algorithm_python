# merge sort
# マージソート

import matplotlib.pyplot as plt
import numpy as np

# --- 日本語フォント設定 ---
plt.rcParams['font.family']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['font.sans-serif']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# -------------------------

# データ配列の初期化
N = 30
data = np.random.randint(1, 100, N)


def draw_bars(arr, current_range, highlight_indices=None, process=""):
    """
    棒グラフを描画するヘルパー関数
    """
    plt.clf()

    colors = ['gray'] * len(arr)

    # 現在処理中の範囲を強調
    start, end = current_range
    for i in range(start, end):
        colors[i] = 'skyblue'

    # ハイライトインデックスを強調 (例: 併合中の要素)
    if highlight_indices:
        for idx in highlight_indices:
            if start <= idx < end:
                colors[idx] = 'red'

    # 最終ソート済みを緑に (プロセスが完了している場合)
    if process == "完了":
        colors = ['limegreen'] * len(arr)

    plt.bar(range(len(arr)), arr, color=colors)
    plt.title("Merge Sort Visualization | "
              f"Process: {process}\nRange: [{start} - {end}]")
    plt.xticks([])  # X軸のラベルは非表示
    plt.ylim(0, 105)  # Y軸の範囲を固定
    plt.pause(0.1)


def merge_sort_visualized(arr, low, high):
    """
    マージソートの本体（可視化ステップを含む）
    """
    if low < high:
        mid = (low + high) // 2

        # 1. 分割の可視化 (左側)
        draw_bars(arr, (low, mid + 1), process="分割 (左側へ)")
        plt.pause(0.2)

        # 左側の再帰呼び出し
        merge_sort_visualized(arr, low, mid)

        # 1. 分割の可視化 (右側)
        draw_bars(arr, (mid + 1, high + 1), process="分割 (右側へ)")
        plt.pause(0.2)

        # 右側の再帰呼び出し
        merge_sort_visualized(arr, mid + 1, high)

        # 2. 併合の実行と可視化
        merge(arr, low, mid, high)


def merge(arr, low, mid, high):
    """
    併合操作（修正版: 範囲外の要素を保護し、インデックスのズレを解消）
    """
    # 処理範囲を一時的にコピーする (マージ後に arr[low:high+1] に書き戻す)
    # L と R の要素数を正しく定義
    L = arr[low: mid + 1].tolist()  # リストに変換して操作しやすくする
    R = arr[mid + 1: high + 1].tolist()

    n1 = len(L)
    n2 = len(R)

    i = 0  # Lのインデックス
    j = 0  # Rのインデックス
    k = low  # arrの書き込み開始インデックス

    # LとRを比較しながら、arrの正しい位置にマージ
    while i < n1 and j < n2:
        highlight_indices = [low + i, mid + 1 + j]
        draw_bars(arr, (low, high + 1), highlight_indices, process="併合中 (比較)")
        plt.pause(0.05)

        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1

        # arr[k]に要素が移動したことを可視化
        draw_bars(arr, (low, high + 1), [k], process="併合中 (移動)")
        plt.pause(0.05)

        k += 1

    # 残りの要素をコピー (ここが最も重要)
    # Lに残っている要素を、arrの残りの位置にコピー
    while i < n1:
        arr[k] = L[i]
        i += 1
        draw_bars(arr, (low, high + 1), [k], process="併合中 (残りを移動)")
        plt.pause(0.05)
        k += 1

    # Rに残っている要素を、arrの残りの位置にコピー
    while j < n2:
        arr[k] = R[j]
        j += 1
        draw_bars(arr, (low, high + 1), [k], process="併合中 (残りを移動)")
        plt.pause(0.05)
        k += 1

    # 併合完了後の範囲を可視化
    draw_bars(arr, (low, high + 1), process="併合完了")
    plt.pause(0.3)


# 実行
plt.figure(figsize=(12, 6))
print(f"--- マージソート開始: 要素数 {N} ---")
print(f"初期配列: {data}")

merge_sort_visualized(data, 0, N - 1)

# 最終ソート済みの状態を描画してウィンドウを保持
draw_bars(data, (0, N), process="完了")
plt.title(f"Merge Sort Completed | Sorted Array: {data}")
plt.show()
