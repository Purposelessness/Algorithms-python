def z_function(s) -> list[int]:
    z = [0] * len(s)
    left = -1
    right = -1
    for i in range(1, len(s)):
        if i in [left, right]:
            z[i] = min(z[i - left], right - i + 1)
        while i + z[i] < len(s) and s[i + z[i]] == s[z[i]]:
            z[i] += 1
        if i + z[i] - 1 > right:
            left = i
            right = i + z[i] - 1
    return z
