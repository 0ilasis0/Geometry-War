from py.a_star.manage import a_star_mg
from py.a_star.variable import PositionSamePath
from py.debug import dbg
from py.variable import GridPoint


def print_map_with_path(grid_data, path, start, end):
    """
    grid_data: GridMapData 物件
    path: list[GridPoint]
    """
    print(f"--- 地圖與路徑預覽 ({grid_data.width},{grid_data.height}) ---")

    width = grid_data.width
    height = grid_data.height

    # 假設 path 裡是 GridPoint 物件
    path_set = {(p.col, p.row) for p in path} if path else set()

    for row in range(height):
        line = ""
        for col in range(width):
            # 這裡不需要每格都 new 一個 GridPoint 物件，太浪費效能
            # 計算 1D 索引
            idx = row * width + col
            is_wall = grid_data.collision_map[idx] == 1

            if col == start.col and row == start.row:
                line += "\033[92mS \033[0m" # 綠色 S
            elif col == end.col and row == end.row:
                line += "\033[91mE \033[0m" # 紅色 E
            elif (col, row) in path_set:
                line += "\033[93m* \033[0m" # 黃色 * (路徑)
            elif is_wall:
                line += "\033[90m# \033[0m" # 灰色 # (牆壁)
            else:
                line += ". " # 空地
        print(line)

def main_a_star(grid_data, start_pos: GridPoint, end_pos: GridPoint, map_tag: str):
    '''
    地圖 (0 = 路, 1 = 牆)
    map_data:路徑地圖
    start_pos:起點
    end_pos:終點
    map_name:該地圖名稱
    return:最短路徑經過座標
    '''
    # 檢查是否已經計算過此地圖的此路徑
    path_key = PositionSamePath(map_tag, start_pos, end_pos)
    if path_key in a_star_mg.store_paths:
        return a_star_mg.store_paths[path_key]

    # 更新 C 端地圖數據，確保牆壁資料是最新的
    a_star_mg.update_map_from_grid_data(grid_data, map_tag)

    raw_path = a_star_mg.inf.find_path(a_star_mg, start_pos, end_pos)
    final_path = []

    if raw_path:
        final_path = [GridPoint(p[0], p[1]) for p in raw_path]

    if final_path:
        a_star_mg.store_paths[path_key] = final_path

        # if dbg.enable:
        #     print(f"請求路徑: {start_pos} -> {end_pos}")
        #     print(f"路徑長度: {len(final_path)} 步")
        #     print(f"路徑節點: {final_path}")
        #     print_map_with_path(grid_data, final_path, start_pos, end_pos)
    else:
        dbg.error("找不到路徑 (或是發生錯誤)")

    return final_path
