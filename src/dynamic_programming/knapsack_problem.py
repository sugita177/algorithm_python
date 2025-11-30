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

# DPテーブルの初期化 (最大価値を記録)
DP = np.zeros((N + 1, Capacity + 1), dtype=int)
# 選択を記録するテーブル: 'IN' (入れた) または 'OUT' (入れなかった)
CHOICE = np.full((N + 1, Capacity + 1), 'N/A', dtype=object)


def reconstruct_solution(N, W, CHOICE, items):
    """
    CHOICE配列を逆順にたどり、選ばれた品物を再構築する関数
    """
    current_capacity = W
    selected_items = []

    # N番目の品物から逆順にたどる
    for i in range(N, 0, -1):
        # i番目の品物を選んだかどうか
        decision = CHOICE[i, current_capacity]

        if decision == 'IN':
            # 選んでいた場合: 品物iを追加し、容量を減らす
            weight_i = items[i][0]
            value_i = items[i][1]
            selected_items.append(f"品物 {i} (W:{weight_i}, V:{value_i})")
            current_capacity -= weight_i
        # 'OUT'の場合、capacityはそのまま（i-1の行をたどる）

    # 選んだ品物を逆順に表示（インデックス順にするため）
    return selected_items[::-1]


def visualize_knapsack(items, W, DP, CHOICE, pause_time=0.5):
    """
    ナップサック問題のDPテーブル構築と解の記録を可視化する関数
    """
    N = len(items) - 1
    Capacity = W

    # 描画用の軸とヒートマップの初期設定
    fig, ax = plt.subplots(figsize=(Capacity + 3, N + 2))
    plt.subplots_adjust(right=0.75)  # 凡例スペースの確保

    # x軸とy軸のラベルを設定
    item_labels = [f"品物 {i}\n(W:{items[i][0]}, V:{items[i][1]})"
                   for i in range(N + 1)]

    ax.set_xlabel("ナップサック容量 (j)")
    ax.set_ylabel("品物 (i)")

    # 最大価値のスケールを固定 (0から最終的な最大価値まで)
    vmax = sum(item[1] for item in items)

    print(f"--- 0/1ナップサック問題開始: 容量W={W}, 品物数N={N} ---")

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

            # --- 描画のカスタマイズ ---
            ax.set_title(f"品物 {i} 処理中 - 容量 {j} | 品物 {i} "
                         f"(W:{weight_i}, V:{value_i})を考慮")

            # セルに数値を書き込む
            for row in range(N + 1):
                for col in range(Capacity + 1):
                    # 現在処理中のセルを赤枠で囲む
                    if row == i and col == j:
                        rect = Rectangle((col - 0.5, row - 0.5),
                                         1, 1, fill=False,
                                         edgecolor='red', linewidth=3)
                        ax.add_patch(rect)
                        text_color = 'red'
                    else:
                        text_color = 'black'

                    ax.text(col, row, f"{DP[row, col]}",
                            ha="center", va="center",
                            color=text_color, fontsize=12)

            plt.xticks(np.arange(Capacity + 1), np.arange(Capacity + 1))
            plt.yticks(np.arange(N + 1), item_labels)
            ax.set_xlabel("ナップサック容量 (j)")
            ax.set_ylabel("品物 (i)")

            plt.pause(pause_time / 2)  # 短めのポーズ

            # ----------------------------------------------------
            # STEP 2: DP遷移の計算と選択の記録
            # ----------------------------------------------------

            # (1) 品物 i を入れない場合 (上の行の同じ容量の値)
            value_not_included = DP[i - 1, j]
            choice = 'OUT'

            # (2) 品物 i を入れる場合
            if j >= weight_i:
                # i-1番目までで、残りの容量 (j - weight_i) での最大価値 + 品物 i の価値
                value_included = DP[i - 1, j - weight_i] + value_i

                if value_included > value_not_included:
                    # 入れた方が価値が高い場合
                    DP[i, j] = value_included
                    choice = 'IN'
                else:
                    # 入れなかった方が価値が高い、または同じ場合
                    DP[i, j] = value_not_included
                    choice = 'OUT'
            else:
                # 容量が足りない場合は入れられない
                DP[i, j] = value_not_included
                choice = 'OUT_CAP'  # 容量不足による「入れない」

            # 決定を記録
            CHOICE[i, j] = choice
            print(f"   -> 容量 {j}: 選択: {choice} (Value: {DP[i, j]})")

            # ----------------------------------------------------
            # STEP 3: 更新後の状態を描画（青枠と選択肢ラベル）
            # ----------------------------------------------------

            plt.clf()
            ax = plt.gca()

            im = ax.imshow(DP, cmap="Blues", vmin=0, vmax=vmax)

            # セルに数値を書き込む (更新後の値 + 選択肢ラベル)
            for row in range(N + 1):
                for col in range(Capacity + 1):

                    text = f"{DP[row, col]}"
                    text_color = 'black'

                    # 更新されたセルを強調
                    if row == i and col == j:
                        rect = Rectangle((col - 0.5, row - 0.5), 1, 1,
                                         fill=False, edgecolor='blue',
                                         linewidth=3)
                        ax.add_patch(rect)
                        text_color = 'blue'
                        # 選択肢をセル内に小さく表示
                        choice_label = CHOICE[row, col]
                        if choice_label == 'OUT_CAP':
                            choice_label = 'OUT(Cap)'
                        text += f"\n({choice_label})"

                    ax.text(col, row, text, ha="center", va="center",
                            color=text_color, fontsize=10)

            plt.xticks(np.arange(Capacity + 1), np.arange(Capacity + 1))
            plt.yticks(np.arange(N + 1), item_labels)

            # 凡例として選択肢を表示
            ax.text(1.05, 0.95,
                    "【選択肢】\nIN: 入れた\nOUT: 入れなかった\nOUT(Cap): 容量不足",
                    transform=ax.transAxes,
                    fontsize=10,
                    verticalalignment='top',
                    bbox=dict(boxstyle="round,pad=0.5",
                              fc="white", alpha=0.8, ec="black"))

            ax.set_title(f"品物 {i} 処理完了 - 容量 {j} | 決定: {CHOICE[i, j]}")
            ax.set_xlabel("ナップサック容量 (j)")
            ax.set_ylabel("品物 (i)")

            plt.pause(pause_time)

    # ----------------------------------------------------
    # FINAL STEP: 最終結果の表示と解の再構築 (トレースバック)
    # ----------------------------------------------------
    plt.clf()
    ax = plt.gca()
    im = ax.imshow(DP, cmap="Greens", vmin=0, vmax=vmax)

    # 最終的な解の再構築を実行
    final_solution = reconstruct_solution(N, Capacity, CHOICE, items)

    # セルに数値と選択肢を書き込む
    for row in range(N + 1):
        for col in range(Capacity + 1):
            text = f"{DP[row, col]}"
            choice_label = CHOICE[row, col]
            if choice_label == 'OUT_CAP':
                choice_label = 'OUT(Cap)'

            # 最終セルの強調
            if row == N and col == Capacity:
                rect = Rectangle((col - 0.5, row - 0.5),
                                 1, 1, fill=False,
                                 edgecolor='red', linewidth=4)
                ax.add_patch(rect)

            if choice_label != 'N/A':
                text += f"\n({choice_label})"
            ax.text(col, row, text, ha="center",
                    va="center", color='black', fontsize=10)

    plt.xticks(np.arange(Capacity + 1), np.arange(Capacity + 1))
    plt.yticks(np.arange(N + 1), item_labels)

    solution_text = "\n".join(final_solution) if final_solution else "なし"

    # 最終結果のサマリーをグラフの右側に表示
    ax.text(1.05, 0.95,
            f"【最終解 (トレースバック)】\n"
            f"最大価値: {DP[N, Capacity]}\n"
            f"容量 {W} の\nナップサックに選ばれた品物:\n"
            f"{solution_text}",
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.5",
                      fc="white", alpha=0.9, ec="black"))

    ax.set_title(f"DPテーブル構築完了 | 最大価値: {DP[N, Capacity]}")
    plt.show()


# 実行
visualize_knapsack(items, W, DP, CHOICE, pause_time=0.5)
