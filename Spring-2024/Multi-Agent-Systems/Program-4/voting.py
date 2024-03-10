
import numpy
from copy import deepcopy

CAND = 0  # subscript of list which represents the candidate
SCORE = 1  # subscript of list which represents the score of the candidate
PLACE = 2  # subscript of list which represents the ranking, lowest is best

def print_connections(names, c, voters, candidates):
    print("CONNECTIONS")
    for i in range(voters):
        print("%10s" % (names[i]), end=" ")
        for j in range(voters):
            print(c[i][j], end=' ')
        print()


def print_rankings(names, r, voters, candidates, ordered):
    print("CANDIDATE Rankings")
    for i in range(voters):
        #print("First choice for {} is {}".format(names[i], ordered[i][CAND]), end=" ")
        print(names[i], end=" ")
        for j in range(candidates):
            print(r[i][j], end='')
        print(" ORDER ", ordered[i])


def create_voting(voters, candidates):
    names = ["Alice ", "Bart  ", "Cindy ", "Darin ", "Elmer ", "Finn  ", "Greg  ", "Hank  ", "Ian   ", "Jim   ",
             "Kate  ", "Linc  ", "Mary  ", "Nancy ", "Owen  ", "Peter ", "Quinn ", "Ross  ", "Sandy ", "Tom   ",
             "Ursula", "Van   ", "Wendy ", "Xavier", "Yan   ", "Zach  "]

    connections = [[0 for i in range(voters)] for j in range(voters)]
    ordered = [[] for i in range(voters)]
    numpy.random.seed(1052)
    for i in range(voters):
        conn = round(numpy.random.uniform(0, voters / 2))
        for j in range(conn):
            connectTo = numpy.random.randint(0, voters)
            if (connectTo!=i):
                connections[i][connectTo] = 1
    print_connections(names, connections, voters, candidates)
    candidateRanking = [[list() for i in range(candidates)] for j in range(voters)]
    for i in range(voters):
        for j in range(candidates):
            candidateRanking[i][j] = [j + 1, round(numpy.random.uniform(0, 100)) / 10, 0]
        # print(candidateRanking[i])
        s = sorted(candidateRanking[i], reverse=True, key=lambda v: v[SCORE])
        ordered[i] = [s[i][CAND] for i in range(candidates)]
        for v in range(candidates):
            candidate = s[v][CAND] - 1  # which candidate has rank v+1
            candidateRanking[i][candidate][PLACE] = v + 1
    # Store voter's most preferred candidate
    preferred = [i[0] for i in ordered]
    print_rankings(names, candidateRanking, voters, candidates, ordered)
    # Part 1
    ranked_choice_voting(names, candidateRanking, connections, deepcopy(ordered), preferred, voters, part_two = False)
    # Part 2
    ranked_choice_voting(names, candidateRanking, connections, deepcopy(ordered), preferred, voters, part_two = True)


# TODO: Using Ranked Choice voting (described above), list the order in which candidates are eliminated. Output the winner using ranked choice voting
def ranked_choice_voting(names, ranking, connections, ordered, preferred, voters, part_two):
    eliminated_order = list()
    majority = 0.5
    winner_pct = 0
    part = 1
    orig_preferred = deepcopy(preferred)
    while winner_pct < majority:
        if part_two:
            ordered = social_network(names, ranking, connections, ordered, preferred, voters)
            part = "2 - Social Network"
        results = dict()
        for r in ordered:
            candidate = r[0]
            if candidate in results:
                results[candidate] += 1
            else:
                results[candidate] = 1
        biggest_loser = min(results, key=results.get)
        winner = max(results, key=results.get)
        # Remove biggest loser
        for r in ordered:
            r.remove(biggest_loser)
        # Calculated winner percentage
        winner_pct = results[winner] / voters
        eliminated_order.append(biggest_loser)
    print(f"\nRANKED CHOICE VOTING: Part {part}", "\nWinner:", winner, "\nOrder candidates were eliminated:", eliminated_order)
    social_welfare(winner, names, ranking, voters, orig_preferred, part)
    return

# TODO: Output the social welfare for the system given the winner using both cardinal and ordinal utility
def social_welfare(winner, names, ranking, voters, preferred, part):
    print(f"\nSOCIAL WELFARE: Part {part}")
    system_cardinal = 0
    system_ordinal = 0
    for i in range(voters):
        # Calculate cardinal utility
        voter = names[i]
        candidate_ranking = ranking[i]
        prefer = preferred[i]
        for j in candidate_ranking:
            if j[0] == winner:
                winner_cardinal = j[1]
                winner_ordinal = j[2]
            elif j[0] == prefer:
                prefer_cardinal = j[1]
                prefer_ordinal = j[2]
        cardinal = round(abs(prefer_cardinal - winner_cardinal), 1)
        ordinal = abs(prefer_ordinal - winner_ordinal)

        system_cardinal += cardinal
        system_ordinal += ordinal
        print(voter, "Cardinal utility:", cardinal, "Ordinal utility:", ordinal)
    print("\nSystem cardinal utility:", round(system_cardinal, 1), "System ordinal utility:", system_ordinal, "\n")
    return

# TODO: Using the social network model, show how many voters change their mind at each round.
"""
    RULES:
    O   (1) Voters who have the least amount of friends will vote first.
    X   (2) Voters will change their vote only if a majority of their friends support a certain candidate
            and if that candidate is one of their top 3 candidates else their vote will remain the same.
    X   (3) If a voter changes their preferred choice, then all voters preferences should be updated.
"""

def social_network(names, ranking, connections, ordered, preferred, voters):
    social_info = map_voters_to_friends(connections, ordered, preferred, voters)
    changed_mind = list()
    # Sort voters by number of friends
    for k, v in social_info.items():
        top_3 = v["candidate_order"][:3]
        num_friends = len(v["friends"])
        friend_preferences = dict()
        for i in v["friends"]:
            c = i["candidate"]
            if c not in friend_preferences:
                friend_preferences[c] = 1
            else:
                friend_preferences[c] += 1
        most_pref = max(friend_preferences, key=friend_preferences.get)
        majority_pct = friend_preferences[most_pref]/num_friends
        if majority_pct == 0.50 and len(friend_preferences) == 2 and most_pref in top_3:
            keys = list(friend_preferences)
            if keys[0] in top_3 and keys[1] in top_3:
                position1 = top_3.index(keys[0])
                position2 = top_3.index(keys[1])
                # The majority of friends want the voter's top candidate
                if position1 != 0 and position2 != 0:
                    change_preference = min(position1, position2)
                    print("change mind0")
        elif majority_pct >= 0.50 and most_pref in top_3:
            changed_mind.append(names[k])
            # Change preference and order
            ordered[k].remove(most_pref)
            ordered[k].insert(0, most_pref)
            preferred[k] = most_pref
    print("Changed their minds", changed_mind)
    return ordered

def map_voters_to_friends(connections, ordered, preferred, voters):
    social_info = dict()
    # Map friend preferences to voters
    for i in range(voters):
        social_info[i] = {"friends": [], "candidate": preferred[i], "candidate_order": ordered[i]}
        for j in range(voters):
            friend = connections[i][j]
            if friend:
                social_info[i]["friends"].append({"friend": j, "candidate": preferred[j]})
    return social_info

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_voting(20, 5)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Python code to demonstrate namedtuple()
