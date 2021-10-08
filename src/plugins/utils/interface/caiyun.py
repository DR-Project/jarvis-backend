class AQI:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        if 0 < self.value <= 50:
            return '优'
        if 51 < self.value <= 100:
            return '良好'
        if 101 < self.value <= 150:
            return '轻度污染'
        if 151 < self.value <= 200:
            return '中度污染'
        if 201 < self.value <= 300:
            return '重度污染'
        return '严重污染'

    def suggest(self) -> str:
        if 51 < self.value <= 100:
            return '极少数异常敏感人群应减少户外活动'
        if 101 < self.value <= 150:
            return '儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼'
        if 151 < self.value <= 200:
            return '儿童、老年人及心脏病、呼吸系统疾病患者应避免长时间、高强度的户外锻炼，一般人群适量减少户外运动'
        if 201 < self.value <= 300:
            return '儿童、老年人及心脏病、呼吸系统疾病患者应停留在室内，停止户外活动，一般人群应避免户外活动'
        return '儿童、老年人及心脏病、呼吸系统疾病患者应停留在室内，避免体力消耗，一般人群应避免户外活动'
