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


def ru_steal_fine(wage, stealing):
    if stealing == 0:
        return 0

    if stealing >= 7500000:
        return max(s.mean((200000, 500000)), wage * 24)
    return max(s.mean((100000, 300000)), wage * 18)


def ru_bribe_fine(bribe):
    mul = 0
    if bribe >= 1000000:
        mul = 80
    elif bribe >= 150000:
        mul = 70
    elif bribe >= 25000:
        mul = 45
    return bribe * mul


def threshold_func(stealing, thresholds):
    if stealing == 0:
        return 0

    for th in thresholds:
        if stealing >= th[0]:
            return th[1]


def reward_func_s1(stealing):
    return threshold_func(stealing, ((400000, 75000), (100000, 40000)))


def reward_func_s2(stealing):
    return threshold_func(stealing, ((400000, 300000), (100000, 40000)))


def reward_func_s3(stealing):
    return threshold_func(stealing, ((400000, 250000), (100000, 75000)))


def coverup_cost_func_s1(stealing):
    return threshold_func(stealing, ((400000, 11250), (100000, 5000)))


def coverup_cost_func_s2(stealing):
    return threshold_func(stealing, ((400000, 152500), (100000, 5000)))


def coverup_cost_func_s3(stealing):
    return threshold_func(stealing, ((400000, 123125), (100000, 49375)))


# Bind inspection and coverup costs to hier_id or to wage or to stealing?


def inspection_cost_func_example(off):
    if off.hier_id[0] >= 2:
        return 22500
    if off.hier_id[0] >= 1:
        return 10000


def simulate(N, hierarchy, steal_fine_func, bribe_fine_func, reward_func):
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
            if x == 1:
                # No inspection
                for official in hierarchy.officials:
                    official.acc_win += official.wage + official.stealing

                hierarchy.inspector.acc_win += hierarchy.inspector.wage
            else:
                # print("End {} with official {}.".format(x, inspected_off.hier_id))
                if x == 2:
                    # No bribe
                    inspected_off.acc_win += inspected_off.wage + inspected_off.kappa * inspected_off.stealing - steal_fine_func(inspected_off.wage, inspected_off.stealing)

                    for official in set(hierarchy.officials) ^ {inspected_off}:
                        official.acc_win += official.wage + official.stealing

                    hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(inspected_off) + reward_func(inspected_off.stealing)
                elif x == 3:
                    # Rejected bribe
                    inspected_off.acc_win += inspected_off.wage + inspected_off.kappa * inspected_off.stealing - (
                            inspected_off.bribe() + steal_fine_func(inspected_off.wage, inspected_off.stealing) +
                            bribe_fine_func(inspected_off.bribe()))

                    for official in set(hierarchy.officials) ^ {inspected_off}:
                        official.acc_win += official.wage + official.stealing

                    hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(
                        inspected_off) + inspected_off.bribe() - hierarchy.inspector.coverup_cost_func(
                        inspected_off.stealing)
                elif x == 4:
                    # Accepted bribe
                    inspected_off.acc_win += inspected_off.wage + inspected_off.stealing - inspected_off.bribe()

                    for official in set(hierarchy.officials) ^ {inspected_off}:
                        official.acc_win += official.wage + official.stealing

                    hierarchy.inspector.acc_win += hierarchy.inspector.wage + inspected_off.bribe() - (
                            hierarchy.inspector.inspection_cost_func(inspected_off) + hierarchy.inspector.coverup_cost_func(inspected_off.stealing))
                else:
                    sum_coverup, sum_reward, sum_inspect = calc_coverup_reward_inspect(exposers)

                    if x == 5:
                        # Exposed, no bribe
                        inspected_off.acc_win += inspected_off.wage + inspected_off.kappa * inspected_off.stealing - steal_fine_func(
                            inspected_off.wage, inspected_off.stealing)

                        for exposer in exposers:
                            exposer.acc_win += exposer.wage + exposer.kappa * exposer.stealing - exposer.theta * steal_fine_func(exposer.wage, exposer.stealing)

                        for official in set(hierarchy.officials) ^ {inspected_off} ^ set(exposers):
                            official.acc_win += official.wage + official.stealing

                        hierarchy.inspector.acc_win += hierarchy.inspector.wage  + reward_func(inspected_off.stealing) + sum_reward - (
                            hierarchy.inspector.inspection_cost_func(inspected_off) + sum_inspect)
                    elif x == 6:
                        # Exposed, rejected bribe
                        inspected_off.acc_win += inspected_off.wage + inspected_off.kappa * inspected_off.stealing - (steal_fine_func(
                            inspected_off.wage, inspected_off.stealing) + inspected_off.bribe() + bribe_fine_func(inspected_off.bribe()))

                        for exposer in exposers:
                            exposer.acc_win += exposer.wage + exposer.kappa * exposer.stealing - exposer.theta * steal_fine_func(
                                exposer.wage, exposer.stealing)

                        for official in set(hierarchy.officials) ^ {inspected_off} ^ set(exposers):
                            official.acc_win += official.wage + official.stealing

                        hierarchy.inspector.acc_win += hierarchy.inspector.wage + reward_func(inspected_off.stealing) + sum_reward - (
                            hierarchy.inspector.inspection_cost_func(inspected_off) + sum_inspect)
                    elif x == 7:
                        # Exposed, accepted bribe
                        inspected_off.acc_win += inspected_off.wage + inspected_off.stealing - inspected_off.bribe()

                        for official in set(hierarchy.officials) ^ {inspected_off}:
                            official.acc_win += official.wage + official.stealing

                        hierarchy.inspector.acc_win += hierarchy.inspector.wage + inspected_off.bribe() - (hierarchy.inspector.inspection_cost_func(
                            inspected_off) + hierarchy.inspector.coverup_cost_func(inspected_off.stealing) + sum_coverup + sum_inspect)

        # Stealing stage
        for off_level in hierarchy.scheme.values():
            cutoff_value = hierarchy.cutoff_values[off_level]
            optimal_stealing = (cutoff_value[0] - cutoff_value[1]) / len(off_level)
            for off in off_level:
                stealing[off_level] += hierarchy.get_with_id(off).steal(optimal_stealing)

        total_stealing = sum(stealing.values())

        # Inspection stage: from top to bottom, from left to right
        for off_level in stealing:
            sum_stealing += stealing[off_level]
            if true_with_prob(1 - sum_stealing / init_money):
                pass
            else:
                inspected_off = hierarchy.get_with_id(r.choice(off_level))
                action = inspected_off.action
                if action == "NB":
                    end(2)
                    break
                if action == "B":
                    acc_part_util = inspected_off.bribe() - hierarchy.inspector.coverup_cost_func(inspected_off.stealing)
                    rej_part_util = reward_func(inspected_off.stealing)
                    if acc_part_util <= rej_part_util:
                        end(3)
                    else:
                        end(4)
                    break
                if action == "E":
                    while True:
                        exposers.append(inspected_off)
                        inspected_off = hierarchy.get_boss_of_id(inspected_off.hier_id)
                        action = inspected_off.action
                        if action == "NB":
                            end(5)
                            break
                        if action == "B":
                            exposers_coverup, exposers_reward, exposers_inspect = calc_coverup_reward_inspect(exposers)
                            acc_part_util = inspected_off.bribe() - hierarchy.inspector.coverup_cost_func(
                                inspected_off.stealing) - exposers_coverup
                            rej_part_util = reward_func(inspected_off.stealing) + exposers_reward
                            if acc_part_util <= rej_part_util:
                                end(6)
                            else:
                                end(7)
                            break
                break

        if inspected_off is None:
            end(1)

    LoC = total_stealing / init_money



    # End of N cycles, Results
    for official in hierarchy.officials:
        print("{}".format(official.acc_win / N))
    print("{}".format(hierarchy.inspector.acc_win / N))

    print("\n{}".format(LoC))

    # for official in hierarchy.officials:
    #     print("{}\t{}".format(official.hier_id, official.acc_win / N))
    # print("Inspector\t{}".format(hierarchy.inspector.acc_win / N))


def main():
    strategies = (("None", "NB", 0), ("Opt", "E", 0), ("Opt", "B", 0.99))

    def level_1_official(hier_id):
        return Official(hier_id=hier_id, wage=40000, strategy=("Opt", "E", 1.0), kappa=0.3, theta=0.01)

    def level_2_official(hier_id):
        return Official(hier_id=hier_id, wage=90000, strategy=("Opt", "B", 1.0), kappa=0.6, theta=1)

    officials = [
        level_2_official((2, 0)), level_2_official((2, 1)),
        level_1_official((1, 0)), level_1_official((1, 1)),
        level_1_official((1, 2)), level_1_official((1, 3))
    ]
    off_scheme = {
        (3, 0): ((2, 0), (2, 1)),
        (2, 0): ((1, 0), (1, 1)),
        (2, 1): ((1, 2), (1, 3))
    }
    cutoff_values = {
        ((2, 0), (2, 1)): (3000000, 2000000),
        ((1, 0), (1, 1)): (2000000 / 2, 750000),
        ((1, 2), (1, 3)): (2000000 / 2, 750000)
    }

    inspector = Inspector(70000, inspection_cost_func_example, coverup_cost_func_s3)

    hierarchy = Hierarchy(off_scheme, officials, cutoff_values, inspector)

    simulate(N=100000, hierarchy=hierarchy, steal_fine_func=ru_steal_fine, bribe_fine_func=ru_bribe_fine, reward_func=reward_func_s3)


if __name__ == "__main__":
    main()

