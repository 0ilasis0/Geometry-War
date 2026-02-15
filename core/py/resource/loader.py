from py.debug import dbg
from py.game.variable import GameMaxVar, GameType, GameTypeMap
from py.path.manager import PathBase
from py.path.uility import PathUtility
from py.resource.registry import ResourceRegistry
from py.screen.image.variable import ImageProfile


class ResourceAutoLoader:
    """
    負責自動遍歷 GameTypeMap 並加載資源至 IMAGE_RESOURCE_MAP
    """
    def __init__(self, target_map: dict):
        self.target_map = target_map
        # 為了方便取得字串值，先緩存一些常用變數
        self.neutral_owner_val = GameTypeMap.get_value(GameType.Owner.NEUTRAL)

    def load_all(self):
        """ 一鍵加載所有動態資源 """
        self.load_buildings()
        self.load_jellies()
        self.load_bullets()

    def load_buildings(self):
        genre_val = GameTypeMap.get_value(GameType.Genre.ARCH)

        # 定義不同建築的最大等級
        genre_max_level_map = {
            GameType.Arch.CASTLE: GameMaxVar.LEVEL_CASTLE,
            GameType.Arch.LAB: GameMaxVar.LEVEL_LAB,
            GameType.Arch.PRODUCTION: GameMaxVar.LEVEL_PRODUCTION,
        }

        for _, owner_val in GameTypeMap.owner.items():
            for g_job, arch_val in GameTypeMap.arch.items():
                max_lv = genre_max_level_map.get(g_job, 0)
                max_lv += 1

                for level in range(max_lv):
                    # 參數組裝
                    args = [genre_val, owner_val, arch_val, level]

                    # 執行註冊與載入 (建築有多張圖，需要 count)
                    self._process_entry(
                        args,
                        path_kwargs={'count': GameMaxVar.VISUAL_STATE_COUNT}
                    )

    def load_jellies(self):
        genre_val = GameTypeMap.get_value(GameType.Genre.JELLY)

        for _, owner_val in GameTypeMap.owner.items():
            # 排除中立陣營
            if owner_val == self.neutral_owner_val: continue

            for _, job_val in GameTypeMap.job.items():
                args = [genre_val, owner_val, job_val]
                self._process_entry(args)

    def load_bullets(self):
        genre_val = GameTypeMap.get_value(GameType.Genre.BULLET)

        for _, owner_val in GameTypeMap.owner.items():
            args = [genre_val, owner_val]
            self._process_entry(args)

    def _process_entry(self, args: list, path_kwargs: dict | None = None):
        """
        向 ResourceRegistry 註冊 Key
        向 PathUtility 取得路徑
        存入 target_map
        """
        if path_kwargs is None:
            path_kwargs = {}

        # 註冊 ID
        key = ResourceRegistry.register_key(*args)

        # 生成路徑
        # PathUtility 需要基底路徑 (PathBase.img) + 識別參數
        paths = PathUtility.get_sequential_paths(PathBase.img, *args, **path_kwargs)

        # 存入 Map
        if paths:
            self.target_map[key] = ImageProfile(path = paths)
        else:
            dbg.war(f"Resource path not found for args: {args}")
