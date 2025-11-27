# depth-first search
# 深さ優先探索

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque  # スタックの代わりとしてdequeを流用

# --- 日本語フォント設定（前回成功した設定を再利用）---
plt.rcParams['font.family']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['font.sans-serif']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# --------------------------------------------------------

# グラフを定義する（前回の例と同じグラフ構造）
G = nx.Graph()
edges = [
    ('A', 'B'), ('A', 'C'),
    ('B', 'D'), ('B', 'E'),
    ('C', 'F'), ('C', 'G'),
    ('D', 'H'),
    ('E', 'I')
]
G.add_edges_from(edges)

# ノード配置の再現性を確保
pos = nx.spring_layout(G, seed=42)

plt.figure()


def visualize_dfs(graph, start_node, pause_time=1.5):
    """
    深さ優先探索のステップを可視化する関数（スタック使用）
    - 探索順序とスタックの内容を表示
    """

    # 状態管理のための辞書
    node_status = {node: 'unvisited' for node in graph.nodes}
    exploration_order = {}
    exploration_counter = 1

    # DFSではキューの代わりにスタック（LIFO）を使用する
    # dequeを使い、append()とpop()でスタックとして動作させる
    stack = deque([start_node])
    node_status[start_node] = 'queued'  # スタックに追加された状態を'queued'として扱う

    color_map =\
        {'unvisited': 'lightgray', 'queued': 'skyblue', 'visited': 'limegreen'}

    print(f"--- DFS開始: 開始ノード '{start_node}' ---")

    while stack:

        # ----------------------------------------------------
        # STEP 1: 探索前の状態を描画（次に探索するノードを強調）
        # ----------------------------------------------------

        plt.clf()

        current_node_colors\
            = [color_map[node_status[node]] for node in graph.nodes]

        node_labels = {}
        for node in graph.nodes:
            label = node
            if node in exploration_order:
                label += f'\n({exploration_order[node]}番目)'
            node_labels[node] = label

        nx.draw(
            graph, pos, with_labels=True, labels=node_labels,
            node_color=current_node_colors, node_size=2500, font_size=10,
            font_weight='bold'
        )

        # スタックの内容を出力（キューではなくスタックとして表示）
        current_stack_list = list(stack)
        current_node_to_explore = stack[-1]  # スタックの末尾（LIFO）

        plt.title(
            f"Stack: {current_stack_list}\n"
            f"-> Next: {current_node_to_explore} を探索します"
        )

        print(f"\n[STEP {exploration_counter}] Stack: {current_stack_list}")
        print(f"   -> 次に探索: {current_node_to_explore}")

        plt.pause(pause_time)  # 1. 一時停止

        # ----------------------------------------------------
        # DFSのコア処理
        # ----------------------------------------------------

        # スタックから要素を取り出す（pop()で末尾の要素を取り出す＝LIFO）
        current_node = stack.pop()

        exploration_order[current_node] = exploration_counter
        exploration_counter += 1

        node_status[current_node] = 'visited'

        newly_stacked = []
        # DFSでは、隣接ノードをスタックに入れる順序が探索経路に影響を与えるため、
        # グラフのノード順（アルファベット順など）で処理します。
        # 逆順にスタックに入れると、次に探索されるのがアルファベット順になりますが、
        # ここではNetworkXのデフォルト順で処理します。

        # 降順で処理すると、次に探索されるのが昇順（A, B, C...）になる
        # 隣接ノードリストを先に取得する
        neighbors = list(graph.neighbors(current_node))

        # そのリストをソートしてループする
        for neighbor in sorted(neighbors, reverse=True):
            if node_status[neighbor] == 'unvisited':
                node_status[neighbor] = 'queued'
                stack.append(neighbor)
                newly_stacked.append(neighbor)

        # ----------------------------------------------------
        # STEP 2: 探索後の状態を描画
        # ----------------------------------------------------

        plt.clf()

        current_node_colors\
            = [color_map[node_status[node]] for node in graph.nodes]

        node_labels = {}
        for node in graph.nodes:
            label = node
            if node in exploration_order:
                label += f'\n({exploration_order[node]}番目)'
            node_labels[node] = label

        nx.draw(
            graph, pos, with_labels=True, labels=node_labels,
            node_color=current_node_colors, node_size=2500,
            font_size=10, font_weight='bold'
        )

        plt.title(
            f"Node '{current_node}' "
            f"Explored (Order: {exploration_order[current_node]})\n"
            f"Newly Stacked: {newly_stacked} | New Stack: {list(stack)}"
        )

        print(f"   -> 探索完了: {current_node} | 新規スタック追加: {newly_stacked}")

        plt.pause(pause_time)  # 2. 一時停止

    print("\n--- DFS完了 ---")

    sorted_order = sorted(exploration_order.items(), key=lambda item: item[1])
    print("\n[最終的な探索順序]")
    for node, order in sorted_order:
        print(f"ノード {node}: {order}番目")

    plt.show()


# 実行
visualize_dfs(G, start_node='A', pause_time=1.5)
