#pragma once
#include <stdio.h>
#include <time.h>



#define ENABLE_DEBUG

/* 時間格式輸出 [HH:MM:SS] */
#define LOG_TIME() do { \
    time_t sys_time = time(NULL); \
    struct tm *timer = localtime(&sys_time); \
    printf("[%02d:%02d:%02d] ", timer->tm_hour, timer->tm_min, timer->tm_sec); \
} while(0)


/* --- 一般 Debug 輸出 --- */
#ifdef ENABLE_DEBUG
  #define DBG_NOR(fmt, ...) do { \
      LOG_TIME(); \
      printf("\033[92m[DEBUG %s:%d %s()] " fmt "\033[0m\n", \
             __FILE__, __LINE__, __func__, ##__VA_ARGS__); \
  } while(0)
#else
  #define DBG_NOR(fmt, ...) do {} while(0)
#endif


/* --- 顯示變數名稱與值 (藍色) --- */
#ifdef ENABLE_DEBUG
  #define DBG_VAR(name, value, fmt_spec) do { \
      LOG_TIME(); \
      printf("\033[94m[VAR %s:%d %s()] %s = " fmt_spec "\033[0m\n", \
             __FILE__, __LINE__, __func__, #name, value); \
  } while(0)
#else
  #define DBG_VAR(name, value, fmt_spec) do {} while(0)
#endif


/* --- 錯誤輸出 (不受 ENABLE_DEBUG 控制) --- */
#define DBG_ERR(fmt, ...) do { \
    LOG_TIME(); \
    fprintf(stderr, "\033[91m[ERROR %s:%d %s()] " fmt "\033[0m\n", \
            __FILE__, __LINE__, __func__, ##__VA_ARGS__); \
    printf("\033[91m[ERROR %s:%d %s()] " fmt "\033[0m\n", \
           __FILE__, __LINE__, __func__, ##__VA_ARGS__); \
} while(0)

// 使用範例：
// DBG_ERR("Value is %d", val); （有 2 個參數）
