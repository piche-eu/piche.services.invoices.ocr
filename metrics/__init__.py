import Levenshtein
import torch
from torchmetrics.text import WordErrorRate
from  torchmetrics.text import CharErrorRate


def n_chat_matched(result:dict, truth:dict) -> torch.Tensor:
    #words error rate
    key_wer = CharErrorRate(result.keys(), truth.keys())
    val_wer = CharErrorRate(result.values(), truth.values())
    return (key_wer, val_wer)

def n_word_matched(result:dict, truth:dict) -> torch.Tensor:
    #words error rate
    key_wer = WordErrorRate(result.keys(), truth.keys())
    val_wer = WordErrorRate(result.values(), truth.values())
    return (key_wer, val_wer)

def levenstein_distance(result:dict, truth:dict) -> tuple(float, float):
    #number of possible transposition between parsed data end expected dictionary
    key_lev_dist = Levenshtein.distance("".join(list(result.keys())), "".join(list(result.keys())))
    val_lev_dist = Levenshtein.distance("".join(list(result.values())), "".join(list(result.values())))
    return (key_lev_dist, val_lev_dist)

def exact_dictionary_matching(result:dict, truth:dict) -> tuple(int, int):
    #calculate the accuracy of the parsed data
    num_matches_keys = 0
    num_matched_val = 0
    for k,v in truth.iter():
        if k in result.keys():num_matches_keys+=1
        if result[k]==truth[k]:num_matched_val+=1
    return (num_matches_keys, num_matched_val)


