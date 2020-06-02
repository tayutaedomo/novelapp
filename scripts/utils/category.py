import re


class NarouCategory:
    categories = {
        'ハイファンタジー〔ファンタジー〕': 0,
        'ローファンタジー〔ファンタジー〕': 1,
        'VRゲーム〔SF〕': 2,
        '現実世界〔恋愛〕': 3,
        '歴史〔文芸〕': 4,
        '異世界〔恋愛〕': 100,
        '純文学〔文芸〕': 104,
        'ヒューマンドラマ〔文芸〕': 105,
        '推理〔文芸〕': 107,
        'ホラー〔文芸〕': 108,
        'アクション〔文芸〕': 109,
        'コメディー〔文芸〕': 110,
        '宇宙〔SF〕': 112,
        '空想科学〔SF〕': 113,
        'パニック〔SF〕': 114,
        '童話〔その他〕': 115,
        '詩〔その他〕': 116,
        'エッセイ〔その他〕': 117,
        'リプレイ〔その他〕': 118,
        'その他〔その他〕': 119,
        'ノンジャンル〔ノンジャンル〕': 120,
    }
    categories_reversed = dict(map(reversed, categories.items()))

    @classmethod
    def to_num(cls, text):
        return cls.categories.get(text, 120)

    @classmethod
    def to_text(cls, num):
        return cls.categories_reversed.get(num, 'ノンジャンル〔ノンジャンル〕')


class NarouCategory2:
    categories = {
        'ハイファンタジー〔ファンタジー〕': 0,
        'ローファンタジー〔ファンタジー〕': 0,
        '現実世界〔恋愛〕': 1,
        '異世界〔恋愛〕': 1,
        '歴史〔文芸〕': 2,
        '純文学〔文芸〕': 2,
        'ヒューマンドラマ〔文芸〕': 2,
        '推理〔文芸〕': 2,
        'ホラー〔文芸〕': 2,
        'アクション〔文芸〕': 2,
        'コメディー〔文芸〕': 2,
        'VRゲーム〔SF〕': 3,
        '宇宙〔SF〕': 3,
        '空想科学〔SF〕': 3,
        'パニック〔SF〕': 3,
        '童話〔その他〕': 4,
        '詩〔その他〕': 4,
        'エッセイ〔その他〕': 4,
        'リプレイ〔その他〕': 4,
        'その他〔その他〕': 4,
        'ノンジャンル〔ノンジャンル〕': 120,
    }
    categories_reversed = dict(map(reversed, categories.items()))

    @classmethod
    def to_num(cls, text):
        return cls.categories.get(text, 120)

    @classmethod
    def to_text(cls, num):
        text = cls.categories_reversed.get(num, 'ノンジャンル〔ノンジャンル〕')
        return re.split(r'[〔〕]', text)[1]

