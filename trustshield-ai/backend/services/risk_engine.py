def calculate_risk(voice_prob, transaction_flag):

    transaction_score = 1 if transaction_flag == -1 else 0

    final_score = (voice_prob * 0.6) + (transaction_score * 0.4)

    if final_score > 0.75:
        level = "Critical"
    elif final_score > 0.4:
        level = "Medium"
    else:
        level = "Low"

    return final_score, level