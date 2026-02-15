from py.rendering.proxy import render_proxy
from py.screen.draw.manager import draw_mg
from py.screen.image.manager.core import img_mg


def submit_static_img():
    # 重置畫面物件是否存在
    render_proxy.reset_frame()

    # 背景/圖片更新
    img_mg.submit_static()

    # 更新繪圖draw
    draw_mg.submit_static()
