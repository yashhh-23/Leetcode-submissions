class Solution {
    public int minFallingPathSum(int[][] matrix) {
        int n = matrix.length;
        
        // Start from the second row and update values based on the row above
        for (int r = 1; r < n; r++) {
            for (int c = 0; c < n; c++) {
                // Get the value directly above
                int minAbove = matrix[r - 1][c];
                
                // Get the value from top-left, if it exists
                if (c > 0) {
                    minAbove = Math.min(minAbove, matrix[r - 1][c - 1]);
                }
                
                // Get the value from top-right, if it exists
                if (c < n - 1) {
                    minAbove = Math.min(minAbove, matrix[r - 1][c + 1]);
                }
                
                // Update current cell with the minimum path sum reaching it
                matrix[r][c] += minAbove;
            }
        }
        
        // Find the minimum value in the last row
        int minPathSum = Integer.MAX_VALUE;
        for (int val : matrix[n - 1]) {
            minPathSum = Math.min(minPathSum, val);
        }
        
        return minPathSum;
    }
}
