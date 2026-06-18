class Solution {
    Integer[] memo;
    public int deleteAndEarn(int[] nums) {
        int max = 0;
        for (int num : nums) {
            max = Math.max(max, num);
        }

        int[] arr = new int[max + 1];
        for (int num : nums) {
            arr[num] += num;
        }

        this.memo = new Integer[max + 1];
        return helper(arr, 0);
    }

    private int helper(int[] arr, int i) {
        if (i >= arr.length) return 0;
        if (memo[i] != null) return memo[i];

        int case0 = helper(arr, i + 1);
        int case1 = arr[i] + helper(arr, i + 2);

        memo[i] = Math.max(case0, case1);
        return memo[i];
    }
}

