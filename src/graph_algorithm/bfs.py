# breadth-first search
# 幅優先探索

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# --- 日本語フォント設定の強化 ---
try:
    # 広く使われる日本語フォントを複数指定して試す
    plt.rcParams['font.family']\
        = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
    # CJK文字のフォールバックを可能にする
    plt.rcParams['font.sans-serif']\
        = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
    # マイナス記号などが文字化けしないように設定
    plt.rcParams['axes.unicode_minus'] = False
except Exception as e:
    # フォントが見つからない場合のフォールバック処理 (念のため)
    print(f"Warning: Failed to set Japanese font settings. Error: {e}")
# ----------------------------------

# グラフを定義する（複雑すぎず、経路が見やすい例）
G = nx.Graph()
edges = [
    ('A', 'B'), ('A', 'C'),
    ('B', 'D'), ('B', 'E'),
    ('C', 'F'), ('C', 'G'),
    ('D', 'H'),
    ('E', 'I')
]
G.add_edges_from(edges)

# 描画位置を固定する（アニメーションでノードが動かないように）
# ノード配置の再現性を確保するため、'spring_layout' を使用し 'seed' を指定
pos = nx.spring_layout(G, seed=42)


def visualize_bfs(graph, start_node, pause_time=1.5):
    """
    幅優先探索のステップを可視化する関数
    - 探索順序とキューの内容を表示
    - 一時停止時間を指定可能
    """

    # 状態管理のための辞書
    # 'unvisited': 未探索, 'queued': キューに追加済み, 'visited': 探索完了
    node_status = {node: 'unvisited' for node in graph.nodes}

    # 1. 探索順序を記録する辞書とカウンター
    exploration_order = {}
    exploration_counter = 1

    # キューの初期化
    queue = deque([start_node])
    node_status[start_node] = 'queued'

    # 描画設定（ノードの色とラベル）
    color_map = {
        'unvisited': 'lightgray', 'queued': 'skyblue', 'visited': 'limegreen'
        }

    print(f"--- BFS開始: 開始ノード '{start_node}' ---")

    # 描画ループ
    while queue:

        # ----------------------------------------------------
        # STEP 1: 探索前の状態を描画（次に探索するノードを強調）
        # ----------------------------------------------------

        plt.clf()  # 前の描画をクリア

        # 現在の状態を基にノードの色リストを作成
        current_node_colors = [
            color_map[node_status[node]] for node in graph.nodes
            ]

        # ノードラベルを更新: ノード名 + (探索順序)
        node_labels = {}
        for node in graph.nodes:
            label = node
            if node in exploration_order:
                # 探索済みのノードには順序番号を付与
                label += f'\n({exploration_order[node]}番目)'
            node_labels[node] = label

        # グラフを描画
        nx.draw(
            graph,
            pos,
            with_labels=True,
            labels=node_labels,
            node_color=current_node_colors,
            node_size=2500,  # 見やすいようにサイズを調整
            font_size=10,
            font_weight='bold'
        )

        # 2. 現在のキューに格納されているノードを出力
        current_queue_list = list(queue)
        current_node_to_explore = queue[0]

        plt.title(
            f"Queue: {current_queue_list}\n"
            f"-> Next: {current_node_to_explore} を探索します"
        )

        print(f"\n[STEP {exploration_counter}] Queue: {current_queue_list}")
        print(f"   -> 次に探索: {current_node_to_explore}")

        # 3. 一時停止
        plt.pause(pause_time)

        # ----------------------------------------------------
        # BFSのコア処理（ノードの探索を実行）
        # ----------------------------------------------------

        current_node = queue.popleft()

        # 1. 探索順序を記録
        exploration_order[current_node] = exploration_counter
        exploration_counter += 1

        # 探索完了としてマーク
        node_status[current_node] = 'visited'

        # 隣接ノードをチェックし、キューに追加
        newly_queued = []
        for neighbor in graph.neighbors(current_node):
            if node_status[neighbor] == 'unvisited':
                node_status[neighbor] = 'queued'
                queue.append(neighbor)
                newly_queued.append(neighbor)

        # ----------------------------------------------------
        # STEP 2: 探索後の状態を描画（探索完了とキューの更新を表示）
        # ----------------------------------------------------

        plt.clf()  # 前の描画をクリア

        # 状態とラベルを更新して再描画
        current_node_colors = [
            color_map[node_status[node]] for node in graph.nodes
            ]

        # ノードラベルを更新
        node_labels = {}
        for node in graph.nodes:
            label = node
            if node in exploration_order:
                label += f'\n({exploration_order[node]}番目)'
            node_labels[node] = label

        nx.draw(
            graph,
            pos,
            with_labels=True,
            labels=node_labels,
            node_color=current_node_colors,
            node_size=2500,
            font_size=10,
            font_weight='bold'
        )

        # 2. キューの内容を出力 (探索後のキュー)
        plt.title(
            f"Node '{current_node}' " +
            f"Explored (Order: {exploration_order[current_node]})\n"
            f"Newly Queued: {newly_queued} | New Queue: {list(queue)}"
        )

        print(f"   -> 探索完了: {current_node} | 新規キュー追加: {newly_queued}")

        # 3. 一時停止
        plt.pause(pause_time)  # 1ノードの探索後の間

    print("\n--- BFS完了 ---")

    # 最終的な探索順序をまとめて表示
    sorted_order = sorted(exploration_order.items(), key=lambda item: item[1])
    print("\n[最終的な探索順序]")
    for node, order in sorted_order:
        print(f"ノード {node}: {order}番目")

    # アニメーション終了後、グラフウィンドウを表示したままにする
    # ループ内で表示した最終フレームがこの命令により画面に残り続けます。
    plt.show()


# 実行（一時停止時間を1.5秒に設定）
visualize_bfs(G, start_node='A', pause_time=1.5)
