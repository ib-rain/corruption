import random as r
import statistics as s


class Official:
    def __init__(self, hier_id, wage, strategy, kappa, theta, is_in_coal):
        self.hier_id = hier_id
        self.wage = wage
        # Strategy is a 3-tuple: (stealing_strategy, action_if_inspected, bribes)
        self.stealing_strategy = strategy[0]
        self.action = strategy[1]
        self.bribe = strategy[2]
        self.kappa = kappa
        self.theta = theta
        self.is_in_coal = is_in_coal
        self.stealing = 0
        self.acc_win = 0

    def steal(self, opt_stealing):
        if self.stealing_strategy == "None":
            self.stealing = 0
        elif self.stealing_strategy == "Opt":
            self.stealing = opt_stealing
        return self.stealing

    def pay_bribe(self, sure=False):
        return self.bribe[sure]

# sure = all(sub_id in coal_offs for sub_id in off_scheme[off_id])
# sure = False = 0 -> B[ch]
# sure = True = 1 -> B[b]
# subs don't care


class Hierarchy:
    def __init__(self, scheme, officials, cutoff_values, inspector):
        self.scheme = scheme
        self.officials = officials
        self.cutoff_values = cutoff_values
        self.inspector = inspector

    def get_with_id(self, hier_id):
        return next((x for x in self.officials if x.hier_id == hier_id), None)

    def get_boss_of_id(self, hier_id):
        for boss in self.scheme:
            if hier_id in self.scheme[boss]:
                return self.get_with_id(boss)


class Coalition:
    def __init__(self, scheme_tuple, hierarchy, rule):
        self.scheme_name = scheme_tuple[0]
        self.off_ids = scheme_tuple[1]
        self.hierarchy = hierarchy
        self.rule = rule
        self.bribe = 0
        self.total_stealing = 0  # Do I really need this?
        self.utils = {}

    def calc_stealing(self):
        if self.total_stealing == 0:
            for off_id in self.off_ids:
                self.total_stealing = self.total_stealing + self.hierarchy.get_with_id(off_id).stealing

        return self.total_stealing

    def pay_bribe(self, inspected_id):
        self.bribe = self.hierarchy.get_with_id(inspected_id).pay_bribe(all(sub_id in self.off_ids for sub_id in self.hierarchy.scheme.get(inspected_id, [])))
        return self.bribe

    def calc_utils(self):
        for off_id in self.off_ids:
            self.utils[off_id] = self.rule(off_id, self.off_ids, self.bribe, self.total_stealing, self.hierarchy)

        return sum(self.utils.values()) == (self.total_stealing - self.bribe)


def EQ_rule(off_id, coal_off_ids, bribe, coal_stealing, hier_scheme):
    return (coal_stealing - bribe) / len(coal_off_ids)


def SS_with_xi(xi):
    def SS_rule(off_id, coal_off_ids, bribe, coal_stealing, hier):
        U = 0
        bl = 3
        subs = set()
        for off in hier.scheme.keys():
            if off[0] == bl:
                subs = subs.union(set(hier.scheme[off]))

        if off_id[0] == bl:
            U = hier.get_with_id(off_id).stealing - (bribe + xi * len(subs.intersection(set(coal_off_ids))) * hier.get_with_id(off_id).stealing) / len([1 for off in coal_off_ids if off[0] == bl])

        elif off_id[0] in (1, 2):
            U = hier.get_with_id(off_id).stealing + xi * hier.get_boss_of_id(off_id).stealing
# Hard-coded and works only on the hierarchy suggested in the work: 3 levels with 2 officials on each.
        return U

    return SS_rule

class Inspector:
    def __init__(self, wage, inspection_cost_func, coverup_cost_func):
        self.wage = wage
        self.acc_win = 0
        self.inspection_cost_func = inspection_cost_func
        self.coverup_cost_func = coverup_cost_func


def true_with_prob(prob):
    return r.random() < prob


#Criminal Code of Russia 285.1
def ru_steal_fine(wage, stealing, is_in_coal):
    if stealing == 0:
        return 0

    if is_in_coal or stealing >= 7500000:
        return max(s.mean((2, 5)) * 100000, s.mean((1, 3)) * 12 * wage)
    return max(s.mean((1, 3)) * 100000, s.mean((1, 2)) * 12 * wage)


#Criminal Code of Russia 291
def ru_bribe_fine(wage, bribe, is_in_coal):
    if bribe >= 1000000:
        return max(s.mean((2, 4)) * 1000000, s.mean((2, 4)) * 12 * wage, s.mean((70, 90)) * bribe)
    elif is_in_coal or bribe >= 150000:
        return max(s.mean((1, 3)) * 1000000, s.mean((1, 3)) * 12 * wage, s.mean((60, 80)) * bribe)
    elif bribe >= 25000:
        return max(1 * 1000000, 2 * 12 * wage, s.mean((10, 40)) * bribe)
    else:
        return max(0.5 * 1000000, 1 * 12 * wage, s.mean((5, 30)) * bribe)


def threshold_func(stealing, thresholds):
    if stealing == 0:
        return 0

    for th in thresholds:
        if stealing >= th[0]:
            return th[1]


def reward_func_def(stealing):
    return threshold_func(stealing, ((400000, 75000), (100000, 40000)))


def coverup_cost_func_def(stealing):
    return threshold_func(stealing, ((400000, 11250), (100000, 5000)))


def reward_func_s1(stealing):
    return threshold_func(stealing, ((400000, 600000), (100000, 90000)))


def coverup_cost_func_s1(stealing):
    return threshold_func(stealing, ((400000, 141642.8571), (100000, 25000)))


def reward_func_s2(stealing):
    return threshold_func(stealing, ((400000, 2000000), (100000, 90000)))


def coverup_cost_func_s2(stealing):
    return threshold_func(stealing, ((400000, 999500), (100000, 25000)))


def reward_func_s3(stealing):
    return threshold_func(stealing, ((400000, 3250000), (100000, 2000000)))


def coverup_cost_func_s3(stealing):
    return threshold_func(stealing, ((400000, 2500000), (100000, 999874.976)))


def reward_func_1_s1(stealing):
    return threshold_func(stealing, ((400000, 270000), (100000, 70000)))


def coverup_cost_func_1_s1(stealing):
    return threshold_func(stealing, ((400000, 124500), (100000, 35000)))


def reward_func_1_s3(stealing):
    return threshold_func(stealing, ((400000, 250000), (100000, 84750)))


def coverup_cost_func_1_s3(stealing):
    return threshold_func(stealing, ((400000, 124625), (100000, 40125)))


def inspection_cost_func_example(off):
    if off.hier_id[0] >= 3:
        return 22500
    if off.hier_id[0] >= 1:
        return 10000


def simulate(N, hierarchy, steal_fine_func, bribe_fine_func, reward_func, coalition):
    acc_state_util = 0
    for _ in range(N):
        # Play the game N times.
        stealing = {}
        for off_level in hierarchy.scheme.values():
            stealing[off_level] = 0

        sum_stealing = 0

        inspected_off = None
        exposers = []
        init_money = list(hierarchy.cutoff_values.values())[0][0]
        # print(hierarchy.officials)
        coal_officials = []
        for i in range(len(hierarchy.officials)):
            for off_id in coalition.off_ids:
                if hierarchy.officials[i].hier_id == off_id:
                    coal_officials.append(hierarchy.officials[i])

        coal_officials = set(coal_officials)
        non_coal_officials = set(hierarchy.officials) ^ coal_officials

        def calc_coverup_reward_inspect(exposers_list):
            coverup = 0
            reward = 0
            inspect = 0

            for exposer in exposers_list:
                coverup += hierarchy.inspector.coverup_cost_func(exposer.stealing)
                reward += reward_func(exposer.stealing)
                inspect += hierarchy.inspector.inspection_cost_func(exposer)

            return coverup, reward, inspect

        def end(x):
            utils_correct = coalition.calc_utils()
            if not utils_correct:
                print("ERROR in calculating coalitional utilities, review the rule!")
                exit(-1)

            state_ut = init_money
            # print(x)

            if x == 1:
                # No inspection
                for off in coal_officials:
                    u = off.wage + coalition.utils[off.hier_id]
                    off.acc_win += u
                    state_ut -= u

                for off in non_coal_officials:
                    u = off.wage + off.stealing
                    off.acc_win += u
                    state_ut -= u

                hierarchy.inspector.acc_win += hierarchy.inspector.wage
                state_ut -= hierarchy.inspector.wage

                return state_ut
            else:
                if x == 2:
                    # No bribe
                    if inspected_off.is_in_coal:
                        for off in coal_officials:
                            u = off.wage + coalition.utils[off.hier_id] - steal_fine_func(
                                off.wage, coalition.total_stealing, True)
                            off.acc_win += u
                            state_ut -= u

                    else:
                        u = inspected_off.wage + inspected_off.kappa * inspected_off.stealing - steal_fine_func(
                            inspected_off.wage, inspected_off.stealing, False)
                        inspected_off.acc_win += u
                        state_ut -= u

                        for off in coal_officials:
                            u = off.wage + coalition.utils[off.hier_id]
                            off.acc_win += u
                            state_ut -= u

                    for off in non_coal_officials - {inspected_off}:
                        u = off.wage + off.stealing
                        off.acc_win += u
                        state_ut -= u

                    hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(
                            inspected_off) + reward_func(inspected_off.stealing)
                    state_ut -= (hierarchy.inspector.wage + reward_func(inspected_off.stealing))

                    return state_ut
                elif x == 3:
                    # Rejected bribe
                    if inspected_off.is_in_coal:
                        for off in coal_officials:
                            bribe = coalition.pay_bribe(inspected_off.hier_id)
                            u = off.wage + coalition.utils[off.hier_id] - (steal_fine_func(
                                off.wage, coalition.total_stealing, True) + bribe_fine_func(off.wage, bribe, True))
                            off.acc_win += u
                            state_ut -= u

                    else:
                        u = inspected_off.wage + inspected_off.kappa * inspected_off.stealing - (
                                inspected_off.pay_bribe(False) + steal_fine_func(inspected_off.wage, inspected_off.stealing, False) +
                                bribe_fine_func(inspected_off.wage, inspected_off.pay_bribe(False), False))
                        inspected_off.acc_win += u
                        state_ut -= u

                        for off in coal_officials:
                            u = off.wage + coalition.utils[off.hier_id]
                            off.acc_win += u
                            state_ut -= u

                    for off in non_coal_officials - {inspected_off}:
                        u = off.wage + off.stealing
                        off.acc_win += u
                        state_ut -= u

                    hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(
                        inspected_off) + reward_func(inspected_off.stealing)

                    state_ut -= (hierarchy.inspector.wage + reward_func(inspected_off.stealing))

                    return state_ut
                elif x == 4:
                    # Accepted bribe
                    if inspected_off.is_in_coal:
                        hierarchy.inspector.acc_win += hierarchy.inspector.wage + coalition.pay_bribe(inspected_off.hier_id) - (
                                hierarchy.inspector.inspection_cost_func(inspected_off) + hierarchy.inspector.coverup_cost_func(inspected_off.stealing))

                    else:
                        inspected_off.acc_win += inspected_off.wage + inspected_off.stealing - inspected_off.pay_bribe(False)
                        state_ut -= (inspected_off.wage + inspected_off.stealing)
                        hierarchy.inspector.acc_win += hierarchy.inspector.wage + inspected_off.pay_bribe() - (
                                hierarchy.inspector.inspection_cost_func(
                                    inspected_off) + hierarchy.inspector.coverup_cost_func(inspected_off.stealing))

                    for off in coal_officials:
                        u = off.wage + coalition.utils[off.hier_id]
                        off.acc_win += u
                        state_ut -= u

                    for off in non_coal_officials - {inspected_off}:
                        u = off.wage + off.stealing
                        off.acc_win += u
                        state_ut -= u

                    state_ut -= hierarchy.inspector.wage

                    return state_ut
                else:
                    sum_coverup, sum_reward, sum_inspect = calc_coverup_reward_inspect(exposers)

                    if x == 5:
                        # Exposed, no bribe
                        if inspected_off.is_in_coal:
                            for off in coal_officials:
                                u = off.wage + coalition.utils[off.hier_id] - steal_fine_func(
                                    off.wage, coalition.total_stealing, True)
                                off.acc_win += u
                                state_ut -= u

                        else:
                            u = inspected_off.wage + inspected_off.kappa * inspected_off.stealing - steal_fine_func(
                                inspected_off.wage, inspected_off.stealing, False)
                            inspected_off.acc_win += u
                            state_ut -= u

                            for off in coal_officials:
                                u = off.wage + coalition.utils[off.hier_id]
                                off.acc_win += u
                                state_ut -= u

                        for exposer in exposers:
                            u = exposer.wage + exposer.kappa * exposer.stealing - exposer.theta * steal_fine_func(
                                exposer.wage, exposer.stealing, False)
                            exposer.acc_win += u
                            state_ut -= u

                        for off in non_coal_officials - {inspected_off} - set(exposers):
                            u = off.wage + off.stealing
                            off.acc_win += u
                            state_ut -= u

                        hierarchy.inspector.acc_win += hierarchy.inspector.wage + reward_func(
                            inspected_off.stealing) + sum_reward - (
                                                               hierarchy.inspector.inspection_cost_func(
                                                                   inspected_off) + sum_inspect)
                        state_ut -= (hierarchy.inspector.wage + reward_func(inspected_off.stealing) + sum_reward)

                        return state_ut
                    elif x == 6:
                        # Exposed, rejected bribe
                        if inspected_off.is_in_coal:
                            bribe = coalition.pay_bribe(inspected_off.hier_id)
                            hierarchy.inspector.acc_win += hierarchy.inspector.wage + reward_func(
                                inspected_off.stealing) + sum_reward - (hierarchy.inspector.inspection_cost_func(inspected_off) + sum_inspect)

                            for off in coal_officials:
                                u = off.wage + coalition.utils[off.hier_id] - (steal_fine_func(
                                    off.wage, coalition.total_stealing, True) + bribe_fine_func(off.wage, bribe, True))
                                off.acc_win += u
                                state_ut -= u

                        else:
                            hierarchy.inspector.acc_win += hierarchy.inspector.wage + reward_func(
                                inspected_off.stealing) + sum_reward - (hierarchy.inspector.inspection_cost_func(inspected_off) + sum_inspect)
                            u = inspected_off.wage + inspected_off.kappa * inspected_off.stealing - (steal_fine_func(
                                inspected_off.wage, inspected_off.stealing, False) + inspected_off.pay_bribe() + bribe_fine_func(
                                inspected_off.wage, inspected_off.pay_bribe(False), False))
                            inspected_off.acc_win += u
                            state_ut -= u

                            for off in coal_officials:
                                u = off.wage + coalition.utils[off.hier_id]
                                off.acc_win += u
                                state_ut -= u

                        for exposer in exposers:
                            u = exposer.wage + exposer.kappa * exposer.stealing - exposer.theta * steal_fine_func(
                                exposer.wage, exposer.stealing, False)
                            exposer.acc_win += u
                            state_ut -= u

                        for off in non_coal_officials - {inspected_off} - set(exposers):
                            u = off.wage + off.stealing
                            off.acc_win += u
                            state_ut -= u

                        state_ut -= (hierarchy.inspector.wage + reward_func(inspected_off.stealing) + sum_reward)

                        return state_ut
                    elif x == 7:
                        # Exposed, accepted bribe
                        if inspected_off.is_in_coal:
                            hierarchy.inspector.acc_win += hierarchy.inspector.wage + coalition.pay_bribe(inspected_off.hier_id) - (
                                    hierarchy.inspector.inspection_cost_func(
                                        inspected_off) + hierarchy.inspector.coverup_cost_func(
                                inspected_off.stealing) + sum_coverup + sum_inspect)

                        else:
                            inspected_off.acc_win += inspected_off.wage + inspected_off.stealing - inspected_off.pay_bribe(False)
                            state_ut -= (inspected_off.wage + inspected_off.stealing)

                            hierarchy.inspector.acc_win += hierarchy.inspector.wage + inspected_off.pay_bribe(False) - (
                                    hierarchy.inspector.inspection_cost_func(inspected_off) + hierarchy.inspector.coverup_cost_func(
                                inspected_off.stealing) + sum_coverup + sum_inspect)

                        for off in coal_officials:
                            u = off.wage + coalition.utils[off.hier_id]
                            off.acc_win += u
                            state_ut -= u

                        for off in non_coal_officials - {inspected_off}:
                            u = off.wage + off.stealing
                            off.acc_win += u
                            state_ut -= u

                        state_ut -= hierarchy.inspector.wage

                        return state_ut

        # Stealing stage
        for off_level in hierarchy.scheme.values():
            cutoff_value = hierarchy.cutoff_values[off_level]
            optimal_stealing = (cutoff_value[0] - cutoff_value[1]) / len(off_level)
            for off in off_level:
                stealing[off_level] += hierarchy.get_with_id(off).steal(optimal_stealing)

        coalition.calc_stealing()
        # Inspection stage: from top to bottom, from left to right


        for off_level in stealing:
            sum_stealing += stealing[off_level]
            if true_with_prob(1 - sum_stealing / init_money):
                pass
            else:
                inspected_off = hierarchy.get_with_id(r.choice(off_level))
                action = inspected_off.action

                if inspected_off.is_in_coal:

                    Acc_part_util = coalition.pay_bribe(inspected_off.hier_id) - hierarchy.inspector.coverup_cost_func(inspected_off.stealing)
                    Rej_part_util = reward_func(inspected_off.stealing)

                    if Acc_part_util <= Rej_part_util:
                        acc_state_util += end(3)
                    else:
                        acc_state_util += end(4)
                    break
                else:
                    if action == "NB":
                        acc_state_util += end(2)
                        break
                    if action == "B":
                        Acc_part_util = inspected_off.pay_bribe() - hierarchy.inspector.coverup_cost_func(inspected_off.stealing)
                        Rej_part_util = reward_func(inspected_off.stealing)
                        if Acc_part_util <= Rej_part_util:
                            acc_state_util += end(3)
                        else:
                            acc_state_util += end(4)
                        break
                    if action == "E":
                        while True:
                            exposers.append(inspected_off)
                            inspected_off = hierarchy.get_boss_of_id(inspected_off.hier_id)
                            action = inspected_off.action

                            if inspected_off.is_in_coal:
                                Acc_part_util = coalition.pay_bribe(
                                    inspected_off.hier_id) - hierarchy.inspector.coverup_cost_func(
                                    inspected_off.stealing)
                                Rej_part_util = reward_func(inspected_off.stealing)

                                if Acc_part_util <= Rej_part_util:
                                    acc_state_util += end(6)
                                else:
                                    acc_state_util += end(7)
                                break

                            else:
                                if action == "NB":
                                    acc_state_util += end(5)
                                    break
                                if action == "B":
                                    exposers_coverup, exposers_reward, exposers_inspect = calc_coverup_reward_inspect(exposers)
                                    Acc_part_util = inspected_off.pay_bribe(False) - hierarchy.inspector.coverup_cost_func(inspected_off.stealing) - exposers_coverup
                                    Rej_part_util = reward_func(inspected_off.stealing) + exposers_reward
                                    if Acc_part_util <= Rej_part_util:
                                        acc_state_util += end(6)
                                    else:
                                        acc_state_util += end(7)
                                    break
                    break

        if inspected_off is None:
            acc_state_util += end(1)

    LoC = sum(stealing.values()) / init_money
    # End of N cycles, Results
    for official in hierarchy.officials:
        print("{}".format(official.acc_win / N))
    print("{}\n{}\n{}".format(hierarchy.inspector.acc_win / N, acc_state_util / N, LoC))


def run_coals(off_scheme, in_and_out_values, funcs, wages, bribes, coal_scheme_tuples, rules):
    def level_12_official(hier_id, strat, is_in_coal):
        return Official(hier_id=hier_id, wage=wages[0], strategy=strat, kappa=0.3, theta=0.01, is_in_coal=is_in_coal)

    def level_3_official(hier_id, strat, is_in_coal):
        return Official(hier_id=hier_id, wage=wages[1], strategy=strat, kappa=0.6, theta=1, is_in_coal=is_in_coal)

    def build_hier(str1, str2, coal):
        offs = [
            level_3_official((3, 0), str2, ((3, 0) in coal)), level_3_official((3, 1), str2, ((3, 1) in coal)),
            level_12_official((2, 0), str1, ((2, 0) in coal)), level_12_official((2, 1), str1, ((2, 1) in coal)),
            level_12_official((1, 0), str1, ((1, 0) in coal)), level_12_official((1, 1), str1, ((1, 1) in coal))
        ]
        return offs

    for rule in rules:
        for sc_tuple in coal_scheme_tuples:
            print(sc_tuple[0])
            off_hier = build_hier(("Opt", "E", [bribes[2], bribes[2]]), ("Opt", "B", [bribes[0], bribes[1]]), sc_tuple[1])
            inspector = Inspector(70000, inspection_cost_func_example, funcs[0])
            hierarchy = Hierarchy(off_scheme, off_hier, in_and_out_values, inspector)
            coalition = Coalition(scheme_tuple=sc_tuple, hierarchy=hierarchy, rule=rule)
            simulate(N=100000, hierarchy=hierarchy, steal_fine_func=ru_steal_fine,
                    bribe_fine_func=ru_bribe_fine, reward_func=funcs[1], coalition=coalition)


def main():
    coal_scheme_tuples = [('1B1SL0', [(3, 0), (2, 0)],),
             ('1B1SL1', [(3, 0), (2, 1)],),
             ('1B1SR0', [(3, 1), (1, 0)],),
             ('1B1SR1', [(3, 1), (1, 1)],),
             ('BB1SL0', [(3, 0), (2, 0), (3, 1)],),
             ('BB1SL1', [(3, 0), (2, 1), (3, 1)],),
             ('BB1SR0', [(3, 1), (1, 0), (3, 0)],),
             ('BB1SR1', [(3, 1), (1, 1), (3, 0)],),
             ('1B2SL', [(3, 0), (2, 0), (2, 1)],),
             ('1B2SR', [(3, 1), (1, 0), (1, 1)],),
             ('2SBBL', [(3, 0), (3, 1), (2, 0), (2, 1)],),
             ('2SBBR', [(3, 0), (3, 1), (1, 0), (1, 1)],),
             ('1SBB1S0', [(2, 0), (3, 0), (3, 1), (1, 0)],),
             ('1SBB1S1', [(2, 0), (3, 0), (3, 1), (1, 1)],),
             ('1SBB1S2', [(2, 1), (3, 0), (3, 1), (1, 0)],),
             ('1SBB1S3', [(2, 1), (3, 0), (3, 1), (1, 1)],),
             ('2SBBL0', [(3, 0), (2, 0), (2, 1), (3, 1), (1, 0)],),
             ('2SBBL1', [(3, 0), (2, 0), (2, 1), (3, 1), (1, 1)],),
             ('2SBBR0', [(3, 1), (1, 0), (1, 1), (3, 0), (2, 0)],),
             ('2SBBR1', [(3, 1), (1, 0), (1, 1), (3, 0), (2, 1)],),
             ('GC', [(2, 0), (2, 1), (3, 0), (3, 1), (1, 0), (1, 1)])]

    # coal_scheme_tuples = [ ('1B1SR0', [(3, 1), (1, 0)],),]

    off_scheme = {
        (4, 0): ((3, 0), (3, 1)),
        (3, 0): ((2, 0), (2, 1)),
        (3, 1): ((1, 0), (1, 1)),
    }
    in_and_out_values = {
        ((3, 0), (3, 1)): (3000000, 2000000),
        ((2, 0), (2, 1)): (2000000 / 2, 750000),
        ((1, 0), (1, 1)): (2000000 / 2, 750000)
    }

    ch, b, s = 0, 1, 2

    W = [0, 90000, 40000]
    S = [0, 500000, 125000]

    B_d = [131750, 86750, 45125]

    B_1 = [857142.8571, 742142.8571, 115125]
    B_2 = [3115000, 3000000, 115125]
    B_3 = [8750374.976, 2999999.976, 5750500]

    B_t1 = []
    B_t3 = []

    B = B_d

    # rules = {EQ_rule, SS_with_xi(0.01)}
    rules = {EQ_rule}

    run_coals(off_scheme=off_scheme, in_and_out_values=in_and_out_values, funcs=(coverup_cost_func_def, reward_func_def),
              wages=[W[s], W[b]], bribes=B, coal_scheme_tuples=coal_scheme_tuples, rules=rules)


if __name__ == "__main__":
    main()
