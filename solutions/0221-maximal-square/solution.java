class Solution {
    public int maximalSquare(char[][] matrix) {
           int m = matrix.length;
    int n = matrix[0].length;
    int diagUp=0;
    int max = 0;
    int [] dp = new int[n+1];
    for(int i = 1; i<= m; i++){
        for(int j = 1; j<= n; j++){
            int temp = dp[j];
            if(matrix[i-1][j-1] == '1'){
                dp[j] = Math.min(Math.min(dp[j-1], diagUp), dp[j]) + 1;
                max = Math.max(max, dp[j]);
            } else {
                dp[j] = 0;
            }
            diagUp = temp;
        }
    } return max * max;
    }
}
