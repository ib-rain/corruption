from math import factorial

coals = [0, frozenset([(1, 1)]), frozenset([(1, 0)]), frozenset([(1, 0), (1, 1)]), frozenset([(2, 1)]),
             frozenset([(2, 1), (1, 1)]), frozenset([(2, 1), (1, 0)]), frozenset([(2, 1), (1, 0), (1, 1)]),
             frozenset([(2, 0)]), frozenset([(2, 0), (1, 1)]), frozenset([(2, 0), (1, 0)]),
             frozenset([(2, 0), (1, 0), (1, 1)]), frozenset([(2, 0), (2, 1)]), frozenset([(2, 0), (2, 1), (1, 1)]),
             frozenset([(2, 0), (2, 1), (1, 0)]), frozenset([(2, 0), (2, 1), (1, 0), (1, 1)]), frozenset([(3, 1)]),
             frozenset([(3, 1), (1, 1)]), frozenset([(3, 1), (1, 0)]), frozenset([(3, 1), (1, 0), (1, 1)]),
             frozenset([(3, 1), (2, 1)]), frozenset([(3, 1), (1, 1), (2, 1)]), frozenset([(3, 1), (1, 0), (2, 1)]),
             frozenset([(3, 1), (1, 0), (1, 1), (2, 1)]), frozenset([(3, 1), (2, 0)]),
             frozenset([(3, 1), (1, 1), (2, 0)]),
             frozenset([(3, 1), (1, 0), (2, 0)]), frozenset([(3, 1), (1, 0), (1, 1), (2, 0)]),
             frozenset([(3, 1), (2, 0), (2, 1)]), frozenset([(3, 1), (1, 1), (2, 0), (2, 1)]),
             frozenset([(3, 1), (1, 0), (2, 0), (2, 1)]), frozenset([(3, 1), (1, 0), (1, 1), (2, 0), (2, 1)]),
             frozenset([(3, 0)]), frozenset([(3, 0), (1, 1)]), frozenset([(3, 0), (1, 0)]),
             frozenset([(3, 0), (1, 0), (1, 1)]), frozenset([(3, 0), (2, 1)]), frozenset([(3, 0), (2, 1), (1, 1)]),
             frozenset([(3, 0), (2, 1), (1, 0)]), frozenset([(3, 0), (2, 1), (1, 0), (1, 1)]),
             frozenset([(3, 0), (2, 0)]),
             frozenset([(3, 0), (2, 0), (1, 1)]), frozenset([(3, 0), (2, 0), (1, 0)]),
             frozenset([(3, 0), (2, 0), (1, 0), (1, 1)]), frozenset([(3, 0), (2, 0), (2, 1)]),
             frozenset([(3, 0), (2, 0), (2, 1), (1, 1)]), frozenset([(3, 0), (2, 0), (2, 1), (1, 0)]),
             frozenset([(3, 0), (2, 0), (2, 1), (1, 0), (1, 1)]), frozenset([(3, 0), (3, 1)]),
             frozenset([(3, 0), (3, 1), (1, 1)]), frozenset([(3, 0), (3, 1), (1, 0)]),
             frozenset([(3, 0), (3, 1), (1, 0), (1, 1)]), frozenset([(3, 0), (3, 1), (2, 1)]),
             frozenset([(3, 0), (3, 1), (2, 1), (1, 1)]), frozenset([(3, 0), (3, 1), (2, 1), (1, 0)]),
             frozenset([(3, 0), (3, 1), (2, 1), (1, 0), (1, 1)]), frozenset([(3, 0), (3, 1), (2, 0)]),
             frozenset([(3, 0), (3, 1), (2, 0), (1, 1)]), frozenset([(3, 0), (3, 1), (2, 0), (1, 0)]),
             frozenset([(3, 0), (3, 1), (2, 0), (1, 0), (1, 1)]), frozenset([(3, 0), (3, 1), (2, 0), (2, 1)]),
             frozenset([(3, 0), (3, 1), (2, 0), (2, 1), (1, 1)]), frozenset([(3, 0), (3, 1), (2, 0), (2, 1), (1, 0)]),
             frozenset([(3, 0), (3, 1), (2, 0), (2, 1), (1, 0), (1, 1)])]

whole_coals_ids = [1, 2, 3, 4, 8, 12, 16, 17, 18, 19, 32, 36, 40, 44, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
                       59, 60, 61, 62, 63]

def calc_vals(whole_val):
    coal_vals = {}

    for i in whole_coals_ids:
        coal_vals[coals[i]] = whole_val[i]

    coal_vals[coals[5]] = coal_vals[coals[4]] + coal_vals[coals[1]]
    coal_vals[coals[6]] = coal_vals[coals[4]] + coal_vals[coals[2]]
    coal_vals[coals[7]] = coal_vals[coals[4]] + coal_vals[coals[3]]
    coal_vals[coals[9]] = coal_vals[coals[8]] + coal_vals[coals[1]]
    coal_vals[coals[10]] = coal_vals[coals[8]] + coal_vals[coals[2]]
    coal_vals[coals[11]] = coal_vals[coals[8]] + coal_vals[coals[3]]
    coal_vals[coals[13]] = coal_vals[coals[12]] + coal_vals[coals[1]]
    coal_vals[coals[14]] = coal_vals[coals[12]] + coal_vals[coals[2]]
    coal_vals[coals[15]] = coal_vals[coals[12]] + coal_vals[coals[3]]
    coal_vals[coals[20]] = coal_vals[coals[16]] + coal_vals[coals[4]]
    coal_vals[coals[21]] = coal_vals[coals[17]] + coal_vals[coals[4]]
    coal_vals[coals[22]] = coal_vals[coals[18]] + coal_vals[coals[4]]
    coal_vals[coals[23]] = coal_vals[coals[19]] + coal_vals[coals[4]]
    coal_vals[coals[24]] = coal_vals[coals[16]] + coal_vals[coals[8]]
    coal_vals[coals[25]] = coal_vals[coals[17]] + coal_vals[coals[8]]
    coal_vals[coals[26]] = coal_vals[coals[18]] + coal_vals[coals[8]]
    coal_vals[coals[27]] = coal_vals[coals[19]] + coal_vals[coals[8]]
    coal_vals[coals[28]] = coal_vals[coals[16]] + coal_vals[coals[12]]
    coal_vals[coals[29]] = coal_vals[coals[17]] + coal_vals[coals[12]]
    coal_vals[coals[30]] = coal_vals[coals[18]] + coal_vals[coals[12]]
    coal_vals[coals[31]] = coal_vals[coals[19]] + coal_vals[coals[12]]
    coal_vals[coals[33]] = coal_vals[coals[32]] + coal_vals[coals[1]]
    coal_vals[coals[34]] = coal_vals[coals[32]] + coal_vals[coals[2]]
    coal_vals[coals[35]] = coal_vals[coals[32]] + coal_vals[coals[3]]
    coal_vals[coals[37]] = coal_vals[coals[36]] + coal_vals[coals[1]]
    coal_vals[coals[38]] = coal_vals[coals[36]] + coal_vals[coals[2]]
    coal_vals[coals[39]] = coal_vals[coals[36]] + coal_vals[coals[3]]
    coal_vals[coals[41]] = coal_vals[coals[40]] + coal_vals[coals[1]]
    coal_vals[coals[42]] = coal_vals[coals[40]] + coal_vals[coals[2]]
    coal_vals[coals[43]] = coal_vals[coals[40]] + coal_vals[coals[3]]
    coal_vals[coals[45]] = coal_vals[coals[44]] + coal_vals[coals[1]]
    coal_vals[coals[46]] = coal_vals[coals[44]] + coal_vals[coals[2]]
    coal_vals[coals[47]] = coal_vals[coals[44]] + coal_vals[coals[3]]
    # todo chains or whatnot

    offs = [(3, 0), (3, 1), (2, 0), (2, 1), (1, 0), (1, 1)]
    H = len(offs)

    myerson_vec = {}
    for off in offs:
        myerson_vec[off] = 0
        for coal in coal_vals.keys():
            if off not in coal and off != coal:
                S = len(coal)
                myerson_vec[off] += factorial(S) * factorial(H - 1 - S) / factorial(H) * (
                            coal_vals[coal.union(frozenset([off]))] - coal_vals[coal])

    return myerson_vec


def check_conv(whole_val):
    coal_vals = {}

    for i in whole_coals_ids:
        coal_vals[coals[i]] = whole_val[i]

    coal_vals[coals[5]] = coal_vals[coals[4]] + coal_vals[coals[1]]
    coal_vals[coals[6]] = coal_vals[coals[4]] + coal_vals[coals[2]]
    coal_vals[coals[7]] = coal_vals[coals[4]] + coal_vals[coals[3]]
    coal_vals[coals[9]] = coal_vals[coals[8]] + coal_vals[coals[1]]
    coal_vals[coals[10]] = coal_vals[coals[8]] + coal_vals[coals[2]]
    coal_vals[coals[11]] = coal_vals[coals[8]] + coal_vals[coals[3]]
    coal_vals[coals[13]] = coal_vals[coals[12]] + coal_vals[coals[1]]
    coal_vals[coals[14]] = coal_vals[coals[12]] + coal_vals[coals[2]]
    coal_vals[coals[15]] = coal_vals[coals[12]] + coal_vals[coals[3]]
    coal_vals[coals[20]] = coal_vals[coals[16]] + coal_vals[coals[4]]
    coal_vals[coals[21]] = coal_vals[coals[17]] + coal_vals[coals[4]]
    coal_vals[coals[22]] = coal_vals[coals[18]] + coal_vals[coals[4]]
    coal_vals[coals[23]] = coal_vals[coals[19]] + coal_vals[coals[4]]
    coal_vals[coals[24]] = coal_vals[coals[16]] + coal_vals[coals[8]]
    coal_vals[coals[25]] = coal_vals[coals[17]] + coal_vals[coals[8]]
    coal_vals[coals[26]] = coal_vals[coals[18]] + coal_vals[coals[8]]
    coal_vals[coals[27]] = coal_vals[coals[19]] + coal_vals[coals[8]]
    coal_vals[coals[28]] = coal_vals[coals[16]] + coal_vals[coals[12]]
    coal_vals[coals[29]] = coal_vals[coals[17]] + coal_vals[coals[12]]
    coal_vals[coals[30]] = coal_vals[coals[18]] + coal_vals[coals[12]]
    coal_vals[coals[31]] = coal_vals[coals[19]] + coal_vals[coals[12]]
    coal_vals[coals[33]] = coal_vals[coals[32]] + coal_vals[coals[1]]
    coal_vals[coals[34]] = coal_vals[coals[32]] + coal_vals[coals[2]]
    coal_vals[coals[35]] = coal_vals[coals[32]] + coal_vals[coals[3]]
    coal_vals[coals[37]] = coal_vals[coals[36]] + coal_vals[coals[1]]
    coal_vals[coals[38]] = coal_vals[coals[36]] + coal_vals[coals[2]]
    coal_vals[coals[39]] = coal_vals[coals[36]] + coal_vals[coals[3]]
    coal_vals[coals[41]] = coal_vals[coals[40]] + coal_vals[coals[1]]
    coal_vals[coals[42]] = coal_vals[coals[40]] + coal_vals[coals[2]]
    coal_vals[coals[43]] = coal_vals[coals[40]] + coal_vals[coals[3]]
    coal_vals[coals[45]] = coal_vals[coals[44]] + coal_vals[coals[1]]
    coal_vals[coals[46]] = coal_vals[coals[44]] + coal_vals[coals[2]]
    coal_vals[coals[47]] = coal_vals[coals[44]] + coal_vals[coals[3]]

    C = True
    (y, n) = (0, 0)
    for S in coal_vals.keys():
        for T in coal_vals.keys():
            if S.intersection(T) == frozenset():
                inter = 0
            else:
                inter = coal_vals[S.intersection(T)]

            test = (coal_vals[S] + coal_vals[T] <= coal_vals[S.union(T)] + inter)
            if test:
                y = y + 1
            else:
                n = n + 1

            C = C & test

    # There are len(coal_vals.keys()) tests for S=T that return True.
    return C, y-len(coal_vals.keys()), n


def main():
    ch, b, s = 0, 1, 2

    W = [0, 90000, 40000]
    S = [0, 500000, 125000]

    d = [131251, 86251, 45001]
    s1 = [1384616.385, 1304616.385, 80001]
    s2 = [3080001, 3000001, 80001]
    s3 = [8750000.976, 5750001, 3000000.976]

    z1 = (500000, 395000, 105001)
    z3 = (500000, 375001, 125000)

    B = z3

    a = [0, 0.5, 0.416666667, 0.333333333]
    a_eff = [0, (1 - a[3]) * (1 - a[2]) * a[1], (1 - a[3]) * a[2], a[3]]

    # [0, 0.19444444443055556, 0.2777777781388889, 0.333333333]

    m_1B1SR = S[b] + S[s] - ((a[3] / 2 + a_eff[1] / 2) * B[ch] + a_eff[1] / 2 * B[s])
    m_1B1SL = S[b] + S[s] - ((a[3] / 2 + a_eff[2] / 2) * B[ch] + a_eff[2] / 2 * B[s])
    m_BB1SR = 2 * S[b] + S[s] - ((a[3] + a_eff[2] + a_eff[1] / 2) * B[ch] + a_eff[1] / 2 * B[s])
    m_BB1SL = 2 * S[b] + S[s] - ((a[3] + a_eff[2] / 2 + a_eff[1]) * B[ch] + a_eff[2] / 2 * B[s])
    m_1SBB1S = 2 * S[b] + 2 * S[s] - (
                (a[3] + a_eff[2] / 2 + a_eff[1] / 2) * B[ch] + (a_eff[2] / 2 + a_eff[1] / 2) * B[s])
    m_2SBB1SR = 2 * S[b] + 3 * S[s] - (
            (a[3] / 2 + a_eff[1] / 2) * B[ch] + a[3] / 2 * B[b] + (a_eff[2] + a_eff[1] / 2) * B[s])
    m_2SBB1SL = 2 * S[b] + 3 * S[s] - (
            (a[3] / 2 + a_eff[2] / 2) * B[ch] + a[3] / 2 * B[b] + (a_eff[2] / 2 + a_eff[1]) * B[s])

    myerson_vals = {1: S[s],
                    2: S[s],
                    3: 2 * S[s] - a_eff[1] * B[s],
                    4: S[s],
                    8: S[s],
                    12: 2 * S[s] - a_eff[2] * B[s],
                    16: S[b] - (a[3] / 2 + a_eff[1]) * B[ch],
                    17: m_1B1SR,
                    18: m_1B1SR,
                    19: S[b] + 2 * S[s] - (a[3] / 2 * B[b] + a_eff[1] * B[s]),
                    32: S[b] - (a[3] / 2 + a_eff[2]) * B[ch],
                    36: m_1B1SL,
                    40: m_1B1SL,
                    44: S[b] + 2 * S[s] - (a[3] / 2 * B[b] + a_eff[2] * B[s]),
                    48: 2 * S[b] - (a[3] + a_eff[2] + a_eff[1]) * B[ch],
                    49: m_BB1SR,
                    50: m_BB1SR,
                    51: 2 * S[b] + 2 * S[s] - ((a[3] / 2 + a_eff[2]) * B[ch] + a[3] / 2 * B[b] + a_eff[1] * B[s]),
                    52: m_BB1SL,
                    53: m_1SBB1S,
                    54: m_1SBB1S,
                    55: m_2SBB1SL,
                    56: m_BB1SL,
                    57: m_1SBB1S,
                    58: m_1SBB1S,
                    59: m_2SBB1SL,
                    60: 2 * S[b] + 2 * S[s] - ((a[3] / 2 + a_eff[1]) * B[ch] + a[3] / 2 * B[b] + a_eff[2] * B[s]),
                    61: m_2SBB1SR,
                    62: m_2SBB1SR,
                    63: 2 * S[b] + 4 * S[s] - (a[3] * B[b] + (a_eff[2] + a_eff[1]) * B[s])}

    t_R = S[s] - a_eff[1] / 2 * B[s]
    t_L = S[s] - a_eff[2] / 2 * B[s]
    t_1B1SR = S[b] + S[s] - (a[3] / 2 * B[b] + a_eff[1] / 2 * B[s])
    t_1B1SL = S[b] + S[s] - (a[3] / 2 * B[b] + a_eff[2] / 2 * B[s])
    t_BB1SR = 2 * S[b] + S[s] - (a[3] * B[b] + a_eff[1] / 2 * B[s])
    t_BB1SL = 2 * S[b] + S[s] - (a[3] * B[b] + a_eff[2] / 2 * B[s])
    t_1SBB1S = 2 * S[b] + 2 * S[s] - (a[3] * B[b] + (a_eff[2] / 2 + a_eff[1] / 2) * B[s])
    t_2SBB1SL = 2 * S[b] + 3 * S[s] - (a[3] * B[b] + (a_eff[1] / 2 + a_eff[2]) * B[s])
    t_2SBB1SR = 2 * S[b] + 3 * S[s] - (a[3] * B[b] + (a_eff[1] + a_eff[2] / 2) * B[s])

    theirson_vals = {1: t_R,
                     2: t_R,
                     3: myerson_vals[3],
                     4: t_L,
                     8: t_L,
                     12: myerson_vals[12],
                     16: S[b] - a[3] / 2 * B[s],
                     17: t_1B1SR,
                     18: t_1B1SR,
                     19: myerson_vals[19],
                     32: S[b] - a[3] / 2 * B[s],
                     36: t_1B1SL,
                     40: t_1B1SL,
                     44: myerson_vals[44],
                     48: 2 * S[b] - a[3] * B[b],
                     49: t_BB1SR,
                     50: t_BB1SR,
                     51: 2 * S[b] + 2 * S[s] - (a[3] * B[b] + a_eff[1] * B[s]),
                     52: t_BB1SL,
                     53: t_1SBB1S,
                     54: t_1SBB1S,
                     55: t_2SBB1SL,
                     56: t_BB1SL,
                     57: t_1SBB1S,
                     58: t_1SBB1S,
                     59: t_2SBB1SL,
                     60: 2 * S[b] + 2 * S[s] - (a[3] * B[b] + a_eff[2] * B[s]),
                     61: t_2SBB1SR,
                     62: t_2SBB1SR,
                     63: myerson_vals[63]}

    def print_it(vec):
        offs = [(3, 0), (3, 1), (2, 0), (2, 1), (1, 0), (1, 1)]
        for off in offs:
            print("{}\t{}".format(off, vec[off]))

    my = calc_vals(myerson_vals)
    print_it(my)
    print(check_conv(myerson_vals))
    print("\n")
    th = calc_vals(theirson_vals)
    print_it(th)
    print(check_conv(theirson_vals))


if __name__ == "__main__":
    main()
