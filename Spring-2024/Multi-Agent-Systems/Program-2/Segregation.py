
'''
Author : Adil Moujahid
Email : adil.mouja@gmail.com
Description: Simulations of Schelling's seggregation model

You will need to set up pycharm to import matplotlib.
'''

import matplotlib.pyplot as plt
import itertools
import random
import copy


class Schelling:
    def __init__(self, width, height, empty_ratio, similarity_threshold, n_iterations, neighborhood, colors=2):
        self.agents = None
        self.width = width
        self.height = height
        self.colors = colors
        self.empty_ratio = empty_ratio
        # self.similarity_threshold = similarity_threshold
        self.similarity_threshold = dict()
        self.n_iterations = n_iterations
        self.neighborhood = neighborhood
        # TODO: Add a feature where the similarity_threshold can be different for each of the colors
        for c in range(colors):
            self.similarity_threshold[c + 1] = similarity_threshold[c]

    def populate(self):
        self.choices = {0: "empty_house", 1: "swap_house"}
        self.empty_houses = []
        self.willing_to_swap = []
        self.agents = {}
        print("Populate ",  self.width ,  self.height)
        self.all_houses = list(itertools.product(range(self.width), range(self.height)))
        print(self.all_houses)
        random.shuffle(self.all_houses)


        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        self.empty_houses = self.all_houses[:self.n_empty]
        #print(self.empty_houses)

        self.remaining_houses = self.all_houses[self.n_empty:]
        houses_by_color = [self.remaining_houses[i::self.colors] for i in range(self.colors)]
        print("Houses by color ", houses_by_color[0])
        for i in range(self.colors):
            # create agents for each color
            dict2 = dict(zip(houses_by_color[i], [i + 1] * len(houses_by_color[i])))
            self.agents = {**self.agents, **dict2}
        print("dictionary",self.agents)

    def is_unsatisfied(self, x, y):

        myColor = self.agents[(x, y)]
        count_similar = 0
        count_different = 0

        if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
            if self.agents[(x - 1, y - 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if y > 0 and (x, y - 1) not in self.empty_houses:
            if self.agents[(x, y - 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
            if self.agents[(x + 1, y - 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and (x - 1, y) not in self.empty_houses:
            if self.agents[(x - 1, y)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
            if self.agents[(x + 1, y)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses:
            if self.agents[(x - 1, y + 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
            if self.agents[(x, y + 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1
        if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
            if self.agents[(x + 1, y + 1)] == myColor:
                count_similar += 1
            else:
                count_different += 1

        if (count_similar + count_different) == 0:
            return False
        else:
            return float(count_similar) / (count_similar + count_different) < self.similarity_threshold[myColor]

    def move_locations(self):
        total_distance=0
        self.prev_temp_dict = dict()
        temp_dict = dict()
        keep_iterating = True
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            total = 0
            satisfied = 0

            for agent in self.old_agents:
                agent_color = self.agents[agent]
                is_unsatisfied = self.is_unsatisfied(agent[0], agent[1])
                if is_unsatisfied:
                    choice = "empty_house"
                    house_outside_neighborhood = True
                    if len(self.willing_to_swap) > 2:
                        choice = random.choice(self.choices)
                    # TODO: Add a feature where agents can improve on their current location by performing a location swap with another agent who is willing to swap
                    if choice == "swap_house":
                        # TODO: e.	Add a feature where you prefer to move to locations in the neighborhood.  The idea is that a move may be cheaper if the agent didn’t move as far.
                        i = 0
                        while house_outside_neighborhood and i < 20:
                            swapping_house_with = random.choice(self.willing_to_swap)
                            house_swap_location = abs(swapping_house_with[0] - agent[0]) + abs(swapping_house_with[1] - agent[1])
                            if house_swap_location <= self.neighborhood:
                                house_outside_neighborhood = False
                                swapping_agent_color = self.agents[swapping_house_with]
                                if swapping_agent_color != agent_color:
                                    self.agents[swapping_house_with] = agent_color
                                    self.agents[agent] = swapping_agent_color
                                    total_distance += abs(swapping_house_with[0] - agent[0]) + abs(swapping_house_with[1] - agent[1])
                                    if not self.is_unsatisfied(swapping_house_with[0], swapping_house_with[1]):
                                        self.willing_to_swap.remove(swapping_house_with)
                                else:
                                    choice = "empty_house"
                            else:
                                house_outside_neighborhood = True

                            if i == 20:
                                choice = "empty_house"
                            i += 1

                    if choice == "empty_house":
                        while house_outside_neighborhood:
                            empty_house = random.choice(self.empty_houses)
                            empty_house_location = abs(empty_house[0] - agent[0]) + abs(empty_house[1] - agent[1])
                            if empty_house_location <= self.neighborhood:
                                house_outside_neighborhood = False
                                self.agents[empty_house] = agent_color
                                del self.agents[agent]
                                self.empty_houses.remove(empty_house)
                                self.empty_houses.append(agent)
                                total_distance += abs(empty_house[0] - agent[0]) + abs(empty_house[1] - agent[1])
                                if self.is_unsatisfied(empty_house[0], empty_house[1]):
                                    self.willing_to_swap.append(empty_house)
                            else:
                                house_outside_neighborhood = True

                    n_changes += 1
                # TODO: Add output to indicate the percentage of each agent type that meets the desired similarity_threshold
                if agent_color not in temp_dict:
                    temp_dict[agent_color] = { "met_threshold": 0, "total": 0 }
                temp_dict[agent_color]["total"] += 1
                total += 1
                if not is_unsatisfied:
                    temp_dict[agent_color]["met_threshold"] += 1
                    satisfied += 1
            self.willing_to_swap.clear()
            # TODO: Add a feature to stop when little progress is being made.  Print out a message to indicate how many iterations  you did.
            if len(self.prev_temp_dict) > 0:
                for color in self.prev_temp_dict:
                    current_percentage = temp_dict[color]['met_threshold']/temp_dict[color]['total']
                    prev_percentage = self.prev_temp_dict[color]['met_threshold']/self.prev_temp_dict[color]['total']
                    if current_percentage - prev_percentage < 0.0005:
                        keep_iterating = False
                        break
            if keep_iterating:
                if i%30==0:
                    print('Iteration: %d. Number of changes: %d total distance: %d' %(i+1,n_changes,total_distance))
                    for color in temp_dict:
                        print(f"\tColor {color} Similarity Ratio: {self.similarity_threshold[color]}, { str(round((temp_dict[color]['met_threshold']/temp_dict[color]['total']) * 100, 1)) }% met the similarity threshold.")
                        self.prev_temp_dict[color] = {"met_threshold": temp_dict[color]['met_threshold'], "total": temp_dict[color]['total']}
                if n_changes == 0:
                    break
            else:
                print("\t\tToo few changes. Number of iterations: " + str(i+1))
                break

    # def move_to_empty(self, x, y):
    #     color = self.agents[(x, y)]
    #     empty_house = random.choice(self.empty_houses)
    #     self.updated_agents[empty_house] = color
    #     del self.updated_agents[(x, y)]
    #     self.empty_houses.remove(empty_house)
    #     self.empty_houses.append((x, y))

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        # If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {1: 'b', 2: 'r', 3: 'g', 4: 'c', 5: 'm', 6: 'y', 7: 'k'}
        marker_size = 150/self.width  # no logic here, I just played around with it
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5,s=marker_size, color=agent_colors[self.agents[agent]])

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

    def calculate_similarity(self):
        similarity = []
        for agent in self.agents:
            count_similar = 0
            count_different = 0
            x = agent[0]
            y = agent[1]
            color = self.agents[(x, y)]
            if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
                if self.agents[(x - 1, y - 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if y > 0 and (x, y - 1) not in self.empty_houses:
                if self.agents[(x, y - 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
                if self.agents[(x + 1, y - 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and (x - 1, y) not in self.empty_houses:
                if self.agents[(x - 1, y)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
                if self.agents[(x + 1, y)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses:
                if self.agents[(x - 1, y + 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
                if self.agents[(x, y + 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
                if self.agents[(x + 1, y + 1)] == color:
                    count_similar += 1
                else:
                    count_different += 1
            try:
                similarity.append(float(count_similar) / (count_similar + count_different))
            except:
                similarity.append(1)
        return sum(similarity) / len(similarity)


def main():
    ##Starter Simulation
    schelling_0 = Schelling(5, 5, 0.3, [0.75, 0.5, .7], 200, 10, 3)
    schelling_0.populate()

    ##First Simulation
    schelling_1 = Schelling(50, 50, 0.3, [0.5, 0.8, 0.25], 200, 500, 3)
    schelling_1.populate()

    schelling_2 = Schelling(50, 50, 0.3, [0.35, 0.5, 0.6], 200, 100, 3)
    schelling_2.populate()

    schelling_3 = Schelling(50, 50, 0.3, [0.25, 0.55, 0.45], 200, 300, 3)
    schelling_3.populate()

    schelling_1.plot('Schelling Model with 2 colors: Initial State', 'files/schelling_2_initial.png')

    schelling_0.move_locations()
    schelling_1.move_locations()
    schelling_2.move_locations()
    schelling_3.move_locations()
    schelling_0.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 30%',
                     'files/schelling_0_30_final.png')
    schelling_1.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 30%',
                     'files/schelling_30_final.png')
    schelling_2.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 50%',
                     'files/schelling_50_final.png')
    schelling_3.plot('Schelling Model with 2 colors: Final State with Happiness Threshold 80%',
                     'files/schelling_80_final.png')

    # #Second Simulation Measuring Seggregation
    # similarity_threshold_ratio = {}
    # for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    #     schelling = Schelling(50, 50, 0.3, i, 500, 2)
    #     schelling.populate()
    #     schelling.update()
    #     similarity_threshold_ratio[i] = schelling.calculate_similarity()
    #
    # fig, ax = plt.subplots()
    # plt.plot(similarity_threshold_ratio.keys(), similarity_threshold_ratio.values(), 'ro')
    # ax.set_title('Similarity Threshold vs. Mean Similarity Ratio', fontsize=15, fontweight='bold')
    # ax.set_xlim([0, 1])
    # ax.set_ylim([0, 1.1])
    # ax.set_xlabel("Similarity Threshold")
    # ax.set_ylabel("Mean Similarity Ratio")
    # plt.savefig('schelling_segregation.png')


if __name__ == "__main__":
    main()