import subprocess

from py.debug import dbg
from py.path.manager import PathBase, PathConfig


class CompileAndLoadDll:
    def __init__(self):
        self.run(PathConfig.a_star.c, PathConfig.a_star.dll)

    def run(self, c_source_paths, dll_output_path, base_path = PathBase.core):
        '''
        c_source_path: c檔案位置
        dll_output_path: .dll生成位置
        '''

        # [防呆] 檢查每一個原始碼檔案是否存在
        for src in c_source_paths:
            if not src.exists():
                dbg.error(f"找不到原始碼: {src}")
                return

        # [防呆] 確保 DLL 的輸出資料夾存在，不然 GCC 會報錯
        if not dll_output_path.parent.exists():
            dll_output_path.parent.mkdir(parents=True, exist_ok=True)


        # 組合編譯指令 (前半部)
        cmd = [
            "gcc",
            "-shared",
            "-o", str(dll_output_path)
        ]
        # 使用迴圈將所有 .c 檔案加入指令
        for src in c_source_paths:
            cmd.append(str(src))
        # 組合編譯指令 (後半部)
        cmd.extend([
            "-I", str(base_path),
            "-std=c99",
            "-static-libgcc",
            "-O2"
        ])


        # 執行編譯
        result = subprocess.run(cmd, capture_output = True, text = True)

        if result.returncode != 0:
            dbg.error("編譯失敗！", result.stderr)
            return
        else:
            dbg.log(f"編譯成功！DLL 已生成於: {dll_output_path}")
