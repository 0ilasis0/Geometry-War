#include <stdbool.h>
#include <stdlib.h>
#include "c_inc/a_star/base.h"
#include "c_inc/a_star/main.h"
#include "c_inc/debug.h"



// --- 通用型 A* 函式 ---
// 參數說明:
// map: 地圖數據 (0 = 路, 1 = 牆)
// width, height: 地圖寬高
// start_x, start_y: 起點
// end_x, end_y: 終點
// out_buffer: 用來存結果的陣列 [x0, y0, x1, y1...]
// 回傳值: 路徑的節點數量 (若無路徑回傳 -1)
int solve_astar(
    const FORM_MAP* map ,
    FORM_W_H width      , FORM_W_H height,
    FORM_POINT start_x  , FORM_POINT start_y,
    FORM_POINT end_x    , FORM_POINT end_y,
    FORM_OUT_BUFFER* out_buffer
) {
    // 動態配置 Node 陣列
    Node* nodes = (Node*)malloc(width * height * sizeof(Node));
    if (!nodes){
        DBG_ERR("Insufficient memory");
        return -1;
    }

    // 初始化
    for (uint32_t i = 0; i < width * height; i++) {
        nodes[i].state = NONE;
        nodes[i].parent = (Point){-1, -1};
    }

    // 設定起點
    FORM_LEN start_idx = get_index(start_x, start_y, width);
    nodes[start_idx].g = 0;
    nodes[start_idx].h = calc_h(start_x, start_y, end_x, end_y);
    nodes[start_idx].f = nodes[start_idx].g + nodes[start_idx].h;
    nodes[start_idx].state = OPEN;

    bool found = false;

    while (true) {
        // 尋找 Open List 中 F 最小的節點
        int min_f = 999999999; // MAX_INT
        Node* current = NULL;
        Point current_pos = {-1, -1};
        FORM_POINT current_idx = -1;

        for (FORM_POINT y = 0; y < height; y++) {
            for (FORM_POINT x = 0; x < width; x++) {
                FORM_POINT idx = get_index(x, y, width);
                if (nodes[idx].state == OPEN) {
                    if (nodes[idx].f < min_f) {
                        min_f = nodes[idx].f;
                        current = &nodes[idx];
                        current_pos = (Point){x, y};
                        current_idx = idx;
                    }
                }
            }
        }

        if (current == NULL) {
            DBG_ERR("There is no road");
            free(nodes);
            return -1;
        }

        // 判斷是否到終點
        if (current_pos.x == end_x && current_pos.y == end_y) {
            found = true;
            break;
        }

        // 關閉當前節點
        current->state = CLOSED;

        // 檢查鄰居
        int8_t dirs[8][2] = {
            {0, -1}, {0, 1}, {-1, 0}, {1, 0},   // 直線
            {-1, -1}, {1, -1}, {-1, 1}, {1, 1}  // 斜向
        };

        for (uint8_t i = 0; i < 8; i++) {
            FORM_POINT new_x = current_pos.x + dirs[i][0];
            FORM_POINT new_y = current_pos.y + dirs[i][1];

            // 判斷是否為斜向
            bool is_diagonal = (dirs[i][0] != 0 && dirs[i][1] != 0);
            int movement_cost = is_diagonal ? COST_DIAGONAL : COST_STRAIGHT;

            // 基本檢查
            if (!is_valid(new_x, new_y, width, height, map)) continue;

            FORM_POINT n_idx = get_index(new_x, new_y, width);
            if (nodes[n_idx].state == CLOSED) continue;

            // 防切角檢查
            if (is_diagonal) {
                if (!is_valid(current_pos.x + dirs[i][0], current_pos.y, width, height, map) ||
                    !is_valid(current_pos.x, current_pos.y + dirs[i][1], width, height, map))
                {
                    continue;
                }
            }

            // 計算 G 值
            int new_g = current->g + movement_cost;

            if (nodes[n_idx].state != OPEN || new_g < nodes[n_idx].g)
            {
                nodes[n_idx].g = new_g;
                nodes[n_idx].h = calc_h(new_x, new_y, end_x, end_y);
                nodes[n_idx].f = nodes[n_idx].g + nodes[n_idx].h;
                nodes[n_idx].parent = current_pos;
                nodes[n_idx].state = OPEN;
            }
        }
    }

    // 回溯路徑
    FORM_LEN path_len = 0;
    if (found) {
        // 先暫存路徑 (這是倒序的: End -> Start)
        Point* temp_path = (Point*)malloc(width * height * sizeof(Point));
        Point p = {end_x, end_y};

        while (p.x != -1 && p.y != -1) {
            temp_path[path_len++] = p;
            FORM_LEN idx = get_index(p.x, p.y, width);
            p = nodes[idx].parent;

            // 安全檢查：若回到起點的前一個 (-1, -1) 則停止
            if (p.x == -1 && p.y == -1) break;
            // 若路徑過長超過 buffer
            if (path_len >= (width * height / 2)) break;
        }

        // 將路徑反轉存入 out_buffer (變成 Start -> End)
        // 格式為: [x0, y0, x1, y1, x2, y2...]
        for (int i = 0; i < path_len; i++) {
            out_buffer[i * 2] = temp_path[path_len - 1 - i].x;
            out_buffer[i * 2 + 1] = temp_path[path_len - 1 - i].y;
        }
        free(temp_path);
    } else {
        DBG_NOR("Could not find the way");
        path_len = -1;
    }

    free(nodes);
    return path_len;
}
