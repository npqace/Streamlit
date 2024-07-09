import streamlit as st

def levenshtein_distance(source, target):
    m = len(source) + 1
    n =len(target) + 1
    
    dp = [[0 for _ in range(n)] for _ in range(m)]
    
    for i in range(m):
        dp[i][0] = i
    for j in range(n):
        dp[0][j] = j
    
    for i in range(1, m):
        for j in range(1, n):
            if source[i-1] == target[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i-1][j] + 1, # deletion
                dp[i][j-1] + 1, # insertion
                dp[i-1][j-1] + cost # substitution
            )
    return dp[m-1][n-1]

def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words
vocabs = load_vocab(file_path='./data/vocab.txt')

def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')
    
    if st.button("Compute"):
        lev_dis = dict()
        for vocab in vocabs:
            lev_dis[vocab] = levenshtein_distance(word, vocab)
        
        # sort by distance
        sorted_dis = dict(sorted(lev_dis.items(), key=lambda item: item[1]))
        correct_word = list(sorted_dis.keys())[0]
        st.write("Correct word: ", correct_word)
        
        col1, col2 = st.columns(2)
        col1.write("Vocabulary:")
        col1.write(vocabs)
        
        col2.write("Distances: ")
        col2.write(sorted_dis)

if __name__ == "__main__":
    main()