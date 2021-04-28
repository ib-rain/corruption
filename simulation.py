import random as r
import statistics as s


class Official:
    def __init__(self, hier_id, wage, strategy, kappa, theta):
        self.hier_id = hier_id
        self.wage = wage
        # Strategy is a 3-tuple: (stealing_strategy, action_if_inspected, bribe_coeff)
        self.stealing_strategy = strategy[0]
        self.action = strategy[1]
        self.bribe_coeff = strategy[2]
        self.kappa = kappa
        self.theta = theta
        self.stealing = 0
        self.acc_win = 0
        # self.coal_id

    def steal(self, opt_stealing):
        if self.stealing_strategy == "None":
            self.stealing = 0
        elif self.stealing_strategy == "Opt":
            self.stealing = opt_stealing
        return self.stealing

    def bribe(self):
        return self.bribe_coeff * self.stealing


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


class Inspector:
    def __init__(self, wage, inspection_cost_func, coverup_cost_func):
        self.wage = wage
        self.acc_win = 0
        self.inspection_cost_func = inspection_cost_func
        self.coverup_cost_func = coverup_cost_func


def true_with_prob(prob):
    return r.random() < prob


#Criminal Code of Russia 285.1
def ru_steal_fine(wage, stealing, is_in_coal=False):
    if stealing == 0:
        return 0

    if is_in_coal or stealing >= 7500000:
        return max(s.mean((2, 5)) * 100000, s.mean((1, 3)) * 12 * wage)
    return max(s.mean((1, 3)) * 100000, s.mean((1, 2)) * 12 * wage)


#Criminal Code of Russia 291
def ru_bribe_fine(wage, bribe, is_in_coal=False):
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


def simulate(N, hierarchy, steal_fine_func, bribe_fine_func, reward_func):
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
            state_ut = init_money
            # print(x)
            
            if x == 1:
                # No inspection
                for off in hierarchy.officials:
                    u = off.wage + off.stealing
                    off.acc_win += u
                    state_ut -= u
                    # print("{}\t{}".format(off.hier_id, off.acc_win))

                hierarchy.inspector.acc_win += hierarchy.inspector.wage
                state_ut -= hierarchy.inspector.wage

                return state_ut
            else:
                # print("{}\t{}".format(inspected_off.hier_id, inspected_off.acc_win))

                if x == 2:
                    # No bribe
                    u = inspected_off.wage + inspected_off.kappa * inspected_off.stealing - steal_fine_func(inspected_off.wage, inspected_off.stealing)
                    inspected_off.acc_win += u
                    state_ut -= u

                    for off in set(hierarchy.officials) - {inspected_off}:
                        u = off.wage + off.stealing
                        off.acc_win += u
                        state_ut -= u

                    hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(inspected_off) + reward_func(inspected_off.stealing)
                    state_ut -= (hierarchy.inspector.wage + reward_func(inspected_off.stealing))

                    return state_ut
                elif x == 3:
                    # Rejected bribe
                    u = inspected_off.wage + inspected_off.kappa * inspected_off.stealing - (
                            inspected_off.bribe() + steal_fine_func(inspected_off.wage, inspected_off.stealing) +
                            bribe_fine_func(inspected_off.bribe()))
                    inspected_off.acc_win += u
                    state_ut -= u

                    for off in set(hierarchy.officials) - {inspected_off}:
                        u = off.wage + off.stealing
                        off.acc_win += u
                        state_ut -= u

                    hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(
                        inspected_off) + reward_func(inspected_off.stealing)

                    state_ut -= (hierarchy.inspector.wage + reward_func(inspected_off.stealing))

                    return state_ut
                elif x == 4:
                    # Accepted bribe
                    inspected_off.acc_win += inspected_off.wage + inspected_off.stealing - inspected_off.bribe()
                    state_ut -= (inspected_off.wage + inspected_off.stealing)

                    for off in set(hierarchy.officials) - {inspected_off}:
                        u = off.wage + off.stealing
                        off.acc_win += u
                        state_ut -= u

                    hierarchy.inspector.acc_win += hierarchy.inspector.wage + inspected_off.bribe() - (
                            hierarchy.inspector.inspection_cost_func(inspected_off) + hierarchy.inspector.coverup_cost_func(inspected_off.stealing))
                    state_ut -= hierarchy.inspector.wage

                    return state_ut
                else:
                    sum_coverup, sum_reward, sum_inspect = calc_coverup_reward_inspect(exposers)

                    if x == 5:
                        # Exposed, no bribe
                        u = inspected_off.wage + inspected_off.kappa * inspected_off.stealing - steal_fine_func(
                            inspected_off.wage, inspected_off.stealing)
                        inspected_off.acc_win += u
                        state_ut -= u

                        for exposer in exposers:
                            u = exposer.wage + exposer.kappa * exposer.stealing - exposer.theta * steal_fine_func(exposer.wage, exposer.stealing)
                            exposer.acc_win += u
                            state_ut -= u

                        for off in set(hierarchy.officials) - {inspected_off} - set(exposers):
                            u = off.wage + off.stealing
                            off.acc_win += u
                            state_ut -= u

                        hierarchy.inspector.acc_win += hierarchy.inspector.wage  + reward_func(inspected_off.stealing) + sum_reward - (
                            hierarchy.inspector.inspection_cost_func(inspected_off) + sum_inspect)
                        state_ut -= (hierarchy.inspector.wage + reward_func(inspected_off.stealing) + sum_reward)

                        return state_ut
                    elif x == 6:
                        # Exposed, rejected bribe
                        u = inspected_off.wage + inspected_off.kappa * inspected_off.stealing - (steal_fine_func(
                            inspected_off.wage, inspected_off.stealing) + inspected_off.bribe() + bribe_fine_func(inspected_off.bribe()))
                        inspected_off.acc_win += u
                        state_ut -= u


                        for exposer in exposers:
                            u = exposer.wage + exposer.kappa * exposer.stealing - exposer.theta * steal_fine_func(
                                exposer.wage, exposer.stealing)
                            exposer.acc_win += u
                            state_ut -= u

                        for off in set(hierarchy.officials) - {inspected_off} - set(exposers):
                            u = off.wage + off.stealing
                            off.acc_win += u
                            state_ut -= u

                        hierarchy.inspector.acc_win += hierarchy.inspector.wage + reward_func(inspected_off.stealing) + sum_reward - (
                            hierarchy.inspector.inspection_cost_func(inspected_off) + sum_inspect)
                        state_ut -= (hierarchy.inspector.wage + reward_func(inspected_off.stealing) + sum_reward)

                        return state_ut
                    elif x == 7:
                        # Exposed, accepted bribe
                        inspected_off.acc_win += inspected_off.wage + inspected_off.stealing - inspected_off.bribe()
                        # print("{}\t{}\t{}\t{}".format(inspected_off.stealing, inspected_off.bribe(), inspected_off.wage, inspected_off.acc_win))
                        state_ut -= (inspected_off.wage + inspected_off.stealing)

                        for off in set(hierarchy.officials) - {inspected_off}:
                            u = off.wage + off.stealing
                            off.acc_win += u
                            state_ut -= u

                        hierarchy.inspector.acc_win += hierarchy.inspector.wage + inspected_off.bribe() - (hierarchy.inspector.inspection_cost_func(
                            inspected_off) + hierarchy.inspector.coverup_cost_func(inspected_off.stealing) + sum_coverup + sum_inspect)
                        state_ut -= hierarchy.inspector.wage

                        return state_ut

        # Stealing stage
        for off_level in hierarchy.scheme.values():
            cutoff_value = hierarchy.cutoff_values[off_level]
            optimal_stealing = (cutoff_value[0] - cutoff_value[1]) / len(off_level)
            for off in off_level:
                stealing[off_level] += hierarchy.get_with_id(off).steal(optimal_stealing)

        # Inspection stage: from top to bottom, from left to right

        for off_level in stealing:
            sum_stealing += stealing[off_level]
            if true_with_prob(1 - sum_stealing / init_money):
                pass
            else:
                inspected_off = hierarchy.get_with_id(r.choice(off_level))
                action = inspected_off.action
                if action == "NB":
                    acc_state_util += end(2)
                    break
                if action == "B":
                    acc_part_util = inspected_off.bribe() - hierarchy.inspector.coverup_cost_func(inspected_off.stealing)
                    rej_part_util = reward_func(inspected_off.stealing)
                    if acc_part_util <= rej_part_util:
                        acc_state_util += end(3)
                    else:
                        acc_state_util += end(4)
                    break
                if action == "E":
                    while True:
                        exposers.append(inspected_off)
                        inspected_off = hierarchy.get_boss_of_id(inspected_off.hier_id)
                        action = inspected_off.action
                        if action == "NB":
                            acc_state_util += end(5)
                            break
                        if action == "B":
                            exposers_coverup, exposers_reward, exposers_inspect = calc_coverup_reward_inspect(exposers)
                            acc_part_util = inspected_off.bribe() - hierarchy.inspector.coverup_cost_func(
                                inspected_off.stealing) - exposers_coverup
                            rej_part_util = reward_func(inspected_off.stealing) + exposers_reward
                            if acc_part_util <= rej_part_util:
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


def run_5_str(off_scheme, in_and_out_values, funcs, b12s, b3s):
    def level_12_official(hier_id, strat):
        return Official(hier_id=hier_id, wage=40000, strategy=strat, kappa=0.3, theta=0.01)

    def level_3_official(hier_id, strat):
        return Official(hier_id=hier_id, wage=90000, strategy=strat, kappa=0.6, theta=1)

    def build_hier(str1, str2):
        offs = [
            level_3_official((3, 0), str2), level_3_official((3, 1), str2),
            level_12_official((2, 0), str1), level_12_official((2, 1), str1),
            level_12_official((1, 0), str1), level_12_official((1, 1), str1)
        ]
        return offs

    for b12 in b12s:
        for b3 in b3s:
            print("({},{})".format(b12, b3))
            off_hiers = [build_hier(("Opt", "E", b12), ("Opt", "B", b3)),
                         build_hier(("Opt", "B", b12), ("Opt", "B", b3)),
                         build_hier(("None", "NB", b12), ("Opt", "B", b3)),
                         build_hier(("Opt", "B", b12), ("None", "NB", b3)),
                         build_hier(("None", "NB", b12), ("None", "NB", b3)),
                         ]

            for off_hier in off_hiers:
                inspector = Inspector(70000, inspection_cost_func_example, funcs[0])
                hierarchy = Hierarchy(off_scheme, off_hier, in_and_out_values, inspector)
                simulate(N=500000, hierarchy=hierarchy, steal_fine_func=ru_steal_fine,
                         bribe_fine_func=ru_bribe_fine, reward_func=funcs[1])


def main():
    strategies = (("None", "NB", 0), ("Opt", "E", 0), ("Opt", "B", 0.99))

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

    b12s_def = (0.1805, 0.361, 0.5415)
    b3s_def = (0.08675, 0.1735, 0.2185, 0.2635, 0.39525)

    b12s_s1 = (0.4605, 0.921, 1.3815)
    b3s_s1 = (0.742142857, 1.484285714, 1.599285714, 1.714285714, 2.571428571)

    b12s_s2 = (0.4605, 0.921, 1.3815)
    b3s_s2 = (3, 6, 6.115, 6.23, 9.345)

    b12s_s3 = (11.9999999, 23.99999981, 35.99999971)
    b3s_s3 = (5.7505, 11.501, 14.50087498, 17.50074995, 26.25112493)

    #Top b by 1

    b12s_1_s1 = (0.63075, 0.841)
    b3s_1_s1 = (0.395, 0.79, 0.895, 1)

    b12s_1_s3 = (0.5, 1)
    b3s_1_s3 = (0.375125, 0.75025, 0.875125, 1)

    ###

    b12_def_1 = (0.361,)
    b3_def_1 = (0.2635,)

    b12_s1_1 = (0.921,)
    b3_s1_1 = (1.714285714,)

    b12_s2_1 = (0.921,)
    b3_s2_1 = (6.23,)

    b12_s3_1 = (23.99999981,)
    b3_s3_1 = (17.50074995,)

    b12_z1_1 = (0.841,)
    b3_z1_1 = (1,)

    b12_z3_1 = (1,)
    b3_z3_1 = (1,)


    run_5_str(off_scheme=off_scheme, in_and_out_values=in_and_out_values, funcs=(coverup_cost_func_def, reward_func_def), b12s=b12_z3_1, b3s=b3_z3_1)


if __name__ == "__main__":
    main()
