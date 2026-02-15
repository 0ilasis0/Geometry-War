from py.game.bullet.entity import BulletEntity
from py.screen.image.manager.core import img_mg


class BulletManager:
    def __init__(self):
        self.bullets: list[BulletEntity] = []

    def spawn_bullet(self, building, target, owner_logic):
        """ 生成一顆新子彈 """
        new_bullet = BulletEntity(
            building = building,
            target = target,
            owner_logic = owner_logic,
        )

        self.bullets.append(new_bullet)

    def update(self, dt: float):
        # 更新所有子彈
        for b in self.bullets:
            b.update(dt)

        # 移除無效子彈
        self.bullets = [b for b in self.bullets if b.is_active]

    def render(self):
        for b in self.bullets:
            img_mg.draw_image_dynamic(
                image_id = b.ui.img_id,
                pos = b.ui.pos,
                size = b.ui.size
            )

    def clear_all(self):
        self.bullets.clear()
