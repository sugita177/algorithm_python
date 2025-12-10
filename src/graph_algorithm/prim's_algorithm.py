# プリム法
# mst : Minimum Spanning Tree（最小全域木）

import matplotlib.pyplot as plt
import networkx as nx
import sys  # 無限大 (sys.maxsize) を使用するため
from matplotlib.lines import Line2D  # Line2Dをインポート


# --- 日本語フォント設定 (環境に合わせて適宜調整してください) ---
plt.rcParams['font.family']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['font.sans-serif']\
      = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# ------------------------------------------------------------------

# --- グラフの定義 (サンプルデータ) ---
G = nx.Graph()
# ノードとエッジ: (ノードA, ノードB, 重み)
edges_with_weight = [
    ('A', 'B', 4), ('A', 'H', 8),
    ('B', 'C', 8), ('B', 'H', 11),
    ('C', 'D', 7), ('C', 'F', 4), ('C', 'I', 2),
    ('D', 'E', 9), ('D', 'F', 14),
    ('E', 'F', 10),
    ('F', 'G', 2),
    ('G', 'H', 1), ('G', 'I', 6),
    ('H', 'I', 7)
]
G.add_weighted_edges_from(edges_with_weight)
nodes = list(G.nodes)
num_nodes = len(nodes)
node_map = {node: i for i, node in enumerate(nodes)}  # ノード名 -> インデックス

# ノードの描画位置を固定
pos = nx.circular_layout(G)


def create_prim_legend(ax, current_step_is_final=False):
    """
    プリム法可視化用の凡例要素を作成し、軸に追加する
    """
    legend_elements = []

    # 1. ノードの凡例
    legend_elements.extend([
        Line2D([0], [0], marker='o', color='w', label='MST確定ノード',
               markersize=10, markerfacecolor='limegreen'),
        Line2D([0], [0], marker='o', color='w', label='現在選択中のノード',
               markersize=10, markerfacecolor='red'),
        Line2D([0], [0], marker='o', color='w', label='未選択ノード',
               markersize=10, markerfacecolor='skyblue')
    ])

    # 2. エッジの凡例
    legend_elements.extend([
        Line2D([0], [0], color='darkgreen', lw=3, label='MST確定エッジ'),
        Line2D([0], [0], color='red', lw=2, label='MST候補エッジ'),
        Line2D([0], [0], color='lightgray', lw=1, label='その他エッジ')
    ])

    # 凡例をグラフ描画エリアの右外側へ配置
    ax.legend(handles=legend_elements,
              loc='center left',
              bbox_to_anchor=(1.05, 0.5),  # 軸の右側に配置
              title="【プリム法 凡例】",
              fontsize=9,
              title_fontsize=10)


def draw_graph_step(
        G, mst_set, parent, key, current_u, process_type, pause_time=0.8):
    plt.cla()  # 軸(Axes)の中身だけをクリアする (Figure自体は残る)
    ax = plt.gca()

    # 1. ノードの色とラベルの設定
    node_colors = []
    node_labels = {}
    for node in nodes:
        i = node_map[node]
        k = key[i]
        p = parent[i]

        # 色の決定
        if node == current_u:
            node_colors.append('red')  # 🔴 現在選択中のノード
        elif node in mst_set:
            node_colors.append('limegreen')  # 🟢 MSTに含まれるノード
        else:
            node_colors.append('skyblue')  # 🔵 未選択のノード

        # ラベルの決定 (ノード名 + キー + 親)
        key_str = "∞" if k == sys.maxsize else str(k)
        parent_str = "" if p is None else f" (from {p})"
        node_labels[node] = f"{node}\nKey: {key_str}{parent_str}"

    # 2. エッジの色と太さの設定
    edge_colors = []
    edge_widths = []

    for u, v, data in G.edges(data=True):

        # MSTの決定済みエッジ
        if parent[node_map[u]] == v and u in mst_set:
            edge_colors.append('darkgreen')
            edge_widths.append(3)
        elif parent[node_map[v]] == u and v in mst_set:
            edge_colors.append('darkgreen')
            edge_widths.append(3)
        # MST候補のエッジ (現在選択中のノードに接続している未選択ノードへのエッジ)
        elif ((u == current_u and v not in mst_set)
              or (v == current_u and u not in mst_set)):
            edge_colors.append('red')
            edge_widths.append(2)
        else:
            edge_colors.append('lightgray')
            edge_widths.append(1)

    # グラフの描画
    nx.draw_networkx_nodes(
        G, pos, node_color=node_colors, node_size=2000, alpha=0.9, ax=ax)
    nx.draw_networkx_edges(
        G, pos, edge_color=edge_colors, width=edge_widths, ax=ax)
    nx.draw_networkx_labels(
        G, pos, labels=node_labels, font_size=10, font_color='black', ax=ax)

    # エッジの重みラベル描画
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color='darkgray', ax=ax)

    # --- 凡例の描画を追加 ---
    create_prim_legend(ax)
    # --------------------------

    # タイトル
    mst_nodes_str = ", ".join(sorted(list(mst_set)))
    plt.title(
        f"プリム法 (Prim's Algorithm) | {process_type}\n"
        f"MST Nodes: {{{mst_nodes_str}}}"
        )

    plt.axis('off')
    plt.tight_layout()
    plt.pause(pause_time)


def prim_visualized(G, start_node, pause_time=0.8):
    """
    プリム法の実行と可視化を行うメイン関数
    """
    nodes = list(G.nodes)
    num_nodes = len(nodes)
    node_map = {node: i for i, node in enumerate(nodes)}

    # 初期化:
    mst_set = set()  # MSTに含まれたノード
    key = [sys.maxsize] * num_nodes  # ノードの最小接続重み
    parent = [None] * num_nodes  # MSTエッジの親ノード

    start_index = node_map[start_node]
    key[start_index] = 0

    # 初期状態の描画
    draw_graph_step(G, mst_set, parent, key, start_node,
                    f"初期化: スタートノード '{start_node}' のキーを 0 に設定",
                    pause_time)

    # MST構築ループ
    for _ in range(num_nodes):

        # ----------------------------------------------------
        # 1. MSTに含まれていないノードの中で、最小キーのノード u を見つける
        # ----------------------------------------------------
        min_key = sys.maxsize
        u = None

        for node in nodes:
            i = node_map[node]
            if node not in mst_set and key[i] < min_key:
                min_key = key[i]
                u = node

        if u is None:
            break

        # ----------------------------------------------------
        # 2. ノード u をMSTに追加し、可視化
        # ----------------------------------------------------
        mst_set.add(u)

        u_index = node_map[u]
        parent_u = parent[u_index]
        process_str = f"選択: ノード '{u}' (Key:{min_key}) をMSTに追加"
        if parent_u is not None:
            process_str += f", エッジ ({parent_u}, {u}) をMSTに組み込む"

        draw_graph_step(G, mst_set, parent, key, u,
                        process_str, pause_time * 1.5)

        # ----------------------------------------------------
        # 3. 隣接ノード v のキーを更新
        # ----------------------------------------------------
        for v in G.neighbors(u):
            v_index = node_map[v]
            # v がまだMSTに含まれていない
            if v not in mst_set:
                weight = G.get_edge_data(u, v)['weight']

                # エッジの重みが現在の v のキーより小さいか
                if weight < key[v_index]:
                    key[v_index] = weight
                    parent[v_index] = u

                    # 更新ステップの可視化
                    draw_graph_step(G, mst_set, parent, key, u,
                                    f"キー更新: {u} -> {v} (重み:{weight}). "
                                    f"{v}のキーを {weight} に更新.", pause_time)

    # ----------------------------------------------------
    # 最終結果の表示
    # ----------------------------------------------------
    total_weight = 0
    mst_edges_list = []

    for i in range(num_nodes):
        u = nodes[i]
        p = parent[i]
        if p is not None:
            weight = G.get_edge_data(u, p)['weight']
            total_weight += weight
            mst_edges_list.append((u, p) if u < p else (p, u))

    mst_edges_str = "\n".join([f"({u}, {v}) "
                               f"(重み: {G.get_edge_data(u, v)['weight']})"
                               for u, v in sorted(list(set(mst_edges_list)))])

    print("\n--- プリム法 実行完了 ---")
    print(f"最小全域木の総重み: {total_weight}")
    print(f"最小全域木のエッジ:\n{mst_edges_str}")

    draw_graph_step(G, mst_set, parent, key, None,
                    f"完了: 最小全域木の総重み {total_weight}", pause_time * 3)
    plt.show()


# 実行
# --- ループに入る前に Figure を作成する ---
plt.figure(figsize=(12, 8))  # サイズを広げ、凡例が入るスペースを確保
plt.subplots_adjust(right=0.75)  # グラフ描画エリアを右端から75%の位置に制限
# --------------------------------------------------

prim_visualized(G, start_node='A', pause_time=2.0)
