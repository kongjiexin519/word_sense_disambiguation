from nltk.corpus import framenet as fn
import pandas as pd


def frame_chose():
    fs = fn.frames()
    fs_dic = {}
    fs_ID = []
    for f in fs:
        fs_ID.append(f.ID)
        fs_dic[f.name] = []
        lexes = f.lexUnit
        for lex in lexes:
            fs_dic[f.name].append(lexes[lex].name)

    fs_ID_copy = fs_ID
    result = []
    for f1 in fs_ID:
        fs_ID_copy.remove(f1)
        f1_name = fn.frame(f1).name
        set1 = set(fs_dic[f1_name])
        for f2 in fs_ID_copy:
            f2_name = fn.frame(f2).name
            set2 = set(fs_dic[f2_name])
            r = list(set1 & set2)
            result.append((f1_name, f2_name, r, len(r)))

    result = sorted(result, key=lambda x: (x[3]), reverse=True)

    frame_chose = []
    for r in result:
        if r[3] >= 10:
            frame_chose.append(r)

    return frame_chose


if __name__ == '__main__':
    fs = frame_chose()
    for r in fs:
        f1 = fn.frame(r[0])
        f2 = fn.frame(r[1])
        lex_list = r[2]
        ls1 = f1.lexUnit
        ls2 = f2.lexUnit

        sents = []
        frames = []
        for l in lex_list:
            l_list = l.split('.')
            ss1 = ls1[l].exemplars
            ss2 = ls2[l].exemplars

            for s in ss1:
                sents.append(s.text)
            for s in ss2:
                sents.append(s.text)

            for i in range(len(ss1)):
                frames.append(r[0])

            for i in range(len(ss2)):
                frames.append(r[1])

            print()

        input_dict = {'Sentences' : sents, 'Frame' : frames}
        df = pd.DataFrame(input_dict)
        df.to_csv('bert_input/'+r[0] + r[1] + '.csv', index=False)
