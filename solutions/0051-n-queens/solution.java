class Solution {
    List<List<String>> result;
    boolean[][] board;
    boolean[] colSet;
    boolean[] mainDiagSet;
    boolean[] antiDiagSet;
    public List<List<String>> solveNQueens(int n) {
        this.result = new ArrayList<>();
        this.board = new boolean[n][n];
        this.colSet = new boolean[2*n];
        this.mainDiagSet = new boolean[2*n];
        this.antiDiagSet = new boolean[2*n];

        helper(0, n);

        return result;
    }

    private void helper(int r , int n){

        if(r == n){
            List<String> list = new ArrayList<>();
            for(int i=0; i<n; i++){
                StringBuilder sb = new StringBuilder();
                for(int j=0; j<n; j++){
                    if(board[i][j]){
                        sb.append("Q");
                    }else{
                        sb.append(".");
                    }
                }
                list.add(sb.toString());
            }
            result.add(list);
            return;
        }
     
        for(int c=0; c<n; c++){
            
            int md = r+c;
            int ad = r-c + n;

            if(!colSet[c]&& !mainDiagSet[md] && !antiDiagSet[ad])
            {
                colSet[c] = true;
                mainDiagSet[md] = true;
                antiDiagSet[ad] = true;

                board[r][c] = true;
                helper(r+1, n);
                board[r][c] = false;

                colSet[c] = false;
                mainDiagSet[md] = false;
                antiDiagSet[ad] = false;

            }
        }
    }
}

