from copy import copy
from typing import List, Tuple

from py.debug import dbg
from py.game.ai.profile.base import AIProfile
from py.game.ai.profile.personality import TraitData


class AIProfileFactory:
    @staticmethod
    def create_mixed_profile(base_profile: AIProfile, traits: List[Tuple[TraitData, float]]) -> AIProfile:
        new_profile = copy(base_profile)
        for trait_data, intensity in traits:
            AIProfileFactory._apply_trait(new_profile, trait_data, intensity)
        return new_profile

    @staticmethod
    def _apply_trait(profile: AIProfile, trait: TraitData, intensity: float):
        for param, delta in trait.items():

            attr_name = param.value
            if not hasattr(profile, attr_name):
                dbg.war(f"[AIProfileFactory] Profile has no attribute '{attr_name}', skipping trait.")
                continue

            original_value = getattr(profile, attr_name)
            change = delta * intensity
            final_value = original_value + change

            # 邊界檢查：權重不為負
            if "weight" in attr_name or "bias" in attr_name:
                final_value = max(0.0, final_value)

            # 處理整數屬性 (如 reserve, scan_range)
            if isinstance(original_value, int):
                final_value = int(round(final_value))

            setattr(profile, attr_name, final_value)
