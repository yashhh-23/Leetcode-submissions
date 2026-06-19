class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        int m = matrix.length;
        int n = matrix[0].length;

        int top = 0, bottom = m-1, l = 0, r = n-1;

        List<Integer> result = new ArrayList<>();

        while(top <= bottom && l <= r){

            for(int i=l; i<=r; i++)
            {
                result.add(matrix[top][i]);
            }
            top++;

            for(int i=top; i<=bottom; i++)
            {
                result.add(matrix[i][r]);
            }
            r--;
          
            if(top <= bottom)
            {
                for(int i=r; i>=l; i--){
                    result.add(matrix[bottom][i]);
                }
                bottom--;
            }

            if(l <= r)
            {
                for(int i=bottom; i>=top; i--)
                {
                    result.add(matrix[i][l]);
                }
                l++;
            }
        }

        return result;
    }
}

