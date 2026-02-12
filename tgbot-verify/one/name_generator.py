"""随机名字生成器"""
import random
from typing import Dict, Tuple


class NameGenerator:
    """英文名字生成器"""

    ROOTS = {
        "prefixes": [
            "Al",
            "Bri",
            "Car",
            "Dan",
            "El",
            "Fer",
            "Gar",
            "Har",
            "Jes",
            "Kar",
            "Lar",
            "Mar",
            "Nor",
            "Par",
            "Quin",
            "Ros",
            "Sar",
            "Tar",
            "Val",
            "Wil",
        ],
        "middles": [
            "an",
            "en",
            "in",
            "on",
            "ar",
            "er",
            "or",
            "ur",
            "al",
            "el",
            "il",
            "ol",
            "am",
            "em",
            "im",
            "om",
            "ay",
            "ey",
            "oy",
            "ian",
        ],
        "suffixes": [
            "ton",
            "son",
            "man",
            "ley",
            "field",
            "ford",
            "wood",
            "stone",
            "worth",
            "berg",
            "stein",
            "bach",
            "heim",
            "gard",
            "land",
            "wick",
            "shire",
            "dale",
            "brook",
            "ridge",
        ],
        "name_roots": [
            "Alex",
            "Bern",
            "Crist",
            "Dav",
            "Edw",
            "Fred",
            "Greg",
            "Henr",
            "Ivan",
            "John",
            "Ken",
            "Leon",
            "Mich",
            "Nick",
            "Oliv",
            "Paul",
            "Rich",
            "Step",
            "Thom",
            "Will",
        ],
        "name_endings": [
            "a",
            "e",
            "i",
            "o",
            "y",
            "ie",
            "ey",
            "an",
            "en",
            "in",
            "on",
            "er",
            "ar",
            "or",
            "el",
            "al",
            "iel",
            "ael",
            "ine",
            "lyn",
        ],
    }

    PATTERNS = {
        "first_name": [
            ["prefix", "ending"],
            ["name_root", "ending"],
            ["prefix", "middle", "ending"],
            ["name_root", "middle", "ending"],
        ],
        "last_name": [
            ["prefix", "suffix"],
            ["name_root", "suffix"],
            ["prefix", "middle", "suffix"],
            ["compound"],
        ],
    }

    PATTERN_WEIGHTS = {
        "first_name": [3, 3, 2, 2],
        "last_name": [3, 3, 2, 1],
    }

    @classmethod
    def _generate_component(cls, pattern):
        """根据模式生成名字组件"""
        components = []
        for part in pattern:
            if part == "prefix":
                component = random.choice(cls.ROOTS["prefixes"])
            elif part == "middle":
                component = random.choice(cls.ROOTS["middles"])
            elif part == "suffix":
                component = random.choice(cls.ROOTS["suffixes"])
            elif part == "name_root":
                component = random.choice(cls.ROOTS["name_roots"])
            elif part == "ending":
                component = random.choice(cls.ROOTS["name_endings"])
            elif part == "compound":
                part1 = random.choice(cls.ROOTS["prefixes"])
                part2 = random.choice(cls.ROOTS["suffixes"])
                component = part1 + part2
            else:
                component = ""

            components.append(component)

        return "".join(components)

    @classmethod
    def _format_name(cls, name):
        """格式化名字（首字母大写）"""
        return name.capitalize()

    @classmethod
    def _is_valid_name_pair(cls, first_name: str, last_name: str) -> bool:
        """过滤掉明显不自然的名字组合。"""
        if first_name == last_name:
            return False
        if len(first_name) < 3 or len(last_name) < 4:
            return False
        if first_name[:3].lower() == last_name[:3].lower():
            return False
        return True

    @classmethod
    def _pick_patterns(cls) -> Tuple[list, list]:
        first_name_pattern = random.choices(
            cls.PATTERNS["first_name"],
            weights=cls.PATTERN_WEIGHTS["first_name"],
            k=1,
        )[0]
        last_name_pattern = random.choices(
            cls.PATTERNS["last_name"],
            weights=cls.PATTERN_WEIGHTS["last_name"],
            k=1,
        )[0]
        return first_name_pattern, last_name_pattern

    @classmethod
    def generate(cls) -> Dict[str, str]:
        """
        生成随机英文名字

        Returns:
            dict: 包含 first_name, last_name, full_name
        """
        for _ in range(5):
            first_name_pattern, last_name_pattern = cls._pick_patterns()

            first_name = cls._format_name(cls._generate_component(first_name_pattern))
            last_name = cls._format_name(cls._generate_component(last_name_pattern))

            if cls._is_valid_name_pair(first_name, last_name):
                return {
                    "first_name": first_name,
                    "last_name": last_name,
                    "full_name": f"{first_name} {last_name}",
                }

        # 兜底：避免极端随机导致无返回
        first_name = cls._format_name(cls._generate_component(["name_root", "ending"]))
        last_name = cls._format_name(cls._generate_component(["name_root", "suffix"]))
        return {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
        }


def generate_email(school_domain="MIT.EDU"):
    """
    生成随机学校邮箱

    Args:
        school_domain: 学校域名

    Returns:
        str: 邮箱地址
    """
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    username = "".join(random.choice(chars) for _ in range(8))
    return f"{username}@{school_domain}"


def generate_birth_date():
    """
    生成随机生日（2000-2005年）

    Returns:
        str: YYYY-MM-DD 格式的日期
    """
    year = 2000 + random.randint(0, 5)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f"{year}-{month}-{day}"
