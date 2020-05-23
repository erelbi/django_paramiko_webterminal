import app
from app.models import Words_Point
import collections


def script_cal(words):
        script_in_word = Words_Point.objects.values_list('word', flat=True)
        point = 0
        words_split = words.split()
        word_counts = collections.Counter(words_split)
        for word, count in sorted(word_counts.items()):
            if str(word) in script_in_word:
                p = Words_Point.objects.filter(word=word).values('point')
                total = int(count)*int(p)
                print(total)
                return total