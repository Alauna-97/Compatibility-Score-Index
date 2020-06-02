# user matrix
# [[personality, leadership, hobby ]  [gender, age, height] [ethnicity, education, occupation ]]

import math
from operator import itemgetter
import joblib
import spacy
import numpy
import tensorflow as tf
from difflib import SequenceMatcher
import en_core_web_lg
nlp = en_core_web_lg.load()
nlp = spacy.load('en_core_web_lg')


personality_wt = 5
leadership_wt = 5
hobby_wt = 5

democratic_meaning = "participative leadership or shared leadership,members of the group take a more participative role in the decision-making process"
autocratic_meaning = "authoritarian leadership, individual control over all decisions and little input from group members.rarely accept advice from followers"
laissez_faire_meaning = "delegative leadership,leaders are hands-off and allow group members to make the decisions.lowest productivity among group members"


ambivert_meaning = "normal overall behavior is between introversion and extroversion"
extrovert_meaning = "Their outgoing, vibrant nature draws people to them, and they have a hard time turning away the attention. They thrive off the interaction"
introvert_meaning = "Introverts tend to feel drained after socializing and regain their energy by spending time alone"


sports_meaning = "activity needing physical effort and skill that is played according to rules, for enjoyment or as a job"
music_meaning = "an art of sound in time that expresses ideas and emotions in significant forms through the elements of rhythm, melody, harmony, and color"
exercising_meaning = "activity requiring physical effort, carried out to sustain or improve health and fitness"
reading_meaning = "cognitive process of decoding symbols to derive meaning"
shopping_meaning = "Searching for or buying goods"
writing_meaning = "using symbols to communicate thoughts and ideas in a readable form "
dancing_meaning = "to move one's body, rhythmically in a pattern of steps"
arts_meaning = "expression of human creative skill and imagination"
watching_tv_meaning = "keep under attentive view or observation or view attentively with interest to a broadcast on television"


# matrix factorization function
def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.5):
    Q = Q.T
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * \
                            (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * \
                            (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P, Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
        if e < 0.001:
            break
    return P, Q.T


def get_leadership(arg1, arg2, wt):
    dict_leadership = {"democratic": democratic_meaning,
                       "autocratic": autocratic_meaning,
                       "laissez-faire": laissez_faire_meaning}

    def get_jaccard_sim(str1, str2):
        a = set(dict_leadership[str1].split())
        b = set(dict_leadership[str2].split())
        c = a.intersection(b)
        d = len(b)+len(a)
        return float(len(c)) / (d - len(c))

    def similar(str1, str2):
        return SequenceMatcher(None, dict_leadership[str1], dict_leadership[str2]).ratio()

#     def score_same_sim(type1_meaning,type2_meaning): #score_same_sim
#         meaning1= nlp(dict_leadership[type1_meaning])
#         remove_stop_words= [str(s) for s in meaning1 if not s.is_stop]
#         meaning2= nlp(dict_leadership[type2_meaning])
#         remove_stop_words2= [str(s) for s in meaning2 if not s.is_stop]
#         meaning1_no_stop_words = nlp(" ".join(remove_stop_words))
#         meaning2_no_stop_words = nlp(" ".join(remove_stop_words2))
#         return meaning1_no_stop_words.similarity( meaning2_no_stop_words)

    def score_same_sim(word, word2):
        leadership_meaning_lookup_democratic = {
            'autocratic': 0.83, 'laissez-faire': 0.85269}
        leadership_meaning_lookup_autocratic = {
            'democratic': 0.83, 'laissez-faire': 0.80558}
        leadership_meaning_lookup_laissez_faire = {
            'autocratic': 0.80558, 'democratic': 0.85269}

        data_dict = {'democratic': leadership_meaning_lookup_democratic, 'autocratic': leadership_meaning_lookup_autocratic,
                     'laissez-faire': leadership_meaning_lookup_laissez_faire}
        word = word.lower()
        word2 = word2.lower()
        result = data_dict[word]

        for i in result:
            if i == word2:
                return float(result[i])

    def score_same_sim2(word, word2):
        leadership_sim_lookup_democratic = {
            'autocratic': 0.5392, 'laissez-faire': 0.2681}
        leadership_sim_lookup_autocratic = {
            'democratic': 0.5392, 'laissez-faire': 0.41400838}
        leadership_sim_lookup_laissez_faire = {
            'autocratic': 0.41400838, 'democratic': 0.2681}

        data_dict = {'democratic': leadership_sim_lookup_democratic, 'autocratic': leadership_sim_lookup_autocratic,
                     'laissez-faire': leadership_sim_lookup_laissez_faire}
        word = word.lower()
        word2 = word2.lower()
        result = data_dict[word]

        for i in result:
            if i == word2:
                return float(result[i])

    def leadership_score(type1, type2, wt):
        return (score_same_sim(type1, type2)+score_same_sim2(type1, type2))/2 + similar(type1, type2) - (wt*get_jaccard_sim(type1, type2))

    if arg1 == "autocratic" and arg2 == "autocratic":
        return (leadership_score("autocratic", "laissez-faire", wt) + leadership_score("democratic", "autocratic", wt))/2
    if arg1 == "laissez-faire" and arg2 == "laissez-faire":
        return (leadership_score("autocratic", "laissez-faire", wt) + leadership_score("democratic", "laissez-faire", wt))/2
    if arg1 == "democratic" and arg2 == "democratic":
        return 1
    if arg1 == "laissez-faire" or arg2 == "laissez-faire":
        if arg1 == "laissez-faire":
            return leadership_score(arg2, arg1, wt)
        else:
            return leadership_score(arg1, arg2, wt)
    else:
        return leadership_score(arg1, arg2, wt)


def get_personality(arg1, arg2, wt):

    dict_psl = {"ambivert": ambivert_meaning,
                "extrovert": extrovert_meaning,
                "introvert": introvert_meaning}

    def get_jaccard_sim(str1, str2):
        a = set(dict_psl[str1].split())
        b = set(dict_psl[str2].split())
        c = a.intersection(b)
        d = len(b)+len(a)
        return float(len(c)) / (d - len(c))

    def similar(str1, str2):
        return SequenceMatcher(None, dict_psl[str1], dict_psl[str2]).ratio()

#     def score_same_sim(type1_meaning,type2_meaning): #score_same_sim
#         meaning1= nlp(dict_psl[type1_meaning])
#         remove_stop_words= [str(s) for s in meaning1 if not s.is_stop]
#         meaning2= nlp(dict_psl[type2_meaning])
#         remove_stop_words2= [str(s) for s in meaning2 if not s.is_stop]
#         meaning1_no_stop_words = nlp(" ".join(remove_stop_words))
#         meaning2_no_stop_words = nlp(" ".join(remove_stop_words2))
#         return meaning1_no_stop_words.similarity( meaning2_no_stop_words)
    def score_same_sim(word, word2):

        personality_meaning_lookup_ambivert = {
            'extrovert': 0.46623, 'introvert': 0.589395}
        personality_meaning_lookpup_extrovert = {
            'ambivert': 0.46623, 'introvert': 0.78617}
        personality_meaning_lookpup_introvert = {
            'ambivert': 0.589395, 'extrovert': 0.78617}

        data_dict = {'introvert': personality_meaning_lookpup_introvert, 'ambivert': personality_meaning_lookup_ambivert,
                     'extrovert': personality_meaning_lookpup_extrovert}
        word = word.lower()
        word2 = word2.lower()
        result = data_dict[word]

        for i in result:
            if i == word2:
                return float(result[i])

    def score_same_sim2(word, word2):
        personality_sim_lookup_ambivert = {
            'extrovert': 0.48455, 'introvert': 0.47561887}
        personality_sim_lookpup_extrovert = {
            'ambivert': 0.48455, 'introvert': 0.8067165}
        personality_sim_lookpup_introvert = {
            'ambivert': 0.47561887, 'extrovert': 0.8067165}

        data_dict = {'introvert': personality_sim_lookpup_introvert, 'ambivert': personality_sim_lookup_ambivert,
                     'extrovert': personality_sim_lookpup_extrovert}
        word = word.lower()
        word2 = word2.lower()
        result = data_dict[word]

        for i in result:
            if i == word2:
                return float(result[i])

    def personality_score(type1, type2, wt):
        return ((score_same_sim(type1, type2)+score_same_sim2(type1, type2))/2)+similar(type1, type2)-(wt*get_jaccard_sim(type1, type2))

    if arg1 == arg2 and arg1 == "ambivert":
        return (1 - personality_score("ambivert", "extrovert", wt)) + (1 - personality_score("ambivert", "introvert", wt))
    if arg1 == arg2 and arg1 == "extrovert":
        return (1 - personality_score("ambivert", "extrovert", wt)) + (1 - personality_score("extrovert", "introvert", wt))
    if arg1 == arg2 and arg1 == "introvert":
        return (1 - personality_score("ambivert", "introvert", wt)) + (1 - personality_score("extrovert", "introvert", wt))
    if arg1 == "introvert" or arg2 == "introvert":
        if arg1 == "introvert":
            return personality_score(arg2, arg1, wt)
        else:
            return personality_score(arg1, arg2, wt)
    if arg1 == "ambivert" or arg2 == "ambivert":
        if arg1 == "ambivert":
            return personality_score(arg1, arg2, wt)
        else:
            return personality_score(arg2, arg1, wt)


def get_hobby(arg1, arg2, wt):

    dict_hobby = {"sports": sports_meaning,
                  "music": music_meaning,
                  "exercising": exercising_meaning,
                  "reading": reading_meaning,
                  "shopping": shopping_meaning,
                  "writing": writing_meaning,
                  "dancing": dancing_meaning,
                  "arts": arts_meaning,
                  "watching-tv": watching_tv_meaning
                  }

    def get_jaccard_sim(str1, str2):
        a = set(dict_hobby[str1].split())
        b = set(dict_hobby[str2].split())
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    def similar(str1, str2):
        return SequenceMatcher(None, dict_hobby[str1], dict_hobby[str2]).ratio()

#     def score_same_sim(type1_meaning,type2_meaning): #score_same_sim
#         meaning1= nlp(dict_hobby[type1_meaning])
#         meaning2= nlp(dict_hobby[type2_meaning])
#         meaning1_no_stop_words = nlp(' '.join([str(t) for t in meaning1 if not t.is_stop]))
#         meaning2_no_stop_words = nlp(' '.join([str(t) for t in meaning2 if not t.is_stop]))
#         return meaning1_no_stop_words.similarity( meaning2_no_stop_words)

    def score_same_sim(word, word2):

        hobby_meaning_lookup_sports = {'music': 0.77, 'exercising': 0.87, 'reading': 0.613, 'shopping': 0.53,
                                       'writing': 0.64, 'dancing': 0.61, 'arts': 0.76, 'watching-tv': 0.6016}

        hobby_meaning_lookup_music = {'sports': 0.77, 'exercising': 0.69, 'reading': 0.647, 'shopping': 0.4467,
                                      'writing': 0.764, 'dancing': 0.753, 'arts': 0.752, 'watching-tv': 0.57}

        hobby_meaning_lookup_exercising = {'sports': 0.87, 'music': 0.69, 'reading': 0.59, 'shopping': 0.489,
                                           'writing': 0.56, 'dancing': 0.61, 'arts': 0.633, 'watching-tv': 0.55}

        hobby_meaning_lookup_reading = {'sports': 0.613, 'music': 0.647, 'exercising': 0.59, 'shopping': 0.344,
                                        'writing': 0.74, 'dancing': 0.53, 'arts': 0.612, 'watching-tv': 0.48}

        hobby_meaning_lookup_shopping = {'sports': 0.53, 'music': 0.4467, 'exercising': 0.489, 'reading': 0.344,
                                         'writing': 0.41, 'dancing': 0.33, 'arts': 0.35, 'watching-tv': 0.4}

        hobby_meaning_lookup_writing = {'sports': 0.64, 'music': 0.764, 'exercising': 0.56, 'reading': 0.74,
                                        'shopping': 0.41, 'dancing': 0.58, 'arts': 0.66, 'watching-tv': 0.582}

        hobby_meaning_lookup_dancing = {'sports': 0.61, 'music': 0.753, 'exercising': 0.61, 'reading': 0.53,
                                        'shopping': 0.33, 'writing': 0.58, 'arts': 0.534, 'watching-tv': 0.4132}

        hobby_meaning_lookup_arts = {'sports': 0.76, 'music': 0.752, 'exercising': 0.633, 'reading': 0.612,
                                     'shopping': 0.35, 'writing': 0.66, 'dancing': 0.534, 'watching-tv': 0.5}

        hobby_meaning_lookup_watch_tv = {'sports': 0.6016, 'music': 0.57, 'exercising': 0.55, 'reading': 0.48,
                                         'shopping': 0.4, 'writing': 0.582, 'dancing': 0.4132, 'arts': 0.5}

        data_dict = {'watching-tv': hobby_meaning_lookup_watch_tv, 'arts': hobby_meaning_lookup_arts,
                     'dancing': hobby_meaning_lookup_dancing, 'writing': hobby_meaning_lookup_writing, 'shopping': hobby_meaning_lookup_shopping,
                     'reading': hobby_meaning_lookup_reading, 'exercising': hobby_meaning_lookup_exercising,
                     'music': hobby_meaning_lookup_music, 'sports': hobby_meaning_lookup_sports}
        word = word.lower()
        word2 = word2.lower()
        result = data_dict[word]

        for i in result:
            if i == word2:
                return float(result[i])
    def score_same_sim2(word, word2):
        hobby_sim_lookup_sports = {'music': 0.3478885, 'exercising': 0.313734, 'reading': 0.2725, 'shopping': 0.36037,
                                   'writing': 0.2795706, 'dancing': 0.3233, 'arts': 0.46557, 'watching-tv': 0.4212}

        hobby_sim_lookup_music = {'sports': 0.3478885, 'exercising': 0.14, 'reading': 0.3018, 'shopping': 0.2290,
                                  'writing': 0.40106, 'dancing': 0.53523, 'arts': 0.43146, 'watching-tv': 0.40618}

        hobby_sim_lookup_exercising = {'sports': 0.314, 'music': 0.14, 'reading': 0.29, 'shopping': 0.224,
                                       'writing': 0.32, 'dancing': 0.33, 'arts': 0.24, 'watching-tv': 0.32588783}

        hobby_sim_lookup_reading = {'sports': 0.27, 'music': 0.3018, 'exercising': 0.29, 'shopping': 0.2715,
                                    'writing': 0.7029, 'dancing': 0.25, 'arts': 0.262, 'watching-tv': 0.5}

        hobby_sim_lookup_shopping = {'sports': 0.36037, 'music': 0.2290, 'exercising': 0.224, 'reading': 0.2715,
                                     'writing': 0.20046543, 'dancing': 0.26, 'arts': 0.31, 'watching-tv': 0.3049}

        hobby_sim_lookup_writing = {'sports': 0.2795706, 'music': 0.40106, 'exercising': 0.32, 'reading': 0.7029,
                                    'shopping': 0.20046543, 'dancing': 0.26433, 'arts': 0.4, 'watching-tv': 0.32}

        hobby_sim_lookup_dancing = {'sports': 0.3233, 'music': 0.53523, 'exercising': 0.33, 'reading': 0.25,
                                    'shopping': 0.26, 'writing': 0.26433, 'arts': 0.4, 'watching-tv': 0.5098276}

        hobby_sim_lookup_arts = {'sports': 0.46557, 'music': 0.43146, 'exercising': 0.24, 'reading': 0.262,
                                 'shopping': 0.31, 'writing': 0.4, 'dancing': 0.392, 'watching-tv': 0.21286}

        hobby_sim_lookup_watch_tv = {'sports': 0.4212, 'music': 0.40618, 'exercising': 0.32588783, 'reading': 0.5,
                                     'shopping': 0.3049, 'writing': 0.32, 'dancing': 0.5098276, 'arts': 0.21286}

        data_dict = {'watching-tv': hobby_sim_lookup_watch_tv, 'arts': hobby_sim_lookup_arts,
                     'dancing': hobby_sim_lookup_dancing, 'writing': hobby_sim_lookup_writing, 'shopping': hobby_sim_lookup_shopping,
                     'reading': hobby_sim_lookup_reading, 'exercising': hobby_sim_lookup_exercising,
                     'music': hobby_sim_lookup_music, 'sports': hobby_sim_lookup_sports}
        word = word.lower()
        word2 = word2.lower()
        result = data_dict[word]

        for i in result:
            if i == word2:
                return float(result[i])
    def hobby_score(type1, type2, wt):
        return (score_same_sim(type1, type2)+score_same_sim2(type1, type2))/2 + similar(type1, type2) - (wt*get_jaccard_sim(type1, type2))

    if arg1 == "watching-tv" or arg2 == "watching-tv":
        if arg1 == "watching-tv":
            if "reading and writing" in arg2:
                return (hobby_score("reading", arg1, wt) + hobby_score("writing", arg1, wt))/2
            return hobby_score(arg2, arg1, wt)
        else:
            if "reading and writing" in arg1:
                return (hobby_score("reading", arg2, wt) + hobby_score("writing", arg2, wt))/2
            return hobby_score(arg1, arg2, wt)
    if (arg1 == "sports" and arg2 == "exercising") or (arg2 == "sports" and arg1 == "exercising"):
        return 1
    if arg1 == arg2:
        return 1
    if (arg1 == "dancing" and arg2 == "music") or (arg1 == "dancing" and arg2 == "arts") or \
        (arg1 == "arts" and arg2 == "music") or (arg2 == "dancing" and arg1 == "music") or \
            (arg2 == "dancing" and arg1 == "arts") or (arg2 == "arts" and arg1 == "music"):
        return 1
    if "reading and writing" in arg1 or "reading and writing" in arg2:
        if "reading and writing" in arg1:
            return (hobby_score("reading", arg2, wt) + hobby_score("writing", arg2, wt))/2
        else:
            return (hobby_score(arg1, "reading", wt) + hobby_score(arg1, "writing", wt))/2
    else:
        return hobby_score(arg1, arg2, wt)


def age_cal(age, predicted_age, age_recieve):
    R = numpy.array([[age, predicted_age, 0], [age, age_recieve, 0]])
    N = len(R)
    M = len(R[0])
    K = 2

    P1 = numpy.array([[0.96618789, 0.28231824],
                      [0.29011499, 0.05317186]])
    Q1 = numpy.array([[0.50060064, 0.68964126],
                      [0.79024825, 0.60951225],
                      [0.10965169, 0.20230712]])

    nP, nQ = matrix_factorization(R, P1, Q1, K)
    nR = numpy.dot(nP, nQ.T)
    ratio = sum(nR[0]) / sum(nR[1])
    factorzd = nR[0][2] / nR[1][2]
    score2 = (factorzd + ratio)/2
    if predicted_age <= age_recieve:
        final = (numpy.dot(age, predicted_age) /
                 numpy.dot(age, age_recieve)) * score2
        return final
    else:
        final = (numpy.dot(age, age_recieve) /
                 numpy.dot(age, predicted_age)) * score2
        return final


def height_cal(height, predicted_ht, ht_recieve):
    R = numpy.array([[height, predicted_ht, 0], [height, ht_recieve, 0]])
    N = len(R)
    M = len(R[0])
    K = 2
    P1 = numpy.array([[0.96618789, 0.28231824],
                      [0.29011499, 0.05317186]])
    Q1 = numpy.array([[0.50060064, 0.68964126],
                      [0.79024825, 0.60951225],
                      [0.10965169, 0.20230712]])

    nP, nQ = matrix_factorization(R, P1, Q1, K)
    nR = numpy.dot(nP, nQ.T)
    ratio = sum(nR[0]) / sum(nR[1])
    factorzd = nR[0][2] / nR[1][2]
    score2 = (factorzd + ratio)/2
    maximum_height = 198
    minimum_height = 142
    total_height_levels = maximum_height-minimum_height
    if predicted_ht <= ht_recieve:
        level_num = ht_recieve-predicted_ht
        if level_num > 40:
            # set maximum height threshold
            final = (numpy.dot(height, predicted_ht) /
                     numpy.dot(height, ht_recieve)) * score2
            return (final * (total_height_levels-(40)))/total_height_levels
        else:
            final = (numpy.dot(height, predicted_ht) /
                     numpy.dot(height, ht_recieve)) * score2
            return (final * (total_height_levels-(level_num)))/total_height_levels

    else:
        final = (numpy.dot(height, predicted_ht) /
                 numpy.dot(height, ht_recieve)) * score2
        return (final * (total_height_levels-(predicted_ht-ht_recieve)))/total_height_levels

# argument 1 gender of the user
# argument 2 gender preference selected by the user {female,male,either}
# argument 3 gender of the potential match


def gender_cal(gender, pref_gender, rec_gender):
    if gender == "male" or gender == "female":
        if pref_gender == rec_gender:
            return 1
        if pref_gender == "either":
            return 1
        else:
            return 0
    else:
        return 0


def ethnicity_cal(userA_race, userA_ideal_match_race, userB_race):
    white = {"white": 100, "hispanic": 72,
             "chinese": 87, "indian": 87, "black": 79}
    chinese = {"white": 86, "chinese": 100,
               "hispanic": 69, "indian": 84, "black": 53}
    black = {"black": 100,  "indian": 70,
             "chinese": 53, "white": 76, "hispanic": 76}
    hispanic = {"white": 56, "chinese": 60,
                "indian": 60, "black": 50, "hispanic": 100}
    indian = {"white": 91, "hispanic": 77,
              "black": 70, "indian": 100, "chinese": 85}
    ethnicity_list = {"white": white, "chinese": chinese,
                      "black": black, "hispanic": hispanic, "indian": indian}
    # print(ethnicity_list)
    retrieve_ethnicity_dict = ethnicity_list[userA_ideal_match_race]
    # print(retrieve_ethnicity_dict)
    for i in retrieve_ethnicity_dict:
        if i == userB_race:
            return float(retrieve_ethnicity_dict[i]/100)


# levels are arrange in ascending order
# 1- diploma
# 2- associate degree
# 3- bachelors
# 4-masters
# 5-PHD
# level = userA current education level
# predicted-level = AI model prediction about user A best compatible match
# level_recieve= User B current education level
def education_cal(level, predicted_level, level_recieve):
    education_number = {"Diploma": 1, "Associate Degree": 2,
                        "Bachelors": 3, "Masters": 4, "PhD": 5}
    R = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]

    ]

    R = numpy.array(R)
    level = education_number[level]
    level_recieve = education_number[level_recieve]
    # print(level,level_recieve)
    R[0][level-1] = level
    R[1][level_recieve-1] = level_recieve
    predicted_level = education_number[predicted_level]
    N = len(R)
    M = len(R[0])
    K = 2

    P2 = numpy.array([[0.09623613, 0.8288161],
                      [0.86809128, 0.2776751]])
    Q2 = numpy.array([[0.21616114, 0.34524425],
                      [0.19479104, 0.12072784],
                      [0.26481668, 0.42976937],
                      [0.57555023, 0.53077791],
                      [0.34441631, 0.57870231]])

    nP, nQ = matrix_factorization(R, P2, Q2, K)
    nR = numpy.dot(nP, nQ.T)
    if level == level_recieve and predicted_level == level and predicted_level == level_recieve:
        return 1
    if level <= level_recieve:
        user_A = sum(nR[0][:level])
        user_B = sum(nR[1][:level_recieve])
        relation = user_A/user_B
        ratio_rows = sum(nR[0]) / sum(nR[1])
        level_difference = predicted_level-level
        if level == level_recieve and level_difference >= 1:
            # edge cases print("edge case")

            return predicted_level / (ratio_rows*predicted_level + relation*(int(level_difference)))
        if predicted_level-level_recieve >= 1 and predicted_level-level >= 1:
            relation = user_B/user_A
            return predicted_level / (ratio_rows*predicted_level + relation*(int(level_difference)))
        else:
            result = (ratio_rows*predicted_level + relation *
                      (level_recieve - level)) / level_recieve
            return result

    else:
        user_A = sum(nR[0][:level])
        user_B = sum(nR[1][:level_recieve])
        relation = user_B/user_A
        ratio_rows = sum(nR[1]) / sum(nR[0])
        if predicted_level-level_recieve >= 1 and predicted_level-level >= 1:
            relation = user_A/user_B
            return predicted_level / (ratio_rows*predicted_level + relation*(predicted_level-level_recieve))
        else:
            result = (ratio_rows * predicted_level +
                      relation * (level-level_recieve)) / level
            return result


def occupation_cal(curr_occupation, predicted_occupation, rec_occupation):
    occupation_number = {"Science": 1, "Technology": 2,
                         "Construction": 3, "Business": 4, "Communication": 5, 'Law': 6}
    R = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    R = numpy.array(R)
    curr_occupation = occupation_number[curr_occupation]
    rec_occupation = occupation_number[rec_occupation]
    R[0][curr_occupation-1] = curr_occupation
    R[1][rec_occupation-1] = rec_occupation
    predicted_occupation = occupation_number[predicted_occupation]
    N = len(R)
    M = len(R[0])
    K = 2
    P1 = numpy.array([[0.63632385, 0.32576404],
                      [0.28746965, 0.83440233]])
    Q1 = numpy.array([[0.37123526, 0.74104888],
                      [0.31432217, 0.65385106],
                      [0.67300467, 0.40201349],
                      [0.7737731,  0.36044194],
                      [0.24890191, 0.40890149],
                      [0.80346764, 0.2857713]])
    nP, nQ = matrix_factorization(R, P1, Q1, K)
    nR = numpy.dot(nP, nQ.T)
    if curr_occupation == rec_occupation and predicted_occupation == curr_occupation and predicted_occupation == rec_occupation:
        return 1
    if predicted_occupation == rec_occupation:
        return 1
    if curr_occupation <= rec_occupation:
        user_A = sum(nR[0][:curr_occupation])
        user_B = sum(nR[1][:rec_occupation])
        relation = user_A/user_B
        ratio_rows = sum(nR[0]) / sum(nR[1])
        occ_diff = predicted_occupation-curr_occupation
        if curr_occupation == rec_occupation and occ_diff >= 1:
            # edge cases print("edge case")
            return predicted_occupation / (ratio_rows*predicted_occupation + relation*(int(occ_diff)))
        if predicted_occupation-rec_occupation >= 1 and predicted_occupation-curr_occupation >= 1:

            relation = user_B/user_A
            return predicted_occupation / (ratio_rows*predicted_occupation + relation*(int(occ_diff)))
        else:
            result = (ratio_rows*predicted_occupation + relation *
                      (rec_occupation - curr_occupation)) / rec_occupation
            return result

    else:
        user_A = sum(nR[0][:curr_occupation])
        user_B = sum(nR[1][:rec_occupation])
        relation = user_B/user_A
        ratio_rows = sum(nR[1]) / sum(nR[0])
        occ_diff = predicted_occupation-rec_occupation
        if predicted_occupation-rec_occupation >= 1 and predicted_occupation-curr_occupation >= 1:

            return predicted_occupation / (ratio_rows*predicted_occupation + relation*(int(occ_diff)))
        else:
            result = (ratio_rows * predicted_occupation + relation *
                      (curr_occupation-rec_occupation))/curr_occupation
            return result


# dt={"gender":'Male', 'height':'170', 'leadership':'autocratic', 'ethnicity':'black', 'personality':}
def convert_user_matrix_userA(lst):
    lst = lst[0]

    personality_number = {"Introvert": 0, "Ambivert": 1, "Extrovert": 2}
    leadership_number = {"Laissez-Faire": 0, "Democratic": 1, "Autocratic": 2}
    hobby_number = {"Sports": 0, "Music": 1, "Exercising": 2, "Shopping": 3,
                    "Dancing": 4, "Watching-TV": 5, "Reading and Writing": 6, "Arts": 7}
    gender_number = {'Female': 0, 'Male': 1}
    ethnicity_number = {"Black": 0, "White": 1,
                        "Chinese": 2, "Indian": 3, "Hispanic": 4}
    education_number = {"Diploma": 0, "Associate Degree": 1,
                        "Bachelors": 2, "Masters": 3, "PhD": 4}
    occupation_number = {"Science": 0, "Technology": 1,
                         "Construction": 2, "Business": 3, "Communication": 4, 'Law': 5}
    return [[personality_number[lst['personality']], leadership_number[lst['leadership']], hobby_number[lst['hobby']]],
            [gender_number[lst['sex']], int(lst['age']), int(lst['height'])],
            [ethnicity_number[lst['ethnicity']], education_number[lst['education']], occupation_number[lst['occupation']]]]


def convert_user_matrix(lst):

    personality_number = {"Introvert": 0, "Ambivert": 1, "Extrovert": 2}
    leadership_number = {"Laissez-Faire": 0, "Democratic": 1, "Autocratic": 2}
    hobby_number = {"Sports": 0, "Music": 1, "Exercising": 2, "Shopping": 3,
                    "Dancing": 4, "Watching-TV": 5, "Reading and Writing": 6, "Arts": 7}
    gender_number = {'Female': 0, 'Male': 1}
    ethnicity_number = {"Black": 0, "White": 1,
                        "Chinese": 2, "Indian": 3, "Hispanic": 4}
    education_number = {"Diploma": 0, "Associate Degree": 1,
                        "Bachelors": 2, "Masters": 3, "PhD": 4}
    occupation_number = {"Science": 0, "Technology": 1,
                         "Construction": 2, "Business": 3, "Communication": 4, 'Law': 5}
    return [[personality_number[lst['personality']], leadership_number[lst['leadership']], hobby_number[lst['hobby']]],
            [gender_number[lst['sex']], int(lst['age']), int(lst['height'])],
            [ethnicity_number[lst['ethnicity']], education_number[lst['education']], occupation_number[lst['occupation']]]]


def unconvert_user_matrix(lst):

    personality_number = {0: "Introvert", 1: "Ambivert", 2: "Extrovert"}
    leadership_number = {0: "Laissez-Faire", 1: "Democratic", 2: "Autocratic"}
    hobby_number = {0: "Sports", 1: "Music", 2: "Exercising", 3: "Shopping",
                    4: "Dancing", 5: "Watching-TV", 6: "Reading and Writing", 7: "Arts"}
    gender_number = {0: 'Female', 1: 'Male'}
    ethnicity_number = {0: "Black", 1: "White",
                        2: "Chinese", 3: "Indian", 4: "Hispanic"}
    education_number = {0: "Diploma", 1: "Associate Degree",
                        2: "Bachelors", 3: "Masters", 4: "PhD"}
    occupation_number = {0: "Science", 1: "Technology",
                         2: "Construction", 3: "Business", 4: "Communication", 5: 'Law'}
    return [[personality_number[lst[0][0]], leadership_number[lst[0][1]], hobby_number[lst[0][2]]],
            [gender_number[lst[1][0]], lst[1][1], lst[1][2]],
            [ethnicity_number[lst[2][0]], education_number[lst[2][1]], occupation_number[lst[2][2]]]]

#print(unconvert_user_matrix([[0, 1, 6], [1, 22, 180], [1, 3, 1]]))


loaded_model_age = joblib.load('finalized_model_age.sav')
loaded_model_height = joblib.load('finalized_model_height.sav')
personality_model = tf.keras.models.load_model('personality_model')
leadership_model = tf.keras.models.load_model('leadership_model')
hobby_model = tf.keras.models.load_model('hobby_model')
education_model = tf.keras.models.load_model('education_model_5_features')
occupation_model = tf.keras.models.load_model('occupation_model_5_features')

#newlist= sorted(result, key=itemgetter('CSI'))


def REGCSI(userA, db):
    list_of_persons = []
    print('>>>>>>>>>', userA)
    #predicted_userA= unconvert_user_matrix(model(convert_user_matrix(userA)))
    details_userA = userA[0]
    numeric_userA = convert_user_matrix_userA(userA)
    print('>>>>>>', numeric_userA)
    #numeric_userB= userB
    words_userA = unconvert_user_matrix(numeric_userA)
    # print('userA:',userA)
    #userB= unconvert_user_matrix(userB)
    # print('userB:',userB)
    # name=details_userA['username']
    # print('name',name)
    age_pred = int(loaded_model_age.predict(
        [[numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]]))
    height_pred = int(loaded_model_height.predict(
        [[numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]]))

    personality_pred = numpy.argmax(personality_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
    leadership_pred = numpy.argmax(leadership_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
    hobby_pred = numpy.argmax(hobby_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
    education_pred = numpy.argmax(education_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[1][0], numeric_userA[2][1], numeric_userA[2][2]]])))
    occupation_pred = numpy.argmax(occupation_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[1][0], numeric_userA[2][1], numeric_userA[2][2]]])))

    predicted_user_matrix = [[personality_pred, leadership_pred, hobby_pred], [
        numeric_userA[1][0], age_pred, height_pred], [numeric_userA[2][0], education_pred, occupation_pred]]
    #print("predicted user matrix: ",predicted_user_matrix)
    con_predicted_user_matrix = unconvert_user_matrix(predicted_user_matrix)
    #print('occupation:  ',occupation_pred)
    #print("predicted user matrix:    ",con_predicted_user_matrix)
    for i in db:
        # print("loop",i)
        userB = convert_user_matrix(i)
        userB = unconvert_user_matrix(userB)
        personality_csi = get_personality(
            con_predicted_user_matrix[0][0].lower(), i['personality'].lower(), personality_wt)

        leadership_csi = get_leadership(
            con_predicted_user_matrix[0][1].lower(), i['leadership'].lower(), leadership_wt)

        hobby_csi = get_hobby(
            con_predicted_user_matrix[0][2].lower(), i['hobby'].lower(), hobby_wt)
        gender_csi = gender_cal(words_userA[1][0].lower(
        ), details_userA['pref_sex'].lower(), i['sex'].lower())
        age_csi = age_cal(
            int(words_userA[1][1]), con_predicted_user_matrix[1][1], int(i['age']))
        height_csi = height_cal(
            int(words_userA[1][2]), con_predicted_user_matrix[1][2], int(i['height']))
        ethnicity_csi = ethnicity_cal(words_userA[2][0].lower(
        ), details_userA['pref_ethnicity'].lower(), i['ethnicity'].lower())
        education_csi = education_cal(
            words_userA[2][1], con_predicted_user_matrix[2][1], i['education'])
        occupation_csi = occupation_cal(
            words_userA[2][2], con_predicted_user_matrix[2][2], i['occupation'])
        #print('occupation csi:',occupation_csi,words_userA[2][2],con_predicted_user_matrix[2][2],i['occupation'] )
        # name2=i['username']
        # print('name2',name2)

        total = personality_csi+leadership_csi + hobby_csi + gender_csi + \
            age_csi + height_csi + ethnicity_csi + education_csi + occupation_csi
        results = {"userA username ": details_userA['username'], "userB username": i['username'], 'CSI': total,


                   'personality_score': round(float(personality_csi), 3), 'leadership_score': round(float(leadership_csi), 3),
                   'hobby_score': round(float(hobby_csi), 3), 'gender_score': int(gender_csi), 'age_score': round(float(age_csi), 3), 'height_score': round(float(height_csi), 3),
                   'ethnicity_score': round(float(ethnicity_csi), 3),  'education_score': round(float(education_csi), 3), 'occupation_score': round(float(occupation_csi), 3),


                   'con_personality_score': int((personality_csi/total)*100), 'con_leadership_score': int((leadership_csi/total)*100),
                   'con_hobby_score': int((hobby_csi/total)*100), 'con_gender_score': int((gender_csi/total)*100), 'con_age_score': int((age_csi/total)*100), 'con_height_score': int((height_csi/total)*100),
                   'con_ethnicity_score': int((ethnicity_csi/total)*100),  'con_education_score': int((education_csi/total)*100), 'con_occupation_score': int((occupation_csi/total)*100)}

        list_of_persons.append(results)
        #print("results   :        ",results)
    top_nine = sorted(list_of_persons, key=itemgetter('CSI'), reverse=True)
    top_nine = top_nine[0:9]
    bottom_nine = sorted(list_of_persons, key=itemgetter('CSI'))
    bottom_nine = bottom_nine[0:9]
    print("top 9:          ", top_nine)
    print("bottom 9:          ", bottom_nine)
    return list_of_persons, bottom_nine, top_nine


x = [{'username': 'Nicholas', 'first_name': 'Nicholas', 'last_name': 'White', 'sex': 'Male', 'pref_sex': 'Male', 'age': '32', 'height': '144', 'leadership': 'Autocratic',
      'education': 'Masters', 'ethnicity': 'White', 'pref_ethnicity': 'Black', 'hobby': 'Music', 'occupation': 'Construction', 'personality': 'Introvert'}]


dt = [{'username': 'Nicholas', 'first_name': 'Nicholas', 'last_name': 'White', 'sex': 'Male', 'pref_sex': 'Male', 'age': '32', 'height': '144', 'leadership': 'Autocratic', 'education': 'Masters', 'ethnicity': 'White', 'pref_ethnicity': 'Black', 'hobby': 'Music', 'occupation': 'Construction', 'personality': 'Introvert'}, {'username': 'Tina', 'first_name': 'Tina', 'last_name': 'Meza', 'sex': 'Male', 'pref_sex': 'Male', 'age': '33', 'height': '179', 'leadership': 'Autocratic', 'education': 'PhD', 'ethnicity': 'Indian', 'pref_ethnicity': 'Indian', 'hobby': 'Watching-TV', 'occupation': 'Communication', 'personality': 'Ambivert'}, {'username': 'Rachel', 'first_name': 'Rachel', 'last_name': 'Johnson', 'sex': 'Male', 'pref_sex': 'Male', 'age': '30', 'height': '152', 'leadership': 'Autocratic', 'education': 'PhD', 'ethnicity': 'Indian', 'pref_ethnicity': 'Chinese', 'hobby': 'Reading and Writing', 'occupation': 'Construction', 'personality': 'Extrovert'}, {'username': 'Fred', 'first_name': 'Fred', 'last_name': 'Rodriguez', 'sex': 'Male', 'pref_sex': 'Male', 'age': '31', 'height': '180', 'leadership': 'Autocratic', 'education': 'Associate Degree', 'ethnicity': 'Indian', 'pref_ethnicity': 'Indian', 'hobby': 'Arts', 'occupation': 'Technology', 'personality': 'Extrovert'}, {'username': 'Mary', 'first_name': 'Mary', 'last_name': 'Diaz', 'sex': 'Female', 'pref_sex': 'Female', 'age': '34', 'height': '143', 'leadership': 'Democratic', 'education': 'Diploma', 'ethnicity': 'Indian', 'pref_ethnicity': 'Hispanic', 'hobby': 'Exercising', 'occupation': 'Law', 'personality': 'Ambivert'}, {'username': 'Lisa', 'first_name': 'Lisa', 'last_name': 'Burns', 'sex': 'Female', 'pref_sex': 'Male', 'age': '24', 'height': '170', 'leadership': 'Autocratic', 'education': 'PhD', 'ethnicity': 'White', 'pref_ethnicity': 'Black', 'hobby': 'Reading and Writing', 'occupation': 'Technology', 'personality': 'Introvert'}, {'username': 'Donna', 'first_name': 'Donna', 'last_name': 'Mitchell', 'sex': 'Male', 'pref_sex': 'Female', 'age': '24', 'height': '150', 'leadership': 'Democratic', 'education': 'Bachelors', 'ethnicity': 'White', 'pref_ethnicity': 'Hispanic', 'hobby': 'Exercising', 'occupation': 'Law', 'personality': 'Extrovert'}, {'username': 'Justin', 'first_name': 'Justin', 'last_name': 'Richardson', 'sex': 'Female', 'pref_sex': 'Female', 'age': '32', 'height': '179', 'leadership': 'Democratic', 'education': 'Masters', 'ethnicity': 'Hispanic', 'pref_ethnicity': 'Chinese', 'hobby': 'Music', 'occupation': 'Science', 'personality': 'Extrovert'}, {'username': 'Melissa',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  'first_name': 'Melissa', 'last_name': 'Perkins', 'sex': 'Male', 'pref_sex': 'Female', 'age': '34', 'height': '182', 'leadership': 'Autocratic', 'education': 'PhD', 'ethnicity': 'White', 'pref_ethnicity': 'Hispanic', 'hobby': 'Shopping', 'occupation': 'Construction', 'personality': 'Ambivert'}, {'username': 'Manuel', 'first_name': 'Manuel', 'last_name': 'Hammond', 'sex': 'Female', 'pref_sex': 'Male', 'age': '24', 'height': '148', 'leadership': 'Laissez-Faire', 'education': 'Associate Degree', 'ethnicity': 'White', 'pref_ethnicity': 'Indian', 'hobby': 'Reading and Writing', 'occupation': 'Construction', 'personality': 'Introvert'}, {'username': 'Carl', 'first_name': 'Carl', 'last_name': 'Robles', 'sex': 'Male', 'pref_sex': 'Female', 'age': '24', 'height': '192', 'leadership': 'Laissez-Faire', 'education': 'Masters', 'ethnicity': 'Chinese', 'pref_ethnicity': 'Indian', 'hobby': 'Arts', 'occupation': 'Business', 'personality': 'Ambivert'}, {'username': 'Robert', 'first_name': 'Robert', 'last_name': 'Davis', 'sex': 'Male', 'pref_sex': 'Male', 'age': '29', 'height': '193', 'leadership': 'Autocratic', 'education': 'Associate Degree', 'ethnicity': 'Hispanic', 'pref_ethnicity': 'Chinese', 'hobby': 'Arts', 'occupation': 'Technology', 'personality': 'Ambivert'}, {'username': 'Gregory', 'first_name': 'Gregory', 'last_name': 'Richardson', 'sex': 'Male', 'pref_sex': 'Female', 'age': '29', 'height': '167', 'leadership': 'Democratic', 'education': 'Bachelors', 'ethnicity': 'Indian', 'pref_ethnicity': 'Indian', 'hobby': 'Shopping', 'occupation': 'Law', 'personality': 'Ambivert'}, {'username': 'Curtis', 'first_name': 'Curtis', 'last_name': 'Jenkins', 'sex': 'Female', 'pref_sex': 'Female', 'age': '33', 'height': '166', 'leadership': 'Democratic', 'education': 'Bachelors', 'ethnicity': 'Hispanic', 'pref_ethnicity': 'Black', 'hobby': 'Sports', 'occupation': 'Science', 'personality': 'Ambivert'}, {'username': 'Matthew', 'first_name': 'Matthew', 'last_name': 'Cook', 'sex': 'Male', 'pref_sex': 'Male', 'age': '30', 'height': '156', 'leadership': 'Laissez-Faire', 'education': 'Masters', 'ethnicity': 'White', 'pref_ethnicity': 'Indian', 'hobby': 'Reading and Writing', 'occupation': 'Communication', 'personality': 'Introvert'}, {'username': 'Lanai', 'first_name': 'Lanai', 'last_name': 'Nevers', 'sex': 'Male', 'pref_sex': 'Male', 'age': '27', 'height': '191', 'leadership': 'Autocratic', 'education': 'Diploma', 'ethnicity': 'White', 'pref_ethnicity': 'Chinese', 'hobby': 'Music', 'occupation': 'Construction', 'personality': 'Ambivert'}]
# print(convert_user_matrix_userA(x))
#print(unconvert_user_matrix([[0, 2, 1], [1, 32, 144], [1, 3, 2]]))
# print(REGCSI(x,dt))


#print(REGCSI([[0, 1, 0], [1, 22, 180], [1, 3, 1]], [[[0, 1, 0], [1, 24, 186], [1, 3, 1]],[[0, 1, 0], [1, 28, 176], [1, 4, 1]],]))
#print(REGCSI([[0, 1, 0], [1, 22, 170], [1, 3, 1]], [[[0, 1, 0], [1, 28, 176], [1, 4, 1]],]))

def GRPCSI(userA, db, max_size):
    list_of_persons = []
#     print(' userA>>>>', userA)
    details_userA = userA[0]

    numeric_userA = convert_user_matrix_userA(userA)
#     print('numeric A >>>>>>', numeric_userA)
    words_userA = unconvert_user_matrix(numeric_userA)

    age_pred = int(loaded_model_age.predict(
        [[numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]]))
    height_pred = int(loaded_model_height.predict(
        [[numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]]))

    personality_pred = numpy.argmax(personality_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
    leadership_pred = numpy.argmax(leadership_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
    hobby_pred = numpy.argmax(hobby_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
    education_pred = numpy.argmax(education_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[1][0], numeric_userA[2][1], numeric_userA[2][2]]])))
    occupation_pred = numpy.argmax(occupation_model.predict(numpy.array(
        [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[1][0], numeric_userA[2][1], numeric_userA[2][2]]])))

    predicted_user_matrix = [[personality_pred, leadership_pred, hobby_pred], [
        numeric_userA[1][0], age_pred, height_pred], [numeric_userA[2][0], education_pred, occupation_pred]]
    con_predicted_user_matrix = unconvert_user_matrix(predicted_user_matrix)

    for i in db:
        userB = convert_user_matrix(i)
        userB = unconvert_user_matrix(userB)
        personality_csi = get_personality(
            con_predicted_user_matrix[0][0].lower(), i['personality'].lower(), personality_wt)
        leadership_csi = get_leadership(
            con_predicted_user_matrix[0][1].lower(), i['leadership'].lower(), leadership_wt)
        hobby_csi = get_hobby(
            con_predicted_user_matrix[0][2].lower(), i['hobby'].lower(), hobby_wt)
        gender_csi = gender_cal(words_userA[1][0].lower(
        ), details_userA['pref_sex'].lower(), i['sex'].lower())
        age_csi = age_cal(
            int(words_userA[1][1]), con_predicted_user_matrix[1][1], int(i['age']))
        height_csi = height_cal(
            int(words_userA[1][2]), con_predicted_user_matrix[1][2], int(i['height']))
        ethnicity_csi = ethnicity_cal(words_userA[2][0].lower(
        ), details_userA['pref_ethnicity'].lower(), i['ethnicity'].lower())
        education_csi = education_cal(
            words_userA[2][1], con_predicted_user_matrix[2][1], i['education'])
        occupation_csi = occupation_cal(
            words_userA[2][2], con_predicted_user_matrix[2][2], i['occupation'])

        total = personality_csi+leadership_csi + hobby_csi + gender_csi + \
            age_csi + height_csi + ethnicity_csi + education_csi + occupation_csi
        results = {"userA username ": details_userA['username'], "userB username": i['username'], 'CSI': total,

                   'username': i['username'],
                   'personality_score': round(float(personality_csi), 3), 'leadership_score': round(float(leadership_csi), 3),
                   'hobby_score': round(float(hobby_csi), 3), 'gender_score': int(gender_csi), 'age_score': round(float(age_csi), 3), 'height_score': round(float(height_csi), 3),
                   'ethnicity_score': round(float(ethnicity_csi), 3),  'education_score': round(float(education_csi), 3), 'occupation_score': round(float(occupation_csi), 3),


                   'con_personality_score': int((personality_csi/total)*100), 'con_leadership_score': int((leadership_csi/total)*100),
                   'con_hobby_score': int((hobby_csi/total)*100), 'con_gender_score': int((gender_csi/total)*100), 'con_age_score': int((age_csi/total)*100), 'con_height_score': int((height_csi/total)*100),
                   'con_ethnicity_score': int((ethnicity_csi/total)*100),  'con_education_score': int((education_csi/total)*100), 'con_occupation_score': int((occupation_csi/total)*100)}
        list_of_persons.append(results)
    top = sorted(list_of_persons, key=itemgetter('CSI'), reverse=True)
    top = top[0:max_size-1]
    bottom = sorted(list_of_persons, key=itemgetter('CSI'))
    bottom = bottom[0:max_size-1]

    return top, bottom


# def get_remaining_set(large_set,visited):
#     lst=[]
#     for i in large_set:
# #         print('i>>>>>>>>>>>>>', i)
#         if visited==[]:
#             pass
#         else:

#             for g in visited:
# #                 print('g>>>>>>>>>>>>>', g)
#                 if i==g:
#                     m= large_set.index(i)
#                     large_set.pop(m)
#     print('large set>>>>>>>', len(large_set))
#     return large_set


def get_remaining_set(large_set, visited):
    lst = []
    for i in visited:

        for g in large_set:

            if i == g['username']:
                m = large_set.index(g)
                print('popppppp>>>>>>>', m)
                large_set.pop(m)
    return large_set


def GRP_SETUP(set_group, group_size):
    set_size = len(set_group)
    no_of_groups = math.ceil(set_size/group_size)
    assigned = {}
    groups = {}

    for i in range(0, no_of_groups):
        remaining_set = get_remaining_set(set_group, assigned)
        print('remainder>>>>>>>', len(remaining_set))
#         print('remainder>>>>>>>',remaining_set)
        main_member = [remaining_set.pop(0)]
        assigned[main_member[0]['username']] = 'visited'
        print('testing!!!!!!!!!!!')
        csi_members = GRPCSI(main_member, remaining_set, group_size)
        members = []
#         members.append( main_member[0])
        for g in range(1, group_size):
            if remaining_set == []:
                groups[i] = main_member
            else:

                other_member = csi_members.pop(0)
#                 print('other member>>>>>>>>>>>>>>',other_member)

                members.append(other_member)
                assigned[other_member['username']] = 'visited'
#                 print('assigned>>>>>>>', assigned)
                groups[i] = members
#         print('assigned>>>>>>>', assigned)

    return groups



def cal_GRPCSI(set_group, group_size):
    groups = GRP_SETUP(set_group, group_size)
    sets = {}
    for i in groups.keys():
        curr = [groups[i].pop(0)]
        print('currr>>>>>>>>>>', curr)
        rest = groups[i]
#         print('rest>>>>>>>>>>', rest)
        sets[i] = GRPCSI(curr, rest, group_size)
    return sets


x = [{'username': 'Nicholas', 'first_name': 'Nicholas', 'last_name': 'White', 'sex': 'Male', 'pref_sex': 'Male', 'age': '32', 'height': '144', 'leadership': 'Autocratic',
      'education': 'Masters', 'ethnicity': 'White', 'pref_ethnicity': 'Black', 'hobby': 'Music', 'occupation': 'Construction', 'personality': 'Introvert'}]


dt = [{'username': 'Nicholas', 'first_name': 'Nicholas', 'last_name': 'White', 'sex': 'Male', 'pref_sex': 'Male', 'age': '32', 'height': '144', 'leadership': 'Autocratic', 'education': 'Masters', 'ethnicity': 'White', 'pref_ethnicity': 'Black', 'hobby': 'Music', 'occupation': 'Construction', 'personality': 'Introvert'}, {'username': 'Tina', 'first_name': 'Tina', 'last_name': 'Meza', 'sex': 'Male', 'pref_sex': 'Male', 'age': '33', 'height': '179', 'leadership': 'Autocratic', 'education': 'PhD', 'ethnicity': 'Indian', 'pref_ethnicity': 'Indian', 'hobby': 'Watching-TV', 'occupation': 'Communication', 'personality': 'Ambivert'}, {'username': 'Rachel', 'first_name': 'Rachel', 'last_name': 'Johnson', 'sex': 'Male', 'pref_sex': 'Male', 'age': '30', 'height': '152', 'leadership': 'Autocratic', 'education': 'PhD', 'ethnicity': 'Indian', 'pref_ethnicity': 'Chinese', 'hobby': 'Reading and Writing', 'occupation': 'Construction', 'personality': 'Extrovert'}, {'username': 'Fred', 'first_name': 'Fred', 'last_name': 'Rodriguez', 'sex': 'Male', 'pref_sex': 'Male', 'age': '31', 'height': '180', 'leadership': 'Autocratic', 'education': 'Associate Degree', 'ethnicity': 'Indian', 'pref_ethnicity': 'Indian', 'hobby': 'Arts', 'occupation': 'Technology', 'personality': 'Extrovert'}, {'username': 'Mary', 'first_name': 'Mary', 'last_name': 'Diaz', 'sex': 'Female', 'pref_sex': 'Female', 'age': '34', 'height': '143', 'leadership': 'Democratic', 'education': 'Diploma', 'ethnicity': 'Indian', 'pref_ethnicity': 'Hispanic', 'hobby': 'Exercising', 'occupation': 'Law', 'personality': 'Ambivert'}, {'username': 'Lisa', 'first_name': 'Lisa', 'last_name': 'Burns', 'sex': 'Female', 'pref_sex': 'Male', 'age': '24', 'height': '170', 'leadership': 'Autocratic', 'education': 'PhD', 'ethnicity': 'White', 'pref_ethnicity': 'Black', 'hobby': 'Reading and Writing', 'occupation': 'Technology', 'personality': 'Introvert'}, {'username': 'Donna', 'first_name': 'Donna', 'last_name': 'Mitchell', 'sex': 'Male', 'pref_sex': 'Female', 'age': '24', 'height': '150', 'leadership': 'Democratic', 'education': 'Bachelors', 'ethnicity': 'White', 'pref_ethnicity': 'Hispanic', 'hobby': 'Exercising', 'occupation': 'Law', 'personality': 'Extrovert'}, {'username': 'Justin', 'first_name': 'Justin', 'last_name': 'Richardson', 'sex': 'Female', 'pref_sex': 'Female', 'age': '32', 'height': '179', 'leadership': 'Democratic', 'education': 'Masters', 'ethnicity': 'Hispanic', 'pref_ethnicity': 'Chinese', 'hobby': 'Music', 'occupation': 'Science', 'personality': 'Extrovert'}, {'username': 'Melissa',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  'first_name': 'Melissa', 'last_name': 'Perkins', 'sex': 'Male', 'pref_sex': 'Female', 'age': '34', 'height': '182', 'leadership': 'Autocratic', 'education': 'PhD', 'ethnicity': 'White', 'pref_ethnicity': 'Hispanic', 'hobby': 'Shopping', 'occupation': 'Construction', 'personality': 'Ambivert'}, {'username': 'Manuel', 'first_name': 'Manuel', 'last_name': 'Hammond', 'sex': 'Female', 'pref_sex': 'Male', 'age': '24', 'height': '148', 'leadership': 'Laissez-Faire', 'education': 'Associate Degree', 'ethnicity': 'White', 'pref_ethnicity': 'Indian', 'hobby': 'Reading and Writing', 'occupation': 'Construction', 'personality': 'Introvert'}, {'username': 'Carl', 'first_name': 'Carl', 'last_name': 'Robles', 'sex': 'Male', 'pref_sex': 'Female', 'age': '24', 'height': '192', 'leadership': 'Laissez-Faire', 'education': 'Masters', 'ethnicity': 'Chinese', 'pref_ethnicity': 'Indian', 'hobby': 'Arts', 'occupation': 'Business', 'personality': 'Ambivert'}, {'username': 'Robert', 'first_name': 'Robert', 'last_name': 'Davis', 'sex': 'Male', 'pref_sex': 'Male', 'age': '29', 'height': '193', 'leadership': 'Autocratic', 'education': 'Associate Degree', 'ethnicity': 'Hispanic', 'pref_ethnicity': 'Chinese', 'hobby': 'Arts', 'occupation': 'Technology', 'personality': 'Ambivert'}, {'username': 'Gregory', 'first_name': 'Gregory', 'last_name': 'Richardson', 'sex': 'Male', 'pref_sex': 'Female', 'age': '29', 'height': '167', 'leadership': 'Democratic', 'education': 'Bachelors', 'ethnicity': 'Indian', 'pref_ethnicity': 'Indian', 'hobby': 'Shopping', 'occupation': 'Law', 'personality': 'Ambivert'}, {'username': 'Curtis', 'first_name': 'Curtis', 'last_name': 'Jenkins', 'sex': 'Female', 'pref_sex': 'Female', 'age': '33', 'height': '166', 'leadership': 'Democratic', 'education': 'Bachelors', 'ethnicity': 'Hispanic', 'pref_ethnicity': 'Black', 'hobby': 'Sports', 'occupation': 'Science', 'personality': 'Ambivert'}, {'username': 'Matthew', 'first_name': 'Matthew', 'last_name': 'Cook', 'sex': 'Male', 'pref_sex': 'Male', 'age': '30', 'height': '156', 'leadership': 'Laissez-Faire', 'education': 'Masters', 'ethnicity': 'White', 'pref_ethnicity': 'Indian', 'hobby': 'Reading and Writing', 'occupation': 'Communication', 'personality': 'Introvert'}, {'username': 'Lanai', 'first_name': 'Lanai', 'last_name': 'Nevers', 'sex': 'Male', 'pref_sex': 'Male', 'age': '27', 'height': '191', 'leadership': 'Autocratic', 'education': 'Diploma', 'ethnicity': 'White', 'pref_ethnicity': 'Chinese', 'hobby': 'Music', 'occupation': 'Construction', 'personality': 'Ambivert'}]
print(GRP_SETUP(dt, 3))
# print(GRPCSI(x,dt,4))
# print(cal_GRPCSI(dt,4))
