from math import sqrt

def sim_distance(prefs, person1, person2):
    """
    Враќа мерка за сличност базирана на растојание помеѓу person1 и person2
    :param prefs: речник со оцени од корисници
    :param person1: име на корисник1
    :param person2: име на корисник2
    :return: сличност помеѓу корисник1 и корисник2
    """
    # Се прави листа на заеднички предмети
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    # Ако немаат заеднички рејтинзи, врати 0
    if len(si) == 0:
        return 0
    # Собери ги квадратите на сите разлики
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sqrt(sum_of_squares))



movie_reviews = {
    'Lisa Rose': {'Catch Me If You Can': 3.0, 'Snakes on a Plane': 3.5, 'Superman Returns': 3.5,
                  'You, Me and Dupree': 2.5, 'The Night Listener': 3.0, 'Snitch': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'The Night Listener': 3.0,
                     'You, Me and Dupree': 3.5},
    'Michael Phillips': {'Catch Me If You Can': 2.5, 'Lady in the Water': 2.5, 'Superman Returns': 3.5,
                         'The Night Listener': 4.0, 'Snitch': 2.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0,
                     'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0,
                     'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Catch Me If You Can': 4.5, 'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5, 'Snitch': 4.5},
    'Toby': {'Snakes on a Plane': 4.5, 'Snitch': 5.0},
    'Michelle Nichols': {'Just My Luck': 1.0, 'The Night Listener': 4.5, 'You, Me and Dupree': 3.5,
                         'Catch Me If You Can': 2.5, 'Snakes on a Plane': 3.0},
    'Gary Coleman': {'Lady in the Water': 1.0, 'Catch Me If You Can': 1.5, 'Superman Returns': 1.5,
                     'You, Me and Dupree': 2.0},
    'Larry': {'Lady in the Water': 3.0, 'Just My Luck': 3.5, 'Snitch': 1.5, 'The Night Listener': 3.5}
}


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
    together_film = 0
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
            together_film += 1


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
    return round(sim_distance(prefs, p1, p2), 3), round(r, 3), together_film

def tabela_na_slichni_korisnici(reviews, korisnik1, korisnik2):
    slicnosti = sim_pearson(reviews, korisnik1, korisnik2)    

    return slicnosti


if __name__ == "__main__":
    korisnik1 = input()
    korisnik2 = input()

    tabela = tabela_na_slichni_korisnici(movie_reviews, korisnik1, korisnik2)
    print(tabela)

# Дадено е множество кое е претставено како речник чиј клуч е името на корисникот и вредност како речник чиј клуч е 
# филмот, а вредност е оцената која корисникот ја дал за филмот. Да се напише функција која ќе генерира табела на слични
#  корисници претставена како речник од речници (клучеви се имињата на корисниците), така што за секој пар корисници ќе чува 
#  торка од сличност базирана на Пеарсонова корелација, сличност базирана на Евклидово растојание, и број на заеднички оцени 
# (оцени дадени за исти филмови). Вредностите да бидат заокружени на 3 децимали. За прочитани имиња на двајца корисници да се 
# испечати торката која се чува во генерираната табела.