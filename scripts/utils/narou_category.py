class NarouCategory:
    categories = {
        '異世界〔恋愛〕': 0,
        '現実世界〔恋愛〕': 1,
        'ハイファンタジー〔ファンタジー〕': 2,
        'ローファンタジー〔ファンタジー〕': 3,
        '純文学〔文芸〕': 4,
        'ヒューマンドラマ〔文芸〕': 5,
        '歴史〔文芸〕': 6,
        '推理〔文芸〕': 7,
        'ホラー〔文芸〕': 8,
        'アクション〔文芸〕': 9,
        'コメディー〔文芸〕': 10,
        'VRゲーム〔SF〕': 11,
        '宇宙〔SF〕': 12,
        '空想科学〔SF〕': 13,
        'パニック〔SF〕': 14,
        '童話〔その他〕': 15,
        '詩〔その他〕': 16,
        'エッセイ〔その他〕': 17,
        'リプレイ〔その他〕': 18,
        'その他〔その他〕': 19,
        'ノンジャンル〔ノンジャンル〕': 20,
    }
    categories_reversed = dict(map(reversed, categories.items()))

    @classmethod
    def to_num(cls, text):
        return cls.categories.get(text, 20)

    @classmethod
    def to_text(cls, num):
        return cls.categories_reversed.get(num, 'ノンジャンル〔ノンジャンル〕')

