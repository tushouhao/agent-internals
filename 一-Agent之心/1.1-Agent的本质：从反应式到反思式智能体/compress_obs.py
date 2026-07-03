# 高维原始感知压缩为特征向量
# 运行: python compress_obs.py

from typing import Any, Callable, Dict


def categorize_distance(lidar_value: float) -> str:
    """将雷达值分类为距离等级"""
    if lidar_value < 0.5:
        return "near"
    elif lidar_value < 2.0:
        return "mid"
    return "far"


def categorize_velocity(speed: float) -> str:
    """将速度值分类"""
    if speed < 0.1:
        return "stopped"
    elif speed < 1.0:
        return "slow"
    return "fast"


def infer_intent(trajectory: list) -> str:
    """从轨迹推断意图（仅使用历史帧，不含未来信息）"""
    if len(trajectory) < 2:
        return "unknown"
    dx = trajectory[-1][0] - trajectory[-2][0]
    dy = trajectory[-1][1] - trajectory[-2][1]
    if abs(dx) > abs(dy):
        return "moving_horizontal"
    return "moving_vertical"


def compress_observation(raw_obs: Dict[str, Any],
                         feature_map: Dict[str, Callable]) -> Dict[str, str]:
    """将高维原始感知压缩为低维特征向量"""
    return {name: func(raw_obs) for name, func in feature_map.items()}


if __name__ == "__main__":
    feature_map = {
        "distance": lambda o: categorize_distance(o.get("lidar", 99)),
        "velocity": lambda o: categorize_velocity(o.get("speed", 0)),
        "intent":   lambda o: infer_intent(o.get("trajectory", [])),
    }

    raw = {"lidar": 1.2, "speed": 0.5, "trajectory": [(0, 0), (1, 0), (2, 0)]}
    compressed = compress_observation(raw, feature_map)
    print(f"原始: {len(raw)} 维 -> 压缩: {len(compressed)} 维")
    print(f"压缩结果: {compressed}")
