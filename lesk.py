from nltk.corpus import framenet as fn
from nltk.stem import PorterStemmer
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


def lesk(context_sentence, candidate_choice, stem=True):
    ps = PorterStemmer()
    max_overlaps = 0
    lesk_sense = None

    # context_sentence = context_sentence.split()
    for ss in candidate_choice:
        lesk_dictionary = []

        # Includes definition.
        lesk_dictionary+= ss.split()

        if stem == True: # Matching exact words causes sparsity, so lets match stems.
            lesk_dictionary = [ps.stem(i) for i in lesk_dictionary]
            context_sentence = [ps.stem(i) for i in context_sentence]

        overlaps = set(lesk_dictionary).intersection(context_sentence)

        if len(overlaps) > max_overlaps:
            lesk_sense = ss
            max_overlaps = len(overlaps)

        if lesk_sense == None:
            lesk_sense = candidate_choice[0]

    return lesk_sense


def leak_result(ss, l_list, l, ls, f, candidate_choice):
    count = 0
    for s in ss:
        sent = s.text
        lesk_sense = lesk(sent, candidate_choice)

        if lesk_sense == ls[l].definition:
            count = count + 1

    return count, len(ss)


def sent_chosen(f1, f2, lex_list):
    ls1 = f1.lexUnit
    ls2 = f2.lexUnit
    correct, total = 0, 0

    for l in lex_list:
        l_list = l.split('.')
        ss1 = ls1[l].exemplars
        ss2 = ls2[l].exemplars

        candidate_choice = [ls1[l].definition, ls2[l].definition]

        if len(ss1) == 0 or len(ss2) == 0:
            continue
        l_correct, l_total = leak_result(ss1, l_list, l, ls1, f1, candidate_choice)

        correct = correct + l_correct
        total = total + l_total

    return correct/total


def main():
    frame1 = []
    frame2 = []
    accuracy = []

    fs = frame_chose()
    for r in fs:
        f1 = fn.frame(r[0])
        f2 = fn.frame(r[1])
        lex_list = r[2]
        acc = sent_chosen(f1, f2, lex_list)

        frame1.append(r[0])
        frame2.append(r[1])
        accuracy.append(acc)

    ja_dict = {"Frame1": frame1, "Frame2": frame2, "Accuracy": accuracy}
    df_ja = pd.DataFrame(data=ja_dict)
    df_ja.to_csv('lesk_output/frame_random.csv')


if __name__ == '__main__':
    main()