import random as r


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
        #coal_id

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
            print(boss)
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


def ru_fine(wage, stealing, bribe):
    return 0


def ru_reward(stealing):
    return 0


def inspection_cost_func_example(off):
    return 0


def coverup_cost_func_example(off):
    return 0


def simulate(N, hierarchy, fine_func, reward_func):
    # Play the game N times.
    M_start = list(hierarchy.cutoff_values.values())[0][0]
    M_left = M_start
    stealing = {}
    for off_level in hierarchy.scheme.values():
        stealing[off_level] = 0

    # Stealing stage
    for off_level in hierarchy.scheme.values():
        cutoff_value = hierarchy.cutoff_values[off_level]
        optimal_stealing = (cutoff_value[0] - cutoff_value[1]) / len(off_level)
        for off in off_level:
            stealing[off_level] += hierarchy.get_with_id(off).steal(optimal_stealing)

    inspected_off = None
    exposers = []

    def end(x):
        if x == 1:
            # No inspection
            for official in hierarchy.officials:
                official.acc_win += official.wage + official.stealing

            hierarchy.inspector.acc_win += hierarchy.inspector.wage
        elif x == 2:
            # No bribe
            inspected_off.acc_win += inspected_off.wage + inspected_off.kappa * inspected_off.stealing - fine_func(inspected_off.wage, inspected_off.stealing, inspected_off.bribe())

            for official in set(hierarchy.officials) ^ set(inspected_off, ):
                official.acc_win += official.wage + official.stealing

            hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(inspected_off.wage) + reward_func(inspected_off.stealing)
        elif x == 3:
            # Rejected bribe
            inspected_off.acc_win += inspected_off.wage + inspected_off.kappa * inspected_off.stealing - (
                    inspected_off.bribe() + fine_func(inspected_off.wage, inspected_off.stealing,
                                                      inspected_off.bribe()))

            for official in set(hierarchy.officials) ^ set(inspected_off, ):
                official.acc_win += official.wage + official.stealing

            hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(
                inspected_off.wage) + inspected_off.bribe() - hierarchy.inspector.coverup_cost_func(
                inspected_off.stealing)
        elif x == 4:
            # Accepted bribe
            inspected_off.acc_win += inspected_off.wage + inspected_off.stealing - inspected_off.bribe()

            for official in set(hierarchy.officials) ^ set(inspected_off, ):
                official.acc_win += official.wage + official.stealing

            hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(
                inspected_off.wage) + inspected_off.bribe()
        elif x == 5:
            # Exposed, no bribe
            inspected_off.acc_win += inspected_off.wage + inspected_off.kappa * inspected_off.stealing - fine_func(
                inspected_off.wage, inspected_off.stealing, inspected_off.bribe())

            for exposer in exposers:
                exposer.acc_win += 0

            for official in set(hierarchy.officials) ^ set(inspected_off, ) ^ set(exposers):
                official.acc_win += official.wage + official.stealing

            hierarchy.inspector.acc_win += hierarchy.inspector.wage - hierarchy.inspector.inspection_cost_func(
                inspected_off.wage) + reward_func(inspected_off.stealing)
        elif x == 6:
            # Exposed, rejected bribe
            pass
        elif x == 7:
            # Exposed, accepted bribe
            pass

    # Inspection stage: from top to bottom, from left to right
    for off_level in stealing:
        M_left -= stealing[off_level]
        if true_with_prob(1 - M_left / M_start):
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
                        exposers_coverup = 0
                        exposers_reward = 0

                        for exposer in exposers:
                            exposers_coverup += hierarchy.inspector.coverup_cost_func(exposer.stealing)
                            exposers_reward += reward_func(exposer.stealing)

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

    # End of N cycles, Results (acc_win / N )
    # for official in hierarchy.officials:
    #     print("{}\n{}".format(official.hier_id, official.acc_win))
    # print("Inspector\n{}".format(hierarchy.inspector.acc_win))


def main():
    strategies = (("None", "NB", 0), ("Opt", "E", 0), ("Opt", "B", 0.99))

    def level_1_official(hier_id):
        return Official(hier_id=hier_id, wage=40000, strategy=("Opt", "E", 0.5), kappa=0.3, theta=0.01)

    def level_2_official(hier_id):
        return Official(hier_id=hier_id, wage=90000, strategy=("Opt", "B", 0.25), kappa=0.6, theta=1)

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

    inspector = Inspector(70000, inspection_cost_func_example, coverup_cost_func_example)

    hier = Hierarchy(off_scheme, officials, cutoff_values, inspector)

    simulate(N=100, hierarchy=hier, fine_func=ru_fine, reward_func=ru_reward)


if __name__ == "__main__":
    main()

