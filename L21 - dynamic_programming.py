def binomial(n: int, k: int) -> int:
    # Usamos una tabla para programación dinámica
    C = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            if j == 0 or j == i:
                C[i][j] = 1
            else:
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    return C[n][k]


def cut_rod(p: list[int], n: int) -> tuple[list[int], list[int]]:
    r = [0] * (n + 1)  # r[i] = max revenue for rod of length i
    s = [None] * (n + 1)  # s[i] = first piece to cut off from rod of length i

    for j in range(1, n + 1):
        max_rev = float('-inf')
        for i in range(1, j + 1):
            if i <= len(p):
                if max_rev < p[i - 1] + r[j - i]:
                    max_rev = p[i - 1] + r[j - i]
                    s[j] = i
        r[j] = max_rev

    return r, s


def lcs(x: str, y: str) -> str:
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Construimos la tabla LCS
    for i in range(m):
        for j in range(n):
            if x[i] == y[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])

    # Reconstruimos la subsecuencia LCS
    lcs_str = []
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            lcs_str.append(x[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(lcs_str))


if __name__ == "__main__":
    print(binomial(10, 5))
    # 252
    r, s = cut_rod([1, 5, 8, 9, 10, 17, 17, 20, 24, 30], 10)
    print(r)
    # [0, 1, 5, 8, 10, 13, 17, 18, 22, 25, 30]
    print(s)
    # [None, 1, 2, 3, 2, 2, 6, 1, 2, 3, 10]
    print(lcs("ABCBDAB", "BDCABA"))
    # BCBA
