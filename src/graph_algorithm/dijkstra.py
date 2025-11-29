# ダイクストラ法

import networkx as nx
import matplotlib.pyplot as plt
import heapq  # 優先度付きキューを使用
# import math
# import time

# --- 日本語フォント設定（前回成功した設定を再利用）---
plt.rcParams['font.family']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['font.sans-serif']\
    = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# --------------------------------------------------------

# グラフを定義する（ノードと重み付きエッジ）
G = nx.Graph()
# (ノード1, ノード2, 重み)
edges_with_weights = [
    ('A', 'B', 4), ('A', 'C', 2),
    ('B', 'C', 5), ('B', 'D', 10),
    ('C', 'E', 3),
    ('D', 'F', 11),
    ('E', 'D', 4), ('E', 'F', 5)
]
G.add_weighted_edges_from(edges_with_weights)

# ノード配置の再現性を確保
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(8, 5))


def visualize_dijkstra(graph, start_node, pause_time=1.5):
    """
    ダイクストラ法のステップを可視化する関数
    """
    nodes = list(graph.nodes())

    # 1. 初期化
    # 距離のディクショナリ: 全て無限大で初期化
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0

    # 経路復元のためのディクショナリ
    predecessors = {node: None for node in nodes}

    # 確定済みノードのセット
    finalized_nodes = set()

    # 優先度付きキュー: (距離, ノード名)
    pq = [(0, start_node)]

    # 描画用: ノードとエッジの色の初期設定
    node_colors = ['lightgray'] * len(nodes)  # 'lightgray': 未確定/未到達
    node_color_map = {node: 'lightgray' for node in nodes}
    # edge_colors = ['gray'] * len(graph.edges)

    # 探索ステップカウンター
    step_counter = 1

    print(f"--- ダイクストラ法開始: 始点 '{start_node}' ---")

    while pq:
        # ----------------------------------------------------
        # STEP 1: 優先度付きキューから最小距離のノードを取り出す
        # ----------------------------------------------------

        # 最小距離のノードを取得
        current_dist, u = heapq.heappop(pq)

        # すでに確定済みならスキップ
        if u in finalized_nodes:
            continue

        # ----------------------------------------------------
        # STEP 2: 描画（処理対象ノードの強調）
        # ----------------------------------------------------

        plt.clf()

        # ノード u を赤で強調（現在処理中）
        node_color_map[u] = 'red'

        # ノードラベル (ノード名 + 距離) を更新
        node_labels = {}
        for node in nodes:
            dist_str = str(distances[node])\
                if distances[node] != float('inf') else '∞'
            node_labels[node] = f'{node}\n(距離: {dist_str})'

        # ノードの最終色リストを作成
        node_colors = [node_color_map[node] for node in nodes]

        nx.draw(
            graph, pos, with_labels=True, labels=node_labels,
            node_color=node_colors, node_size=3000,
            font_size=10, font_weight='bold',
            edge_color='gray'  # エッジ色はリセット
        )

        print(f"\n[STEP {step_counter}] 確定候補ノード: {u} (距離: {current_dist})")
        plt.title(f"Step {step_counter}: ノード '{u}' を処理中（距離確定）")

        plt.pause(pause_time)

        # ----------------------------------------------------
        # STEP 3: 距離の確定と緩和処理（Relaxation）
        # ----------------------------------------------------

        # ノード u の距離を確定
        finalized_nodes.add(u)
        node_color_map[u] = 'limegreen'  # 確定したノードは緑に

        relaxation_info = []

        # 隣接ノード v の距離を緩和
        for v, data in graph[u].items():
            weight = data['weight']
            new_dist = current_dist + weight

            # 緩和条件: より短い経路が見つかった場合
            if new_dist < distances[v]:
                old_dist = distances[v]
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(pq, (new_dist, v))

                # ノード v を黄色で強調（暫定距離更新）
                if v not in finalized_nodes:
                    node_color_map[v] = 'yellow'

                relaxation_info.append(
                    f"{u} -> {v} ({old_dist} -> {new_dist})"
                    )
                print(
                    f"   -> 緩和処理: {u} -> {v} (重み{weight})。"
                    f"距離を {old_dist} から {new_dist} に更新。"
                    )

            # ----------------------------------------------------
            # STEP 4: 緩和処理後の状態を描画（エッジの強調）
            # ----------------------------------------------------

            plt.clf()

            # エッジの色を更新: 現在緩和処理を行ったエッジをオレンジに強調
            temp_edge_colors = []
            for edge in graph.edges():
                is_in_relaxation\
                    = (edge[0] == u and edge[1] == v)\
                    or (edge[0] == v and edge[1] == u)
                if is_in_relaxation is True:
                    temp_edge_colors.append('orange')
                # 最短経路木の一部
                elif edge in _get_shortest_path_edges(predecessors):
                    temp_edge_colors.append('dodgerblue')
                else:
                    temp_edge_colors.append('gray')

            # ノードラベルを再作成（更新後の距離を反映）
            for node in nodes:
                dist_str = str(distances[node])\
                    if distances[node] != float('inf') else '∞'
                node_labels[node] = f'{node}\n(距離: {dist_str})'

            # ノードの最終色リストを作成
            node_colors = [node_color_map[node] for node in nodes]

            nx.draw(
                graph, pos, with_labels=True, labels=node_labels,
                node_color=node_colors, node_size=3000,
                font_size=10, font_weight='bold',
                edge_color=temp_edge_colors
            )

            if relaxation_info:
                plt.title(
                    f"Step {step_counter} (緩和処理): {', '.join(relaxation_info)}"
                    )
            else:
                plt.title(f"Step {step_counter}: ノード {u} は緩和処理なし")

            plt.pause(pause_time / 2)  # 緩和処理のステップは短めにポーズ

        step_counter += 1

    print("\n--- ダイクストラ法完了 ---")

    # ----------------------------------------------------
    # FINAL STEP: 最終結果の描画
    # ----------------------------------------------------
    plt.clf()

    # 最短経路木 (SPT) のエッジを青で強調
    spt_edges = _get_shortest_path_edges(predecessors)
    final_edge_colors\
        = ['dodgerblue' if edge in spt_edges or (edge[1], edge[0])
           in spt_edges else 'lightgray' for edge in graph.edges()]

    # 最終的なノードの色（全て確定なので緑）
    final_node_colors = ['limegreen'] * len(nodes)

    # 最終的なノードラベル
    for node in nodes:
        dist_str = str(distances[node])\
            if distances[node] != float('inf') else '∞'
        node_labels[node] = f'{node}\n(確定距離: {dist_str})'

    nx.draw(
        graph, pos, with_labels=True, labels=node_labels,
        node_color=final_node_colors, node_size=3000,
        font_size=10, font_weight='bold',
        edge_color=final_edge_colors
    )
    plt.title("ダイクストラ法 最終結果: 最短経路木")

    print("\n[最終的な最短距離]")
    for node in sorted(distances.keys()):
        dist_str = str(distances[node])\
            if distances[node] != float('inf') else '到達不可'
        print(f"ノード {node}: {dist_str}")

    plt.show()


def _get_shortest_path_edges(predecessors):
    """最短経路木のエッジリストを生成するヘルパー関数"""
    spt_edges = set()
    for node, pred in predecessors.items():
        if pred is not None:
            # エッジは(ノード, プレデシッサ)のタプルとして保存
            spt_edges.add(tuple(sorted((node, pred))))
    return spt_edges


# 実行（始点 'A' からスタート）
visualize_dijkstra(G, start_node='A', pause_time=3.0)
