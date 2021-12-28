import sys

# choose() is the same as computing the number of combinations. Normally this is
# equal to:
#
#   factorial(N) / (factorial(m) * factorial(N - m))
#
# but this is very slow to run and requires a deep stack (without tail
# recursion).
#
# The below algorithm works as follows. First, re-organize as:
#
#   (factorial(N) / (factorial(m)) / factorial(N - m)
#
# It should be obvious that N! / m! is the same thing as N * N - 1 * N - 2 * ...
# m + 1. So we construct our loop to compute that:
#
#   c = 1
#   for i in range(m + 1, n + 1):
#      c *= i
#
# So now we've computed (factorial(N) / (factorial(m)), but we still need to
# divide by factorial(N - m). We already have a for loop, of (N - m) iterations,
# so we can reuse it.
#
# We want to divide by all of the values between 1 and ... (N - m),
# which are the same values as (i - m). Recall that i starts at m + 1, so it
# it will go 1, 2, 3 ... (N - m) because the final value of i will be N.
#
# Since division and multiplication are commutative in this context, and the
# order never matters we place the division directly in-line within the loop.
# Lastly, since we're now dividing, we will end up with fractions at
# intermediary stages, so we use floating point. The end-result will include
# precision errors, but that's ok for our purposes.

def choose(n, m):
    c = 1
    for i in range(m + 1, n + 1):
        c *= float(i) / (i - m) 
    return c

def overlap(n, m, o):
    return (choose(m, o) * choose(n - m, m - o)) / choose(n, m)

def usage():
    print("shard.py n m")
    print()
    print(" n: The total number of elements")
    print(" m: The number of elements per shard")
    print()


if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()

    try:
        n = int(sys.argv[1])
        m = int(sys.argv[2]) 

    except:
        usage()

    if m > n:
        usage()

    print('With a total of %d elements, a randomly chosen shuffleshard of %d elements ...' % (n, m))
    print('')
    for i in range(0, m + 1):
        print('overlaps by %-4d elements with %23.20f %% of other shuffleshards' % (i, overlap(n, m, i) * 100))