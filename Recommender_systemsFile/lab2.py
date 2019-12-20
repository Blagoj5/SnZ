from math import sqrt

def sim_pearson(prefs, p1, p2):
    """
    Го враќа коефициентот на Пирсонова корелација помеѓу p1 и p2 (личност1 и личност 2).
    Вредностите се помеѓу -1 и 1
    :param prefs: речник со оцени од корисници
    :param p1: име на корисник1
    :param p2: име на корисник2
    :return: сличност помеѓу корисник1 и корисник2
    """
    # Се креира речник во кој ќе се чуваат предметите кои се оценети од двајцата
    # Во речникот ни се важни само клучевите за да ги чуваме имињата на филмовите
    # кои се заеднички, а вредностите не ни се важни
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # Се пресметува бројот на предмети оценети од двајцата
    n = len(si)

    # Ако немаат заеднички предмети, врати корелација 0
    if n == 0:
        return 0

    # Собери ги сите оцени за секоја личност посебно
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Собери ги квадратите од сите оцени за секоја личност посебно
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    # Собери ги производите од оцените на двете личности
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Пресметај го коефициентот на корелација
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r

def get_recommendations(prefs, person, similarity=sim_pearson):
    """
    Ги враќа препораките за даден корисник со користење на тежински просек
    со оцените од другите корисници
    :param prefs: речник со оцени од корисници
    :param person: име на корисник
    :param similarity: метрика за сличност
    :return: препораки за даден корисник
    """
    totals = {}
    simSums = {}
    for other in prefs:
        # За да не се споредува со самиот себе
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        # не се земаат предвид резултати <= 0
        if sim <= 0:
            continue
        for item in prefs[other]:
            # за тековниот корисник ги земаме само филмовите што ги нема гледано
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

                # Сума на сличности
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Креирање на нормализирана листа со рејтинзи
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    # Сортирање на листата во растечки редослед. Превртување на листата за најголемите вредности да бидат први
    rankings.sort(reverse=True)

    return rankings[:3]

ratings = {
    'Lisa Rose': {'Catch Me If You Can': 3.0 , 'Snakes on a Plane': 3.5, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0, 'Snitch': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5,  'The Night Listener': 3.0,'You, Me and Dupree': 3.5},
    'Michael Phillips': {'Catch Me If You Can': 2.5, 'Lady in the Water': 2.5,'Superman Returns': 3.5, 'The Night Listener': 4.0, 'Snitch': 2.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,'The Night Listener': 4.5, 'Superman Returns': 4.0,'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,'Just My Luck': 2.0, 'Superman Returns': 3.0, 'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Catch Me If You Can': 4.5, 'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5, 'Snitch': 4.5},
    'Toby': {'Snakes on a Plane':4.5, 'Snitch': 5.0},
    'Michelle Nichols': {'Just My Luck' : 1.0, 'The Night Listener': 4.5, 'You, Me and Dupree': 3.5, 'Catch Me If You Can': 2.5, 'Snakes on a Plane': 3.0},
    'Gary Coleman': {'Lady in the Water': 1.0, 'Catch Me If You Can': 1.5, 'Superman Returns': 1.5, 'You, Me and Dupree': 2.0},
    'Larry': {'Lady in the Water': 3.0, 'Just My Luck': 3.5, 'Snitch': 1.5, 'The Night Listener': 3.5}
    }


if __name__ == '__main__':
    test_users = list(input().split(", "))
        
    test_mnoz = {}
    for test_user in test_users:
        for user_k, user_v in ratings.items():
            if user_k == test_user:
                test_mnoz[user_k] = user_v
        del ratings[test_user]


    for test_user in test_users:
        ratings[test_user] = test_mnoz[test_user]
        final = get_recommendations(ratings, test_user)
        #  OVA GO PRAM SO CEL DA SE ZNAJ KOJ E POSLEDEN ELEMENT ZA DA GO OSTRANAM ; OD POSLEDNIOT ELEMENT
        empty_str = ''
        size = 0
        if final:
            for i in final:
                if size == len(final)-1:
                    empty_str += f'{i[1]}'
                else:
                    empty_str += f'{i[1]}; '
                size += 1
        else:
            empty_str = 'no recommendations ...'    
        print(f'{test_user}: {empty_str}')
        del ratings[test_user]






    

# Потребно е да изградите систем за препорака на филмови за корисниците. Најпрво поделете го иницијалното множество на множество за тренирање и множество за тестирање, 
# така што множеството за тестирање ќе биде составено од корисниците проследени на стандарден влез, додека множеството за тренирање 
# ги вклучува сите останати корисници.

# При давањето на препорака за даден корисник од тестирачкото множество, потребно е множеството за тренирање да не ги содржи корисниците 
# од тестирачкото множество, освен моменталниот корисник за кој се изведува препораката (кој треба да е вклучен во множеството при одредување
#  на препораките). Пример: доколку корисниците 1, 2, 3 се дел од тестирачкото множество потребно е при предвидување на препорака на 
#  корисникот 1 од целокупното множество со сите корисници да не се земаат во предвид корисниците 2 и 3, при препорака за корисникот 2 
#  не треба да се земаат во предвид корисниците 1 и 3, а при препорака на корисникот 3 не треба да се земаат во предвид корисниците 1 и 2 
#  соодветно.

# На стандарден излез испринтајте ги првите три препораки за музичките изведувачи за секој од корисниците во множеството за тестирање.
#  Користете систем за препорака базиран на корисниците и Пирсонова корелација.