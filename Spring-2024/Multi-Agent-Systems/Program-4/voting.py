
import numpy

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
    preferred = [i[0] for i in ordered]
    print_rankings(names, candidateRanking, voters, candidates, ordered)
    winner = ranked_choice_voting(voters, ordered)
    social_welfare(winner, names, candidateRanking, voters, preferred)


# TODO: Using Ranked Choice voting (described above), list the order in which candidates are eliminated. Output the winner using ranked choice voting
def ranked_choice_voting(voters, ordered):
    eliminated_order = list()
    majority = 0.5
    winner_pct = 0
    while winner_pct < majority:
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
    print("\nRANKED CHOICE VOTING", "\nWinner:", winner, "\nOrder candidates were eliminated:", eliminated_order)
    return winner

# TODO: Output the social welfare for the system given the winner using both cardinal and ordinal utility
def social_welfare(winner, names, ranking, voters, preferred):
    print("\nSOCIAL WELFARE")
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
    print("\nSystem cardinal utility:", round(system_cardinal, 1), "System ordinal utility:", system_ordinal)
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_voting(20, 5)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Python code to demonstrate namedtuple()
