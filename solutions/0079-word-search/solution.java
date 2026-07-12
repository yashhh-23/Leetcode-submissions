class Solution {
    public boolean exist(char[][] board, String word) {
        int rows= board.length;
        int cols=board[0].length;
        if(word.length()>rows*cols) return false;
        for(int r=0;r<rows;r++)
        {
            for(int c=0;c<cols;c++)
            {
                if(board[r][c]==word.charAt(0))
                {
                    if(dfs(board,word,r,c,0))
                    {
                        return true;
                    }
                }
            }
        } return false;
    }
    private boolean dfs(char[][] board, String word, int r, int c, int idx)
    {
        if(idx== word.length())
        {
            return true;
        }
        if(r>=board.length||c<0||r<0||c>=board[0].length||board[r][c]!= word.charAt(idx))
        {
            return false;
        }
        char temp=board[r][c];
        board[r][c]='#';
        boolean found=dfs(board,word,r+1,c,idx+1)||dfs(board,word,r-1,c,idx+1)||dfs(board,word,r,c+1,idx+1)||dfs(board,word,r,c-1,idx+1);
        board[r][c]=temp;
        return found;
    }
}
