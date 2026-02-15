#pragma once

#include <stdint.h>

// 定義節點狀態
#define NONE 0      // 未走過
#define OPEN 1      // 考慮走
#define CLOSED 2    // 已走過

// 設定直走斜走代價
#define COST_DIAGONAL 14
#define COST_STRAIGHT 10



typedef int FORM_MAP;
typedef int FORM_W_H;
typedef int FORM_POINT;
typedef int FORM_OUT_BUFFER;
typedef uint32_t FORM_LEN;

typedef struct Point {
    int x, y;
} Point;

typedef struct Node {
    uint32_t g;
    uint32_t h;
    uint32_t f;
    Point parent;
    uint8_t state;
} Node;

