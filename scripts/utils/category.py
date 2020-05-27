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

