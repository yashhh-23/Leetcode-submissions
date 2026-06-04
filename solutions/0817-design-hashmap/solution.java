import java.util.LinkedList;

class MyHashMap {
    private static final int SIZE = 1009;
    private LinkedList<int[]>[] buckets;

    public MyHashMap() {
        buckets = new LinkedList[SIZE];
        for (int i = 0; i < SIZE; i++) {
            buckets[i] = new LinkedList<>();
        }
    }

    private int hash(int key) {
        return key % SIZE;
    }

    public void put(int key, int value) {
        int idx = hash(key);
        for (int[] pair : buckets[idx]) {
            if (pair[0] == key) {
                pair[1] = value;
                return;
            }
        }
        buckets[idx].add(new int[]{key, value});
    }

    public int get(int key) {
        int idx = hash(key);
        for (int[] pair : buckets[idx]) {
            if (pair[0] == key) {
                return pair[1];
            }
        }
        return -1;
    }

    public void remove(int key) {
        int idx = hash(key);
        for (int i = 0; i < buckets[idx].size(); i++) {
            if (buckets[idx].get(i)[0] == key) {
                buckets[idx].remove(i);
                return;
            }
        }
    }
}
