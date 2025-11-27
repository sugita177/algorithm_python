# breadth-first search
# 幅優先探索

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
# import time # アニメーションの進行を遅らせるために使用

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
pos = nx.spring_layout(G, seed=42)


def visualize_bfs(graph, start_node):
    """
    幅優先探索のステップを可視化する関数
    """

    # 状態管理のための辞書
    # 'unvisited': 未探索, 'queued': キューに追加済み, 'visited': 探索完了
    node_status = {node: 'unvisited' for node in graph.nodes}

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

        # 描画の準備
        plt.clf()  # 前の描画をクリア

        # 現在の状態を基にノードの色リストを作成
        current_node_colors = [
            color_map[node_status[node]] for node in graph.nodes
            ]

        # グラフを描画
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_color=current_node_colors,
            node_size=1500,
            font_size=10,
            font_weight='bold'
        )

        # タイトルに現在のステップ情報を表示
        plt.title(f"BFS Step - Queue: {list(queue)}")

        plt.pause(1.0)  # 1秒間表示を一時停止 (アニメーション効果)

        # --- BFSのコア処理 ---
        current_node = queue.popleft()

        print(f"探索中ノード: {current_node}")

        # 探索完了としてマーク
        node_status[current_node] = 'visited'

        # 隣接ノードをチェック
        for neighbor in graph.neighbors(current_node):
            if node_status[neighbor] == 'unvisited':
                node_status[neighbor] = 'queued'
                queue.append(neighbor)

    print("--- BFS完了 ---")
    plt.close()


# 実行
visualize_bfs(G, start_node='A')
