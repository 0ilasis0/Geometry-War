#pragma once

// 確保你的函式在 Windows 系統下能被外部程式（如 Python）看見並呼叫
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

EXPORT int solve_astar(
    const FORM_MAP* map ,
    FORM_W_H width      , FORM_W_H height,
    FORM_POINT start_x  , FORM_POINT start_y,
    FORM_POINT end_x    , FORM_POINT end_y,
    FORM_OUT_BUFFER* out_buffer
);
