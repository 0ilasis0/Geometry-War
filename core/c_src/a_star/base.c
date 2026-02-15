#include <stdbool.h>
#include <stdlib.h>
#include "c_inc/a_star/base.h"


// 輔助函式：計算 ID 陣列索引 (因為從 Python 傳入通常是攤平的陣列)
FORM_LEN get_index(FORM_POINT x, FORM_POINT y, FORM_W_H width) {
    return y * width + x;
}

// 曼哈頓距離
FORM_LEN calc_h(FORM_POINT start_x, FORM_POINT start_y, FORM_POINT end_x, FORM_POINT end_y) {
    int dx = abs(start_x - end_x);
    int dy = abs(start_y - end_y);
    if (dx > dy)
        return (COST_DIAGONAL * dy) + (COST_STRAIGHT * (dx - dy));
    else
        return (COST_DIAGONAL * dx) + (COST_STRAIGHT * (dy - dx));
}

// 檢查是否可走
bool is_valid(
    FORM_POINT x, FORM_POINT y,
    FORM_W_H width, FORM_W_H height,
    const FORM_MAP* map
) {
    if (x < 0 || x >= width || y < 0 || y >= height) return false;

    // map 中 0 是路，其他是非路 (1 是牆)
    return map[get_index(x, y, width)] == 0;
}
