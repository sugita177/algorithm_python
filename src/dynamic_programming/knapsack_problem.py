# ナップサック問題
# 動的計画法

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# --- 日本語フォント設定 ---
plt.rcParams['font.family']\
    = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['font.sans-serif']\
    = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# -------------------------

# 品物の定義: (重さ, 価値) のリスト
# 0番目はダミーとして空けておく
items = [(0, 0), (2, 3), (3, 4), (4, 5), (5, 8)]
W = 7  # ナップサックの最大容量

# 品物の数と容量
N = len(items) - 1
Capacity = W

# DPテーブルの初期化 (N+1 行, Capacity+1 列)
DP = np.zeros((N + 1, Capacity + 1), dtype=int)


def visualize_knapsack(items, W, DP, pause_time=0.5):
    """
    0/1ナップサック問題のDPテーブル構築を可視化する関数
    """
    N = len(items) - 1
    Capacity = W

    # 描画用の軸とヒートマップの初期設定
    fig, ax = plt.subplots(figsize=(Capacity + 2, N + 2))

    # x軸とy軸のラベルを設定
    ax.set_xticks(np.arange(Capacity + 1))
    ax.set_yticks(np.arange(N + 1))
    ax.set_xticklabels(np.arange(Capacity + 1))

    # 品物名のラベルを設定
    item_labels = [f"品物 {i}\n(W:{items[i][0]}, V:{items[i][1]})"
                   for i in range(N + 1)]
    ax.set_yticklabels(item_labels)

    ax.set_xlabel("ナップサック容量 (j)")
    ax.set_ylabel("品物 (i)")

    print(f"--- 0/1ナップサック問題開始: 容量W={W}, 品物数N={N} ---")

    # 最大価値のスケールを固定 (0から最終的な最大価値まで)
    vmax = sum(item[1] for item in items)

    # DPテーブルの構築
    for i in range(1, N + 1):
        weight_i = items[i][0]
        value_i = items[i][1]

        print(f"\n[品物 {i} 処理開始] (W:{weight_i}, V:{value_i})")

        for j in range(1, Capacity + 1):

            # ----------------------------------------------------
            # STEP 1: 計算前の状態を描画（処理中セルをハイライト）
            # ----------------------------------------------------

            plt.clf()
            ax = plt.gca()

            # ヒートマップ描画 (vmin=0, vmax=最大価値でスケール固定)
            im = ax.imshow(DP, cmap="Blues", vmin=0, vmax=vmax)

            # カラーバーの追加 (一度だけ)
            if i == 1 and j == 1:
                fig.colorbar(im, ax=ax, label='最大価値')

            ax.set_title(f"品物 {i}/{N} 処理中 - 容量 {j}/{Capacity}")

            # セルに数値を書き込む
            for row in range(N + 1):
                for col in range(Capacity + 1):
                    # 現在処理中のセルを赤枠で囲む
                    if row == i and col == j:
                        rect = Rectangle((col - 0.5, row - 0.5),
                                         1, 1, fill=False, edgecolor='red',
                                         linewidth=3)
                        ax.add_patch(rect)
                        text_color = 'red'
                    else:
                        text_color = 'black'

                    ax.text(col, row, f"{DP[row, col]}", ha="center",
                            va="center", color=text_color, fontsize=12)

            plt.xticks(np.arange(Capacity + 1), np.arange(Capacity + 1))
            plt.yticks(np.arange(N + 1), item_labels)
            ax.set_xlabel("ナップサック容量 (j)")
            ax.set_ylabel("品物 (i)")

            plt.pause(pause_time / 2)  # 短めのポーズ

            # ----------------------------------------------------
            # STEP 2: DP遷移の計算
            # ----------------------------------------------------

            # (1) 品物 i を入れない場合 (上の行の同じ容量の値)
            value_not_included = DP[i - 1, j]

            # (2) 品物 i を入れる場合
            if j >= weight_i:
                # i-1番目までで、残りの容量 (j - weight_i) での最大価値 + 品物 i の価値
                value_included = DP[i - 1, j - weight_i] + value_i

                # 最終的な最大価値を決定
                DP[i, j] = max(value_not_included, value_included)

                choice = "入れた" if DP[i, j] == value_included else "入れなかった"
                print(f"   -> 容量 {j}: {i}を{choice} (Value: {DP[i, j]})")
            else:
                # 容量が足りない場合は入れられない
                DP[i, j] = value_not_included
                print(f"   -> 容量 {j}: 容量不足のため入れなかった (Value: {DP[i, j]})")

            # ----------------------------------------------------
            # STEP 3: 更新後の状態を描画
            # ----------------------------------------------------

            plt.clf()
            ax = plt.gca()

            im = ax.imshow(DP, cmap="Blues", vmin=0, vmax=vmax)

            # セルに数値を書き込む (更新後の値)
            for row in range(N + 1):
                for col in range(Capacity + 1):
                    # 更新されたセルを強調
                    if row == i and col == j:
                        rect = Rectangle((col - 0.5, row - 0.5),
                                         1, 1, fill=False, edgecolor='blue',
                                         linewidth=3)
                        ax.add_patch(rect)
                        text_color = 'blue'
                    else:
                        text_color = 'black'

                    ax.text(col, row, f"{DP[row, col]}", ha="center",
                            va="center", color=text_color, fontsize=12)

            plt.xticks(np.arange(Capacity + 1), np.arange(Capacity + 1))
            plt.yticks(np.arange(N + 1), item_labels)
            ax.set_title(f"品物 {i}/{N} 処理完了 - 容量 {j}/{Capacity}")
            ax.set_xlabel("ナップサック容量 (j)")
            ax.set_ylabel("品物 (i)")

            plt.pause(pause_time)  # 計算後のポーズ

    # ----------------------------------------------------
    # FINAL STEP: 最終結果の表示
    # ----------------------------------------------------
    plt.clf()
    ax = plt.gca()
    im = ax.imshow(DP, cmap="Greens", vmin=0, vmax=vmax)  # 最終結果を緑色で表示

    for row in range(N + 1):
        for col in range(Capacity + 1):
            ax.text(col, row, f"{DP[row, col]}",
                    ha="center", va="center", color='black', fontsize=12)

    plt.xticks(np.arange(Capacity + 1), np.arange(Capacity + 1))
    plt.yticks(np.arange(N + 1), item_labels)
    ax.set_title(f"DPテーブル構築完了 | 最大価値: {DP[N, Capacity]}")
    ax.set_xlabel("ナップサック容量 (j)")
    ax.set_ylabel("品物 (i)")

    print("\n--- 最終結果 ---")
    print(f"DPテーブルの最終値:\n{DP}")
    print(f"最大容量 {W} での最大価値: {DP[N, Capacity]}")

    plt.show()


# 実行
visualize_knapsack(items, W, DP, pause_time=0.5)
