from py.debug import dbg
from py.game.building.entity import BuildingEntity
from py.game.jelly.entity import JellyEntity
from py.game.jelly.variable import ARCH_TO_JOB_MAP, JellyStats, SpawnContext
from py.game.variable import GameType, GameTypeMap
from py.resource.registry import ResourceRegistry
from py.variable import GridPoint


class JellyFactory:
    @staticmethod
    def spawn_from_building(source_building: BuildingEntity, path: list[GridPoint], target_building, army_count):
        """ [外部入口] 建立 Context 並執行生成 """
        # 建立情境物件 (打包參數)
        ctx = SpawnContext(
            source = source_building,
            target = target_building,
            path = path,
            amount = army_count,
        )
        return JellyFactory._spawn_by_context(ctx)

    @staticmethod
    def _spawn_by_context(ctx: SpawnContext):
        """ 根據 Context 自動查表並生成實體 """

        # 決定職業 (從建築類型映射)
        arch_type = ctx.source.stats.arch
        job_type = ARCH_TO_JOB_MAP.get(arch_type)

        if not job_type:
            dbg.error(f"Error: No job mapping for arch {arch_type}")
            return None

        return JellyFactory._create_entity(ctx, job_type)

    @staticmethod
    def _create_entity(ctx: SpawnContext, job: GameType.Job):
        """ 負責將資料轉換為 JellyEntity """
        source_stats = ctx.source.stats

        stats = JellyStats(
            job = job,
            owner = ctx.owner,
            pos = ctx.start_pos,
            army = ctx.amount,
            attack = source_stats.jelly_attack,
            move_speed = source_stats.jelly_speed,
            path = ctx.path,
            target_building = ctx.target
        )

        img_id = JellyFactory._resolve_img_id(ctx.owner, job)

        return JellyEntity(stats, img_id)

    @staticmethod
    def _resolve_img_id(owner_enum, job_enum):
        """ 取得資源 ID """
        genre_str = GameTypeMap.get_value(GameType.Genre.JELLY)
        owner_str = GameTypeMap.get_value(owner_enum)
        job_str = GameTypeMap.get_value(job_enum)
        img_id = ResourceRegistry.get_key(genre_str, owner_str, job_str)

        if not img_id: dbg.error(f"The img_id [genre:{genre_str},owner:{owner_str},job:{job_str}] is not exisit")

        return img_id
