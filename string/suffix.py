# -*- coding: utf-8 -*-

from data_structure.suffixArray import SuffixArray


class Main():
    def pattern_search(self, txt, pat):
        sfx = SuffixArray().main_nlogn(txt)
        low, high = 0, len(sfx) - 1
        while low <= high:
            mid = low + (high - low) / 2
            ret = cmp(pat, txt[sfx[mid]:sfx[mid] + len(pat)] if sfx[mid] + len(pat) < len(txt) else sfx[mid] + len(pat))
            if ret < 0:
                high = mid - 1
            elif ret > 0:
                low = mid + 1
            else:
                assert (ret == 0)
                return sfx[mid]
        return None

    def minimum_lexicographic_rotation(self, str):
        concat = str + str
        sfx = SuffixArray().main_nlogn(concat)
        for s in sfx:
            if len(concat) - s >= len(str):
                return concat[s:s + len(str)]

    def testcase(self):
        assert (self.pattern_search('banana', 'nan') == 2)
        assert (self.minimum_lexicographic_rotation('alabala') == 'aalabal')
        print 'pass:', self.__class__


if __name__ == '__main__':
    Main().testcase()
    print 'done'
