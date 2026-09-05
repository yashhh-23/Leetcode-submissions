import java.util.ArrayDeque;
import java.util.Queue;

class Solution {
    public int shortestPath(int[][] grid, int k) {
        int m = grid.length;
        int n = grid[0].length;


        if (m == 1 && n == 1) {
            return 0;
        }


        if (k >= m + n - 3) {
            return m + n - 2;
        }

k = Math.min(k, m + n - 3);


        boolean[][][] visited = new boolean[m][n][k + 1];


        Queue<int[]> queue = new ArrayDeque<>();

queue.offer(new int[]{0, 0, k});
        visited[0][0][k] = true;

        int steps = 0;
        int[][] directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

        while (!queue.isEmpty()) {
            int size = queue.size();
            steps++;

            for (int i = 0; i < size; i++) {
                int[] curr = queue.poll();
                int r = curr[0];
                int c = curr[1];
                int remK = curr[2];

                for (int[] dir : directions) {
                    int nr = r + dir[0];
                    int nc = c + dir[1];


                    if (nr < 0 || nr >= m || nc < 0 || nc >= n) {
                        continue;
                    }

                    int nextK = remK - grid[nr][nc];


                    if (nextK < 0) {
                        continue;
                    }

                    if (nr == m - 1 && nc == n - 1) {
                        return steps;
                    }

                    if (visited[nr][nc][nextK]) {
                        continue;
                    }

                    visited[nr][nc][nextK] = true;
                    queue.offer(new int[]{nr, nc, nextK});
                }
            }
        }

        return -1;
    }
}
