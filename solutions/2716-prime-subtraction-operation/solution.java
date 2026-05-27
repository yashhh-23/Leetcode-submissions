import java.util.*;

class Solution {
    public boolean primeSubOperation(int[] nums) {
        int max = 1000;
        List<Integer> primes = sieve(max);

        int prev = 0;
        for (int num : nums) {
            int best = num;
            
            int need = num - prev; // we need result > prev
            int idx = lowerBound(primes, need); // first prime >= need
            
            if (idx > 0) {
                best = num - primes.get(idx - 1);
            }

            if (best <= prev) return false;
            prev = best;
        }
        return true;
    }

    private List<Integer> sieve(int n) {
        boolean[] isPrime = new boolean[n + 1];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;

        for (int i = 2; i * i <= n; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j <= n; j += i) {
                    isPrime[j] = false;
                }
            }
        }

        List<Integer> primes = new ArrayList<>();
        for (int i = 2; i <= n; i++) {
            if (isPrime[i]) primes.add(i);
        }
        return primes;
    }

    private int lowerBound(List<Integer> primes, int target) {
        int l = 0, r = primes.size();
        while (l < r) {
            int m = l + (r - l) / 2;
            if (primes.get(m) < target) l = m + 1;
            else r = m;
        }
        return l;
    }
}
