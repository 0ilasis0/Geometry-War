#pragma once

#include "c_inc/a_star/variable.h"

FORM_LEN get_index(FORM_POINT x, FORM_POINT y, FORM_W_H width);
FORM_LEN calc_h(FORM_POINT start_x, FORM_POINT start_y, FORM_POINT end_x, FORM_POINT end_y);
bool is_valid(
    FORM_POINT x, FORM_POINT y,
    FORM_W_H width, FORM_W_H height,
    const FORM_MAP* map
);

